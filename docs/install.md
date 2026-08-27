# Install Axiomatic Octo

## VS Code (recommended)

1. [Install Axiomatic Octo from the VS Code
   Marketplace](https://marketplace.visualstudio.com/items?itemName=AxiomaticAI.axiomatic-octo).
2. Open a **Lean project folder** in VS Code.
3. Open the Octo sidebar and follow the setup checklist.
4. Search your project and its dependencies from the Octo Search panel.

On first activation, the extension installs the Octo runtime and guides you
through setup. See [Set up search on your repo](setup-search.md) for a
screenshot-by-screenshot walkthrough.

### Terminal and agent access

The extension can also expose the `octo` CLI and install a workspace-scoped
Claude Code skill. After setup, accept the prompt or run **Octo: Enable terminal
/ agent access** from the Command Palette.

Octo asks for permission separately in each repository before installing the
skill under `.claude/skills/`.

### Check the installation

Open the Octo sidebar and run a search. If setup does not complete:

- Run **Octo: Retry setup** from the Command Palette.
- Run **Octo: Show Output** to see the setup and sidecar logs.

## CLI only

Install the package as a command-line tool with
[`uv`](https://docs.astral.sh/uv/):

```bash
uv tool install axiomatic-octo
```

This installs `octo` and `octo-sidecar` on your `PATH`. Verify the installation:

```bash
octo --help
octo search --help
```

### Choose how Octo accesses models { #api-keys }

Fetching and querying need no key at all. `octo search fetch` downloads the
shared corpora anonymously, under a global ceiling of 1,000 anonymous downloads
per day, and query embeddings go through the Axiomatic server at 60 anonymous
queries per hour per IP address (a rolling window, not a daily allowance).

Reranking, private repositories, building your own index, and rate limits of
your own are what the credentials below are for.

=== "Axiomatic account (easiest setup)"

    Route query embeddings and reranking through the Axiomatic server by
    setting your Axiomatic API key:

    ```bash
    export OCTO_SERVER_TOKEN=...
    ```

    Reranking is the visible difference: without a credential the query
    returns vector-ranked results and says so. The same token authorizes
    search databases for your private repositories, lifts the shared anonymous
    rate limits, and is required to build an index of your own.

    The VS Code extension supplies this credential automatically after you
    sign in.

=== "OpenRouter API key"

    Send query embeddings and reranking directly to OpenRouter by setting your
    own key:

    ```bash
    export OPENROUTER_API_KEY=...
    ```

    You can instead store the key in `.env.secrets` at the root of your Lean
    project:

    ```bash
    # .env.secrets
    OPENROUTER_API_KEY=...
    ```

Add `.env.secrets` to `.gitignore`; never commit API keys.

#### Other credentials { #optional-keys }

Building a local index may require additional provider keys if you override
the default models. See [Configuration](reference/configuration.md).

### Try Octo Search

From a Lean project:

```bash
cd my-lean-project
octo search fetch
octo search query "self-adjoint operator is symmetric"
```

Use `octo search status` to see which project and dependency databases are
installed and whether updates are available.

### Build a local search index

Querying and fetching use the standard installation. To build a search index
yourself, install the optional indexing dependencies:

```bash
uv tool install 'axiomatic-octo[build-search-index]'
```

Then run `octo search index` from your Lean project. Indexing can make many
model-provider calls, so run `octo search index --dry-run` to estimate the cost
before starting a large build.

## Next

[:octicons-arrow-right-24: Set up search on your repo](setup-search.md)
