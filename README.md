<p align="center">
  <img src="docs/assets/octo_search.svg" alt="Axiomatic Octo logo" width="180">
</p>

<h1 align="center">Axiomatic Octo</h1>

<p align="center">
  <a href="https://octo.axiomatic-ai.com/"><img src="https://img.shields.io/badge/octo.axiomatic--ai.com-website-111111" alt="Website"></a>
  <a href="https://axiomatic-ai.github.io/octo/"><img src="https://img.shields.io/badge/docs-manual-2563A6" alt="Manual"></a>
  <a href="https://marketplace.visualstudio.com/items?itemName=AxiomaticAI.axiomatic-octo"><img src="https://img.shields.io/visual-studio-marketplace/v/AxiomaticAI.axiomatic-octo?label=VS%20Code" alt="VS Code Marketplace"></a>
  <a href="https://pypi.org/project/axiomatic-octo/"><img src="https://img.shields.io/pypi/v/axiomatic-octo" alt="PyPI version"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB" alt="Python 3.11+">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-AGPL--3.0-2563A6" alt="License: AGPL-3.0"></a>
</p>

Axiomatic Octo is a swiss army knife for Lean (auto)formalization workflows.
Today, it provides semantic search over your own projects and common dependencies
such as Mathlib, Batteries, CSLib, and Physlib through a VS Code extension and
Python CLI. The roadmap includes broader theorem-proving and knowledge-management
tools.

- [octo.axiomatic-ai.com](https://octo.axiomatic-ai.com/) is the Octo website.
- [Search the corpora in your browser](https://octo.axiomatic-ai.com/search) with
  no install: Mathlib, core, Batteries, and friends.
- [Axiomatic Octo on the VS Code
  Marketplace](https://marketplace.visualstudio.com/items?itemName=AxiomaticAI.axiomatic-octo).
- This repository hosts the [user
  manual](https://axiomatic-ai.github.io/octo/).

## Install

**VS Code (recommended):** install [Axiomatic Octo from the
Marketplace](https://marketplace.visualstudio.com/items?itemName=AxiomaticAI.axiomatic-octo)
and open a Lean project. The extension completes setup on first activation.

Hosted project indexing requires a GitHub repository. The extension identifies
it from the Git `origin` remote and supports SSH host aliases when the remote
path uses the standard `owner/repository` form.

**CLI only:**

```bash
uv tool install axiomatic-octo
```

To build your own search index, install the optional dependencies:

```bash
uv tool install 'axiomatic-octo[build-search-index]'
```

## Quickstart

No account, no keys:

```bash
cd my-lean-project
octo search fetch
octo search query "self-adjoint operator is symmetric"
```

`octo search fetch` downloads the shared corpora (mathlib and friends)
anonymously, under a global ceiling of 1,000 anonymous downloads per day. It
fetches this project's own `local.db` too, if the repository is registered for
search and the Axiomatic search GitHub App is installed for its owner; without
that there is nothing published for the project itself to download.

`octo search query` embeds the query through the Axiomatic server, which serves
60 anonymous queries per hour per IP address. That is a rolling window, not a
daily allowance. Set `OPENROUTER_API_KEY` in your environment or a project-root
`.env.secrets` file to spend your own provider key instead. An Axiomatic API key
(`OCTO_SERVER_TOKEN`) is what buys reranking, private repositories, building your
own index, and rate limits of your own.

Use `octo search status` to check installed databases and updates. Local index
creation is available through `octo search index` when the optional dependencies
are installed.

Axiomatic hosts project databases by default. Repositories that already build a
`search-lean-db` workflow artifact can set `search_lean.db_source` to
`workflow` to use their own instead. That setting covers this project's own
database; the shared corpora still come from the Axiomatic server either way.
Octo uses only the selected source for each and does not fall back.

## Agents

Octo includes a workspace-scoped Claude Code skill that lets agents search Lean
declarations through the CLI. After the VS Code extension starts successfully,
enable terminal and agent access when prompted. You can also run
**Octo: Enable terminal / agent access** from the Command Palette. The extension
installs the skill under `.claude/skills/`, offers to add
`.claude/skills/octo*` to `.gitignore`, and keeps the skill synchronized when
Octo updates.

## Building the manual

The manual is MkDocs Material. Its CLI reference page is generated at build time
from the installed CLI's `--help` output, so `octo` has to be on `PATH`:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

## License

AGPL-3.0-only. See [LICENSE](LICENSE).
