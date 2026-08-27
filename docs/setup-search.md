# Set up search on your repo

Octo Search needs three things: an Axiomatic API key in this editor, the
repository indexed on the server, and a search database on disk. The setup
checklist in the Octo sidebar tracks all three.

The following assumes the extension is [installed](install.md) and you have opened a Lean
project that lives on GitHub.

## 1. Open the Octo sidebar

<figure markdown="1">
![The setup checklist before sign-in](assets/screenshots/onboarding-01-signed-out.png){ width="370" }
<figcaption>A fresh install: every row open, no databases installed.</figcaption>
</figure>

## 2. Create an account

**Sign in** opens your browser: authorize the app on GitHub, then connect this
editor. Signing up for the first time also asks you to accept the terms and
conditions.

<figure markdown="1">
![Authorizing the Axiomatic app on GitHub](assets/screenshots/onboarding-02-github-authorize.png){ width="470" }
</figure>

<figure markdown="1">
![Connecting VS Code to the Axiomatic account](assets/screenshots/onboarding-03-connect-vscode.png){ width="470" }
<figcaption>Mints an API key for this machine. Revoke it any time from your
account page.</figcaption>
</figure>

## 3. Give Octo Search access to the repository

Indexing runs server-side, so the GitHub App needs read access. Expand **Index
this repository**; each row says what it is waiting for. (Dependencies like
Mathlib ask for nothing: see
[why your repo needs access and Mathlib does not](faq.md#repo-permissions).)

<figure markdown="1">
![The repository rows, waiting on GitHub App access](assets/screenshots/onboarding-04-grant-access.png){ width="520" }
</figure>

**Grant on GitHub** opens the App's install page. Install for all repositories,
or pick just this one. Under an organization, an owner may have to approve it.

<figure markdown="1">
![Installing the Octo Search GitHub App](assets/screenshots/onboarding-05-github-app-install.png){ width="470" }
</figure>

## 4. Indexing starts

GitHub sends you to the dashboard, where the build appears.

<figure markdown="1">
![The dashboard's search tab, with a build running](assets/screenshots/onboarding-06-dashboard.png)
</figure>

Nothing else to do here — the extension polls in the background and enables the
repository itself, so the panel has moved on by the time you switch back.

<figure markdown="1">
![The checklist, with a build in flight](assets/screenshots/onboarding-07-indexing.png){ width="420" }
<figcaption>Take longer than four minutes on GitHub and the row offers
<strong>Check again</strong>: the watch gave up, not the install.</figcaption>
</figure>

## 5. The search databases download themselves

Indexing produces a database on the server; searching reads one from disk. Once
the index is built there is nothing to decide, so the extension starts the
downloads itself and the rows report progress.

<figure markdown="1">
![The database rows, nothing downloaded yet](assets/screenshots/onboarding-08-download-database.png){ width="370" }
<figcaption><strong>Dependencies</strong> is the prebuilt corpora your project
uses; <strong>This project</strong> is your own declarations.</figcaption>
</figure>

Dependency databases are cached per machine, so you pay for Mathlib once. Each
row keeps a **Download** button, which is the retry if one fails.

## 6. Search

When the last database lands, a final row names what you can now search: the
dependency corpora and your own repo. The checklist stays put until you click
**Dismiss** on it.

Then describe what you want, not its name.

<figure markdown="1">
![Search results, filtered by source and kind](assets/screenshots/search-01-results-filtered.png){ width="400" }
<figcaption>Corpus and declaration kind are both filters.</figcaption>
</figure>

<figure markdown="1">
![An expanded search result](assets/screenshots/search-02-result-expanded.png){ width="380" }
<figcaption>The ✦ paragraph is the description Octo embedded and searched
against.</figcaption>
</figure>

<figure markdown="1">
![A result opened in its source file](assets/screenshots/search-03-panel-with-source.png)
<figcaption>Clicking a result opens the declaration in its source file.</figcaption>
</figure>

## If setup does not complete

Run **Octo: Show Output** for the logs; the dashboard's search tab has the full
build log for a failed index.

See the [CLI reference](reference/cli.md) for querying, fetching, and indexing
from the command line.
