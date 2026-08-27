#!/usr/bin/env python
"""Render the manual's CLI reference from the CLI's `--help` output.

The generator walks each argparse subparser tree and reads the `{a,b,c}` choice
block from `--help`, keeping the reference aligned with the parsers.

The page is generated at docs-build time by `scripts/mkdocs_gen_cli.py` and is
not committed. Run this module directly to inspect the output:

    python scripts/gen_cli_reference.py | less
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

# argparse wraps help to the terminal width, so output is machine-dependent
# unless COLUMNS is pinned.
HELP_COLUMNS = "88"

# Each CLI to document: console script, blurb.
CLIS = [
    (
        "octo",
        "Semantic search over Lean declarations: fetching and building search "
        "databases, and querying them. See [Set up search on your repo]"
        "(../setup-search.md) for how to get started.",
    ),
]

# Backstop against runaway recursion. The current tree is at most three levels.
MAX_DEPTH = 8

# Each `--help` imports the package in a new process. Run independent calls in
# parallel to keep the traversal fast.
MAX_WORKERS = 12

# argparse renders subcommand choices as `{ingest,query,status}`.
_CHOICES_RE = re.compile(r"\{([a-z0-9,_-]+)\}")

# Help lines that say nothing a reader needs.
_NOISE_RE = re.compile(r"^\s*-h, --help\s+show this help message and exit\s*$\n?", re.MULTILINE)

# Dropping the `-h` line leaves a bare `options:` header behind on commands that
# take no other flags. Strip the header too when nothing follows it.
_EMPTY_OPTIONS_RE = re.compile(r"\n*^options:\s*$(?!\n\s+\S)", re.MULTILINE)


def run_help(argv: tuple[str, ...]) -> str:
    """Capture `--help` for one command path; "" if it doesn't respond."""
    try:
        proc = subprocess.run(
            [*argv, "--help"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
            env={**os.environ, "COLUMNS": HELP_COLUMNS},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"warning: `{' '.join(argv)} --help` failed: {exc}", file=sys.stderr)
        return ""
    if proc.returncode != 0:
        print(f"warning: `{' '.join(argv)} --help` exited {proc.returncode}", file=sys.stderr)
        return ""
    return proc.stdout


def subcommands(help_text: str) -> list[str]:
    """Return candidate subcommands from the first `{a,b,c}` group.

    argparse renders subparsers and choice options such as
    `--format {json,markdown}` identically. `documents()` distinguishes them.
    """
    match = _CHOICES_RE.search(help_text)
    return [name for name in match.group(1).split(",") if name] if match else []


def documents(argv: tuple[str, ...], help_text: str) -> bool:
    """Return whether `help_text` describes `argv` rather than its parent.

    A value scraped from a choice option is not a command, but asking for its
    help can still succeed and print the parent's help. The usage line names
    the resolved command, so compare it with `argv`.
    """
    return help_text.startswith(f"usage: {' '.join(argv)}")


def strip_noise(help_text: str) -> str:
    """Remove the universal `-h` line and any `options:` header it emptied."""
    return _EMPTY_OPTIONS_RE.sub("", _NOISE_RE.sub("", help_text)).strip()


def collect(root: str) -> dict[tuple[str, ...], str]:
    """Every (command path -> help text) under `root`.

    Traverse breadth-first so each level runs concurrently. Parsing one level
    provides the paths for the next.
    """
    helps: dict[tuple[str, ...], str] = {}
    frontier = [(root,)]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for _ in range(MAX_DEPTH):
            if not frontier:
                break
            for argv, text in zip(frontier, pool.map(run_help, frontier), strict=True):
                if text and documents(argv, text):
                    helps[argv] = text
            frontier = [
                (*argv, name)
                for argv in frontier
                if argv in helps
                for name in subcommands(helps[argv])
            ]
    return helps


def ordered(helps: dict[tuple[str, ...], str], argv: tuple[str, ...]) -> list[tuple[str, ...]]:
    """Command paths depth-first, so verbs read under the command they belong to."""
    if argv not in helps:
        return []
    out = [argv]
    for name in subcommands(helps[argv]):
        out.extend(ordered(helps, (*argv, name)))
    return out


def generate() -> str:
    """The full CLI reference page as markdown."""
    lines = [
        "<!-- Generated at build time by scripts/gen_cli_reference.py. Do not edit. -->",
        "",
        "# CLI reference",
        "",
        "Generated from the installed CLI at build time, this page contains each",
        "command's complete `--help` output.",
        "",
        "For what the values *mean* (model aliases, tuning knobs, precedence) see",
        "[Configuration](configuration.md).",
        "",
    ]

    for command, blurb in CLIS:
        helps = collect(command)
        if not helps:
            raise RuntimeError(
                f"could not run `{command} --help`. Install the CLI "
                f"(`pip install -r requirements-docs.txt`) "
                f"and rebuild."
            )

        lines += [f"## `{command}`", "", blurb, ""]
        for argv in ordered(helps, (command,)):
            if len(argv) > 1:
                # Top-level CLI owns the `##` above; verbs nest from `###`.
                lines += ["#" * min(len(argv) + 1, 6) + f" `{' '.join(argv)}`", ""]
            lines += ["```text", strip_noise(helps[argv]), "```", ""]

    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    sys.stdout.write(generate())
