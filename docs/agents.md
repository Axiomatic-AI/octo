# Agents and MCP

Octo gives coding agents semantic search over Lean declarations through
**MCP**. There are two servers, and which one you want turns on a single
question: does the agent need to see your own Lean code?

| | `octo-mcp` | Octo Search |
| --- | --- | --- |
| Runs | On your machine, over stdio | Hosted by Axiomatic, over HTTP |
| Tools | `query`, `status`, `fetch` | `search_lean`, `list_scopes` |
| Setup | Ships with the package | A URL, nothing to install |
| Searches | Every corpus installed for your project, **including your own code** | Mathlib, core, Batteries, physlib, cslib, and public repositories indexed by Octo |
| Credentials | Your own key | None |
| Disk | Hundreds of megabytes per corpus | None |
| Versions | Whatever your project pins | Any Lean version we have built |

Reach for **`octo-mcp`** when the agent is working inside a Lean project: it is
the only one that can find the lemma you wrote yesterday, and it searches your
dependencies at the versions your project actually pins.

Reach for **Octo Search** when there is no project to search, or no time to set
one up: answering a Mathlib question from a scratch directory, working on a
machine you will not be installing anything on, or searching a public
repository that is not yours.

Configuring both is reasonable, and they do not collide. Give them distinct
names in your client so the agent can tell which one it is calling.

## `octo-mcp`: your project, on your machine

`octo-mcp` exposes three tools:

| Tool | What it does |
| --- | --- |
| `query` | Semantic search over Lean declarations. Returns ranked hits with each declaration's name, kind, signature, informal description, and location. |
| `status` | Which search databases are installed for a project, how many declarations each holds, and whether a newer one can be fetched. |
| `fetch` | Downloads a prebuilt search database. Can move hundreds of megabytes. |

It speaks MCP over stdio and ships with the package, so any MCP client can
launch it. Only VS Code configures it for you.

### Install per client

=== "VS Code"

    The extension registers the server with the editor's own MCP client, the
    client behind Copilot Chat and agent mode. It publishes one server per Lean
    workspace folder and supplies both the project folder and your Axiomatic
    key, so no manual configuration is required.

    Requires VS Code 1.101 or newer.

    Run **Octo: Show Output** and look for `[mcp] published Octo:` to confirm.

    !!! note "Claude Code inside VS Code is a separate client"

        Claude Code reads its own configuration and never consults the editor's
        MCP registry, so follow the Claude Code tab even when you run it inside
        VS Code.

=== "Claude Code"

    ```bash
    claude mcp add --scope user octo \
      -e OCTO_FOLDER='${CLAUDE_PROJECT_DIR:-.}' \
      -- octo-mcp
    ```

=== "Codex"

    Add to `~/.codex/config.toml`:

    ```toml
    [mcp_servers.octo]
    command = "octo-mcp"
    env = { OCTO_FOLDER = "/path/to/my-lean-project" }
    ```

=== "Cursor"

    Add to `~/.cursor/mcp.json`, or to `.cursor/mcp.json` in your project:

    ```json
    {
      "mcpServers": {
        "octo": {
          "command": "octo-mcp",
          "env": { "OCTO_FOLDER": "/path/to/my-lean-project" }
        }
      }
    }
    ```

Every client except VS Code needs `octo-mcp` on your `PATH`. Installing the
package with `uv tool install axiomatic-octo` puts it there. If you only have the
VS Code extension, run **Octo: Enable terminal / agent access** from the Command
Palette, which links `octo`, `octo-sidecar`, and `octo-mcp` into `~/.local/bin`.

### Which project gets searched

Every tool call resolves a project folder in this order:

1. The call's own `folder` argument.
2. `$OCTO_FOLDER`, which is what the configurations above set.
3. The directory the client launched the server in.

Every result names the folder it used. This matters when you keep several
worktrees of one repository: without `OCTO_FOLDER`, the third rule picks whatever
directory your agent session started in.

### Credentials

`octo-mcp` needs the same credential as the CLI, and reads it from the
environment or from `.env.secrets`. See [Choose how Octo accesses
models](install.md#api-keys).

In VS Code the extension supplies your Axiomatic key to the server it registers.
Everywhere else you set it yourself: signing in through the extension stores the
key in the editor's secret storage, where terminal agents cannot read it. A tool
call with no credential returns an error naming every location Octo searched.

### Scopes { #local-scopes }

A **scope** is what a search runs over. Every scope here is a database on this
machine, so what you can name depends on what has been fetched; `status` reports
that, and missing databases are skipped rather than raising.

| Scope | What it searches |
| --- | --- |
| `both` (default) | The installed corpora this project *depends on*, plus its own local library. |
| `everything`, `all` | Every installed corpus plus the local library, dependency or not. The escape hatch for a corpus this project does not require. |
| `local` | The project's own code only. |
| `mathlib`, `core`, … | That one corpus. Naming a corpus is deliberate, so the dependency filter stays out of it. |
| `mathlib,core,local` | A comma-separated list, optionally including `local`. |

Note that a scope naming a corpus this machine never fetched searches *less*
than you asked for rather than failing, which is why an empty result is worth a
`status` call before you conclude there are no matches.

!!! warning "Not the same vocabulary as Octo Search"

    The hosted server's [scopes](#hosted-scopes) overlap these but are not identical.
    `everything` means the same thing on both, deliberately. But `physlib` and
    `cslib` are single corpora here and *groups* there, and `repo:owner/name` is
    hosted-only: named here it matches no installed database and quietly
    searches nothing.

### The Claude Code skill

Alongside the MCP server, Octo installs a workspace-scoped Claude Code skill.
The two are complementary rather than alternatives:

- The **MCP server** provides the capability, the three tools above.
- The **skill** carries the judgment about using them well: when to reach for
  search, that a hit's `distance` ranks results rather than scoring confidence,
  and the `status` → `fetch` → re-query recovery when a project has no database
  installed.

The skill works through the MCP tools when a client has them and falls back to
the `octo` CLI otherwise, so it is useful whether or not you configured the
server. Octo asks permission separately in each repository before installing it
under `.claude/skills/`.

## Octo Search: the hosted server

The same search that powers the [Octo Search
website](https://octo.axiomatic-ai.com/search) is available to agents as a
remote MCP server. Nothing to install, no key, no index download: it searches
prebuilt corpora that live on our side.

**Server URL:** `https://search.octo.axiomatic-ai.com/mcp/`

It exposes two tools:

| Tool | What it does |
| --- | --- |
| `search_lean` | Semantic search over Lean declarations. Returns ranked hits with each declaration's name, kind, signature, informal description, and a GitHub permalink. |
| `list_scopes` | Every scope `search_lean` accepts and the Lean versions each has been built at. |

### Add it to your client

=== "Claude Code"

    ```bash
    claude mcp add --scope user --transport http octo-search \
      https://search.octo.axiomatic-ai.com/mcp/
    ```

=== "Codex"

    Add to `~/.codex/config.toml`:

    ```toml
    [mcp_servers.octo_search]
    url = "https://search.octo.axiomatic-ai.com/mcp/"
    ```

=== "VS Code"

    Add to `.vscode/mcp.json` in your project, or to your user `mcp.json`:

    ```json
    {
      "servers": {
        "octo-search": {
          "type": "http",
          "url": "https://search.octo.axiomatic-ai.com/mcp/"
        }
      }
    }
    ```

    Requires VS Code 1.101 or newer. Unlike `octo-mcp`, the extension does not
    register this one for you: it is not tied to a workspace folder.

=== "Cursor"

    Add to `~/.cursor/mcp.json`, or to `.cursor/mcp.json` in your project:

    ```json
    {
      "mcpServers": {
        "octo-search": {
          "url": "https://search.octo.axiomatic-ai.com/mcp/"
        }
      }
    }
    ```

### Scopes { #hosted-scopes }

A **scope** is what a search runs over. Naming none searches Lean core,
Batteries and Mathlib together, which is the right default for most questions.

| Scope | What it is |
| --- | --- |
| `core`, `batteries`, `mathlib` | One corpus each. Searched together when you name no scope. |
| `physlib`, `cslib` | A group: several corpora searched as one. |
| `repo:owner/name` | A public repository indexed by Octo, plus the corpora it builds against, so a search of one project still finds the Mathlib lemma it depends on. |
| `everything` | Every corpus and every indexed public repository at once. |

These are the hosted server's scopes. `octo-mcp` accepts [its own
set](#local-scopes), which shares `everything` but not `repo:owner/name`, and treats
`physlib` and `cslib` as single corpora rather than groups.

`list_scopes` reports the live list along with the Lean versions each scope has
been built at, which is worth calling before pinning a `version`: asking for a
version nobody built falls back to the nearest older one, and the result says
which was actually served.

### What to expect

**Search by meaning, not by name.** The index is built from each declaration's
statement together with an AI-written description of it, so "continuous
function attains its maximum on a compact set" finds the lemma whose name you
could not have guessed. A guessed identifier is the weakest query you can send.

**Reranking is on by default** and adds a few seconds per search. Turn it off
with `rerank: false` when the agent is issuing many exploratory queries and
cares more about latency than about the exact ordering.

**Informal descriptions are AI-generated.** They are written at index time, not
by the declaration's author. Good for matching intent, not quotable as
documentation. Every hit carries a GitHub permalink to the real source.

**Only public code.** Repositories appear here only when their owner enabled
indexing and the repository is public. Your own unpublished work is never in
this index, which is the reason `octo-mcp` exists.

### Limits

Access is anonymous, so it is rate limited rather than metered: a per-caller
hourly allowance, and a daily ceiling shared by everyone. An agent that hits
either gets a tool error saying "limit reached" and, for the daily one, that it
resets at 00:00 UTC. Neither is a failure to retry through. If you need volume
beyond that, run `octo-mcp` against your own indexes instead.
