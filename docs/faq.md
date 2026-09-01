# FAQ

## Which MCP server should my agent use? { #which-mcp }

Octo has two, and the choice turns on one question: does the agent need to see
your own Lean code?

**`octo-mcp`** runs on your machine over your project's own indexes. It is the
only one that can find the lemma you wrote this morning, and it searches your
dependencies at the versions your lakefile pins. It needs a key and a few
hundred megabytes per corpus. Its tools are `query`, `status`, and `fetch`.

**Hosted Octo Search** is a URL. Nothing to install, no key, no index to
download, and it searches only public code that has been indexed, so it cannot
see your project. Its tools are `search_lean` and `list_scopes`.

Working in a Lean project, want `octo-mcp`. Answering a Mathlib question from a
scratch directory, on a machine you are not installing anything on, or searching
someone else's public repo, want Octo Search.

Configuring both is reasonable and they do not collide: no tool name appears on
both servers, so an agent holding both always knows which one it called. Give
them distinct names in your client. Watch one asymmetry if you use both — the
`scope` argument is not quite the same vocabulary on each. `everything` means the
same thing deliberately, but `repo:owner/name` is hosted-only and `physlib` and
`cslib` name groups there and single corpora locally. See [Agents and
MCP](agents.md#local-scopes).

## Why can't the agent find a lemma I just wrote? { #agent-cant-see-local }

Most likely it searched the hosted server, which only ever sees public indexed
code, or it searched `octo-mcp` with no local database built yet.

Ask the agent which tool it called. `search_lean` is the hosted server and will
never return your unpublished work, no matter how the query is phrased; switch
to `query` from `octo-mcp`. If it did call `query`, have it run `status`: that
distinguishes "no database installed" from "no matches", and `fetch` installs
one. A local index also lags your working tree, so a lemma written since the
last build is not in it yet — `status` reports uncommitted files for exactly
this reason.

## Why does Octo Search need GitHub access for my repo but not for Mathlib? { #repo-permissions }

Because the two are indexed on different schedules.

Octo indexes two kinds of repository:

**Core dependencies** are core, Batteries, Mathlib, PhysLib, and CSLib.
Axiomatic indexes these itself, once per Lean version, because that is how
projects consume them: a lakefile pins a version. Depend on one and you get the
index for the version you pinned, so there is nothing to grant.

**User repos** are any other Lean repo. These are indexed on every commit
pushed, so results match the code you are working on rather than the last
release. That is what the GitHub App is for. It tells the server you pushed, and
gives it read access to build the index.

Permission is per repository, not per person. Once a maintainer installs the App
on a repo, anyone can search it without signing in, as long as the repo is
public.

The same repo can fall on either side of the line, depending on who is working
on it. Developing PhysLib itself, or a fork of it, makes it a user repo: indexed
per commit, and the App is required. Working *downstream* of PhysLib, on a
project that depends on it, reads the core-dependency index at the version your
lakefile pins, and needs no permission at all.

See [Set up search on your repo](setup-search.md) for the walkthrough, on the
web and in VS Code.
