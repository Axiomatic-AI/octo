# FAQ

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

See [Give Octo Search access to the repository](setup-search.md#3-give-octo-search-access-to-the-repository)
for the walkthrough.
