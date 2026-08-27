# Configuration

Commands read models and tuning options from one merged configuration.

## Precedence

Layered **lowest priority first**:

1. Built-in defaults (`SearchLeanConfig` dataclass)
2. Bundled `configs/default.yaml` + its `configs/llms.yaml` import
3. `<folder>/.axiomatic/config.yaml`, the auto-discovered per-project config —
   its **`search_lean:` subtree**. Other Axiomatic tools read the same file,
   so one project config can serve all of them
4. `-c/--config <file.yaml>`, repeatable, passed **before** the verb
5. `--overrides KEY=VALUE` dot-notation overrides, also **before** the verb

```bash
octo search -c experiment.yaml index
octo search --overrides embed_batch_size=32 index
```

Config files and overrides use **top-level** keys (`informalize_llm`,
`embed_batch_size`, ...). Only the per-project `.axiomatic/config.yaml` nests
them under `search_lean:`, because that file is shared with other Axiomatic tools:

```yaml
# <project>/.axiomatic/config.yaml
search_lean:
  informalize_llm: ${llm_configs.claude_opus_5}
  informalize_concurrency: 16
```

Model references use OmegaConf interpolation against `configs/llms.yaml`.

## Model aliases

`configs/llms.yaml` defines aliases such as `${llm_configs.<name>}`. Each alias
includes a model id and provider settings such as thinking mode and token caps.

| Alias | Model |
| --- | --- |
| `claude_opus_5` | `anthropic:claude-opus-5` |
| `claude_sonnet_5` | `anthropic:claude-sonnet-5` |
| `claude_opus_4_8` | `anthropic:claude-opus-4-8` |
| `claude_opus_4_7` | `anthropic:claude-opus-4-7` |
| `claude_opus_4_6` | `anthropic:claude-opus-4-6` |
| `claude_opus_4_5` | `anthropic:claude-opus-4-5` |
| `claude_sonnet_4_6` | `anthropic:claude-sonnet-4-6` |
| `claude_sonnet_4_5` | `anthropic:claude-sonnet-4-5` |
| `claude_haiku_4_5` | `anthropic:claude-haiku-4-5-20251001` |
| `gemini_3_pro` | `google_genai:gemini-3-pro-preview` |
| `gemini_3_flash` | `google_genai:gemini-3-flash-preview` |
| `gpt_5_2` | `openai:gpt-5.2` |
| `gpt_5_nano` | `openai:gpt-5-nano` |

Non-Anthropic aliases need the corresponding
[optional API key](../install.md#optional-keys).

To keep an alias's settings but change its model id, use an inline override:
`--overrides informalize_llm.model=anthropic:claude-opus-5`.

---

## Keys

| Key | Default | Effect |
| --- | --- | --- |
| `informalize_llm` | `${llm_configs.claude_sonnet_5}` | Writes natural-language declaration descriptions during `index` |
| `embedding.provider` | `mistral` | Embedding provider |
| `embedding.model` | `mistral-embed` | Embedding model |
| `embedding.dim` | `1024` | Vector dimension |
| `embed_batch_size` | `64` | Embeddings per API call |
| `embed_max_retries` | `5` | Retries on embedding failures |
| `informalize_concurrency` | `32` | Parallel informalization calls |
| `informalize_max_retries` | `5` | Retries on informalization failures |
| `insert_batch_size` | `1000` | Rows per DB insert batch |
| `default_top_k` | `20` | Default result count |
| `server_token` | *none* | ax-prover-server API key for private-repo DB fetches. `OCTO_SERVER_TOKEN` takes precedence |
| `db_source` | `hosted` | Where this project's database comes from: `hosted` or `workflow` |
| `corpus_release_repo` | *none* | `owner/repo` publishing corpus databases as `searchdb-<target>-<version>` releases. Only used under `db_source: workflow`; unset, corpora come from the search server |

!!! danger "`embedding.dim` is fixed at creation time"
    Search databases with different dimensions require a full rebuild.

!!! note "`db_source` governs your project's database, not the corpora"
    `db_source: workflow` takes *your* `local.db` from your repo's CI
    artifacts. The shared corpora (mathlib, core, …) keep coming from the
    search server, because it publishes them for everyone and building them
    yourself is a large job you have not asked for.

    Setting `corpus_release_repo` is what opts corpora out of that: under
    `db_source: workflow` it reads them from the named repo's
    `searchdb-<target>-<version>` releases instead. Only do that if you build
    and publish your own corpus databases. There is no default, so no
    configuration ever probes a repo you did not name.

API keys are **not** part of this tree. They live in `.env.secrets` files and
shell environment variables. See [Install](../install.md#api-keys).
