"""Build the CLI reference page from live `--help` output.

The `hooks` entry in mkdocs.yml loads this module. It adds the generated page to
MkDocs in memory rather than writing it to disk.

Requires `octo` on PATH. Install it with `pip install -r requirements-docs.txt`.
"""

from __future__ import annotations

import sys
from pathlib import Path

from mkdocs.structure.files import File

sys.path.insert(0, str(Path(__file__).parent))

from gen_cli_reference import generate  # noqa: E402  (needs the sys.path line above)

PAGE_URI = "reference/cli.md"

# Cache the `--help` calls during `mkdocs serve`. Restart after changing a
# parser.
_cache: str | None = None


def on_files(files, config):
    """Add the generated reference to the file collection."""
    global _cache
    if _cache is None:
        _cache = generate()
    files.append(File.generated(config, PAGE_URI, content=_cache))
    return files
