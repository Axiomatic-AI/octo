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

Axiomatic Octo is a Swiss Army knife for Lean formalization workflows. It
currently supports semantic search across local projects and commonly used
libraries, including Mathlib, Batteries, CSLib, and Physlib, through a VS Code
extension and Python CLI. Planned capabilities include additional
theorem-proving and knowledge-management tools.

- [Website](https://octo.axiomatic-ai.com/)
- [Browser-based corpus search](https://octo.axiomatic-ai.com/search)
- [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=AxiomaticAI.axiomatic-octo)
- [User manual](https://axiomatic-ai.github.io/octo/)

## Install

### VS Code

Install [Axiomatic Octo from the VS Code
Marketplace](https://marketplace.visualstudio.com/items?itemName=AxiomaticAI.axiomatic-octo),
then open a Lean project. The extension completes setup on first activation.

Hosted project indexing requires a GitHub repository. The extension identifies
the repository from its Git `origin` remote. SSH host aliases are supported when
the remote path uses the standard `owner/repository` format.

### CLI

```bash
uv tool install axiomatic-octo
```

To build a search index, install the optional dependencies:

```bash
uv tool install 'axiomatic-octo[build-search-index]'
```

## Quickstart

Search without an account or API key:

```bash
cd my-lean-project
octo search fetch
octo search query "self-adjoint operator is symmetric"
```

`octo search fetch` anonymously downloads the shared corpora, subject to a
global limit of 1,000 anonymous downloads per day. It also downloads the
project's `local.db` when the repository is registered for search and its owner
has installed the Axiomatic search GitHub App.

`octo search query` embeds queries through the Axiomatic server. Anonymous use
is limited to 60 queries per IP address within a rolling one-hour window. To use
your own provider account, set `OPENROUTER_API_KEY` in the environment or in a
project-root `.env.secrets` file. An Axiomatic API key (`OCTO_SERVER_TOKEN`)
enables reranking, private repository access, index creation, and account-level
rate limits.

Use `octo search status` to check installed databases and available updates. Use
`octo search index` to create a local index after installing the optional
dependencies.

Axiomatic hosts project databases by default. Repositories that build a
`search-lean-db` workflow artifact can set `search_lean.db_source` to `workflow`
to use that artifact instead. This setting applies only to the project database;
shared corpora continue to come from the Axiomatic server. Octo does not fall
back to an alternate source.

## Agents

Octo integrates with coding agents through two complementary components: an
**MCP server** provides search capabilities, and a **skill** provides guidance
on when and how to use them.

Choose the MCP server based on whether the agent needs access to local Lean code.

### Local project search

`octo-mcp` communicates over stdio and exposes `query`, `status`, and `fetch`.
It searches local code and dependencies at the versions pinned by the project.
The VS Code extension registers it with the editor's MCP client automatically.
Other clients, including Claude Code within VS Code, require configuration:

```bash
claude mcp add --scope user octo -e OCTO_FOLDER='${CLAUDE_PROJECT_DIR:-.}' -- octo-mcp
```

### Hosted corpus search

Hosted Octo Search exposes `search_lean` and `list_scopes` over HTTP at
`https://search.octo.axiomatic-ai.com/mcp/`. It searches prebuilt public
corpora without requiring installation, credentials, or a local index. It
cannot access local or unpublished code.

```bash
claude mcp add --scope user --transport http octo-search https://search.octo.axiomatic-ai.com/mcp/
```

Both servers can be configured because their tool names do not conflict. See
[Agents and MCP](https://axiomatic-ai.github.io/octo/agents/) for client-specific
configuration, project selection, scopes, and credentials.

The extension installs the workspace-scoped Claude Code skill after terminal
and agent access is enabled. It can also be installed with **Octo: Enable
terminal / agent access** from the Command Palette. The skill uses MCP tools
when available and otherwise uses the CLI. Octo requests permission before
installing the skill under `.claude/skills/` and can add
`.claude/skills/octo*` to `.gitignore`.

## Building the manual

The manual uses MkDocs Material. Its CLI reference is generated from the
installed CLI's `--help` output, so `octo` must be on `PATH`:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

## License

AGPL-3.0-only. See [LICENSE](LICENSE).
