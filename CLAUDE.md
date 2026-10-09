# CLAUDE.md

This file is both a **one-time setup trigger** and **ongoing documentation** for a project
scaffolded from https://github.com/erikrikarddaniel/dltemplates. It is meant to be the only
file a new project starts with — copy just this file into an empty directory (no `git clone`
required) and start a Claude Code session there.

## Communication style

The students using this template are often new to R and the command line — be direct and
concise, not verbose.

- Answer the question, then stop. Skip preamble ("Great question!", "I'd be happy to
  help..."), skip recaps of what was just asked, skip restating the plan before doing it.
- Avoid AI-assistant stock phrases: "Let's dive into...", "It's worth noting that...",
  "leverage", "seamless", "robust solution", "comprehensive", "ensure that". Say the plain
  thing instead.
- No unearned enthusiasm or hedging. State what's true, what changed, what to do next.
- Short sentences. One idea per sentence. Match response length to the question — a
  one-line answer doesn't need three paragraphs of framing around it.

## Code comments

- Default to no comment. Code shows *how*; comment only to carry *why* — a non-obvious
  constraint, deliberate deviation, gotcha, or workaround.
- Never narrate the code ("loop over users", "parse the body"), restate names/types/
  signatures, or mark block ends.
- Never narrate the change ("fixed X", "updated to Y", "as requested"). A comment must
  read correctly to someone seeing the file fresh who never saw the diff; change context
  belongs in the commit message.
- Delete by default. A comment that just restates a decision the code already reflects —
  "1 vCPU is deliberate", "right-sized from prod" — is dead weight even when it points to
  a doc: the doc is where anyone questioning it looks anyway. Keep inline only what a
  reader needs *at that line* and can't get from the code — a non-obvious invariant/
  constraint ("timeout must stay < interval — ALB rule") or a cross-file sync obligation
  ("keep in sync with the router's TGs").
- Comments must stand on their own with any link removed — encode the substance, never a
  pointer as a substitute for it. Banned: specs, section numbers, design docs —
  point-in-time artifacts that get superseded and rot ("spec §7" is the canonical case).
  Fine: a maintained doc/README at a stable path — and when the *why* is a system-level
  narrative ("why it's built this way"), extract it there as a *pure* extraction: not an
  inline block, and not a comment that merely points to the doc. What stays inline are the
  non-obvious local details, which reference the doc only when a reader genuinely needs it
  *at that line* — a pointer-only comment generally shouldn't exist at all. Tickets,
  Confluence, RFCs, permalinks stay fine as trailing breadcrumbs.
- Occam's razor on every comment you *keep*, not just the ones you delete. "Carries a real
  *why*" and "is worded minimally" are independent judgments — a genuine *why* can still be
  3x too long, and "it's a real why" is not license to keep the wording verbatim. Keep only
  the one non-obvious fact a reader needs *at that line*, in the fewest words; cut the
  mechanism the code already shows, where a value is consumed downstream, the
  consequence-of-the-consequence, and justification-of-the-justification. A 5-line block
  almost never survives intact — suspect it on sight; the razored answer is sometimes zero.
- A one-line summary on a public function/endpoint is fine; inline restatement of a single
  clear line never is.
- TODOs are fine and don't need issue IDs — but a TODO is a marker, not a substitute for
  doing the work in scope.

## If the project structure below doesn't exist yet

Check the current directory for `data/`, `scripts/`, `figures/`, `Makefile`, and a `*.Rproj`
file. If any of them are missing, this project hasn't been scaffolded yet — do the following
before anything else, and before addressing whatever the user actually asked for:

1. If the current directory's name looks generic (e.g. `untitled`, `new folder`, `test`),
   ask the user first whether to rename the folder before continuing — its name becomes the
   project name, used for the `.screenrc` session name and the `.qmd` report filename.
2. `git clone --depth 1 https://github.com/erikrikarddaniel/dltemplates <tmpdir>` into a
   scratch/temp directory — never inside the project directory itself, and this clone's own
   `.git` history must not end up in the project.
3. From inside the project directory (the one containing this `CLAUDE.md`), run
   `<tmpdir>/setup_project.sh` with **no argument**. It detects that the directory already
   exists, uses its basename as the project name, and builds the full structure in place —
   see "Project structure" below for exactly what it creates. (Use the absolute path to the
   script; running it via a relative path after the temp clone could break once the script's
   own `cd` changes the working directory.)
4. Delete the temporary clone.
5. Tell the user what was created and that they can open `project.Rproj` in RStudio or start
   editing `scripts/`.

`setup_project.sh` itself does the `git init .` / `git add .` (this `CLAUDE.md` gets committed
along with everything else) and deliberately does not create a commit — leave that for the
user's first commit.

If the structure already exists, skip all of the above — this file is now just documentation.

## Project structure

- `data/` — raw/intermediate data, built via `data/Makefile`. Nothing here is meant to be
  edited by hand; it's regenerated by rules you add to `data/Makefile`.
- `scripts/` — analysis/processing scripts. Includes `convert_to_parquet.R` by default, a
  generic TSV(.gz)-to-Parquet converter for pipeline output that doesn't already ship
  Parquet copies — see "Fetching pipeline output into `data/`" below.
- `figures/` — generated plots (`*.png`, `*.pdf` are gitignored — figures are build products,
  not source).
- `docs/` — general project documentation: free-form notes, protocols, write-ups — anything
  that isn't the `.qmd` report itself or code. Not tied to Quarto rendering or GitHub Pages,
  just a place to keep documentation out of the project root.
- `Makefile` (root) — currently just delegates to `data/Makefile` (`cd data; make all`).
  Extend it as the project grows.
- `project.Rproj` — RStudio project file (`BuildType: Makefile`), so RStudio's Build pane
  runs the root `Makefile`. Remind students to always open the project via this file (not
  by opening individual scripts/documents directly) — that's what puts R's working
  directory at the project root. `setwd()` and absolute paths in R scripts or `.qmd` files
  should never be needed and shouldn't be added; they break as soon as the project moves or
  someone else clones it, defeating the point of committing the `.Rproj` file at all.
- `CLAUDE.md` (this file) — copied in by `setup_project.sh` itself, same as `project.Rproj`
  or `tools.bib` below, so every project scaffolded this way carries its own copy of this
  documentation, not just ones bootstrapped from a student's pre-seeded copy.
- `.screenrc` — a GNU screen layout with windows for `rstudio`, `data`, `scripts`, `man`,
  and `root`, opened automatically in the right directory. Run `screen` in the project root
  to use it (optional — nothing else depends on it).
- `.gitignore` — tuned for bioinformatics projects: keeps large/raw sequence and alignment
  files (`*.fastq*`, `*.fna`, `*.gz`, `*.dmnd`, etc.) out of git.
- `tools.bib` — a shared BibTeX library of tool/database citations, copied in from
  dltemplates. Add citations for tools/databases you use to your project's `bibliography.bib`
  instead of editing this file, unless the citation is generic enough to be useful in other
  projects too.
- `bibliography.bib` — project-specific references. Starts empty.
- `grateful-refs.bib` — **not** created by setup; the `grateful` R package generates this
  automatically (via `cite_packages()`) the first time the `.qmd` report is rendered, listing
  exact versions of R packages used.
- `<project-name>.qmd` — a Quarto report with a fixed section skeleton (Version history,
  Summary, Introduction, Materials and Methods, Results, Discussion, References) and a
  packages-used table. All three `.bib` files above are wired into its bibliography.

## Setting up a GitHub remote

`setup_project.sh` only runs `git init` locally — the project isn't backed up or shareable
until it has a remote. Help the student with this once the local scaffold exists:

1. Check whether they already have a GitHub account. If not, they need to create one
   manually at https://github.com/join — sign-up needs email verification, so nothing here
   can be done on their behalf.
2. Create a **private** repository for the project. Prefer whichever of these actually
   works in the student's environment:
   - If the `gh` CLI is installed and already authenticated (`gh auth status`), it can be
     created directly: `gh repo create <name> --private --source=. --remote=origin --push`.
     Confirm the repo name and that private is what they want *before* running it — this
     publishes something to their GitHub account, so don't run it unprompted.
   - Otherwise, walk them through the web UI: log in, go to https://github.com/new, enter a
     name (the project directory's name is a good default), select **Private**, and leave
     "Initialize this repository with a README/.gitignore/license" unchecked — the local
     project already has these, and initializing remotely would create a repo history that
     conflicts with the one already committed locally. GitHub shows a remote URL afterward.
3. If step 2 didn't already do it via `--remote=origin`, add that URL as a remote:
   ```
   git remote add origin <url-from-github>
   ```
   (`git remote set-url origin <url>` instead, if `origin` is already set to something else)
4. Push and set upstream tracking — check the local default branch name first
   (`git branch --show-current`, likely `master` or `main`) rather than assuming one:
   ```
   git push -u origin <branch-name>
   ```
   Confirm with the student before this first push, same as any other push.

### Authentication

Plain HTTPS with a username and password no longer works for `git push` — GitHub removed
that in 2021, so an unprepared HTTPS remote just fails with a confusing error rather than
prompting cleanly. Two ways around it, in order of preference:

- **`gh auth login`**, if the `gh` CLI is present (step 2's first option already relies on
  this). It's a browser-based device-code login that configures git's credential helper
  automatically — no keys to generate, no tokens to copy anywhere. Least setup when it's
  available.
- **SSH keys**, otherwise. Conceptually the same thing the student is already learning for
  the cluster fetch alias above — an SSH keypair, just registered to their own GitHub
  account this time instead of a shared cluster login. Treat the keypair as belonging to
  the *student*, not the machine: one keypair, reused on every computer they work from, is
  the convention here — not a fresh one per machine.
  1. Check for an existing key first — on this machine, and on any other machine the
     student already uses (their own laptop, a department computer, etc.):
     `ls ~/.ssh/id_ed25519.pub`. If one exists anywhere already, copy that same private and
     public key file over to the new machine (a USB drive, or `scp` between two machines
     the student already has access to — never by email or pasted into chat, since the
     private key is as sensitive as a password) rather than generating a second keypair.
     Skip to step 3 once the key is in place.
  2. Only if no key exists anywhere yet, generate one: `ssh-keygen -t ed25519 -C "<their
     email>"`. Accepting the default file location is fine. Use a real, good passphrase —
     that's the recommendation here, not the empty-passphrase shortcut, precisely because
     this one key ends up trusted everywhere (GitHub, and potentially the cluster too), so
     it's worth protecting well:
     - Avoiding having to re-enter the passphrase on every push depends on `ssh-agent`,
       which behaves differently per OS:
       - **macOS**: an agent already runs, but forgets keys after a reboot by default. Add
         `UseKeychain yes` and `AddKeysToAgent yes` to `~/.ssh/config`, then run
         `ssh-add --apple-use-keychain ~/.ssh/id_ed25519` once — after that it persists via
         the system Keychain.
       - **Linux**: most desktop environments auto-start an agent tied to the login
         keyring (prompts once at login, remembers afterward). On a headless machine or a
         minimal window manager there's no agent unless started manually, each session:
         `eval "$(ssh-agent -s)"` then `ssh-add ~/.ssh/id_ed25519`.
       - **Windows**: the built-in "OpenSSH Authentication Agent" service is disabled by
         default — enable it once from an elevated PowerShell:
         `Set-Service ssh-agent -StartupType Automatic; Start-Service ssh-agent`. Git Bash
         also bundles its own, separate agent; if a push keeps re-asking for the
         passphrase, that's usually two agents not sharing state, not a broken key.
     - Regardless of OS, `ssh-add -l` shows what's currently loaded and `ssh-add
       ~/.ssh/id_ed25519` (re-)loads it — the one command that's the same everywhere, worth
       reaching for whenever a push unexpectedly asks for the passphrase again.
     - An empty passphrase sidesteps all of the above and works identically on every OS —
       mention it as an option that exists, but it's not the default taught here, precisely
       because it leaves the key file alone as the only thing protecting access.
  3. `cat ~/.ssh/id_ed25519.pub` and have them paste the output into GitHub → Settings →
     SSH and GPG keys → New SSH key.
  4. Verify with `ssh -T git@github.com` — it should greet them by GitHub username, not
     ask for a password.
  5. Use the SSH form of the remote URL, `git@github.com:<user>/<repo>.git` (both the web
     UI and `gh repo create` offer this alongside the HTTPS one).

Avoid a manually-pasted Personal Access Token unless neither of the above is available —
tokens expire and need scopes configured, which is more to explain than either option here.

## Chatting with Claude inside RStudio (`chattr`)

Optional, but worth setting up — [`chattr`](https://mlverse.github.io/chattr/) adds a chat
pane to RStudio (and Positron) that talks to an LLM, including Claude, without leaving the
IDE. It's built on `ellmer`, Posit's general R-to-LLM package, which it pulls in as a
dependency.

1. Install: `install.packages("chattr")` (and `install.packages("usethis")` too, if not
   already present — used in the next steps).
2. Get an Anthropic API key from https://console.anthropic.com. This is separate from a
   claude.ai subscription and needs its own billing set up (pay-as-you-go credits), unless
   using a shared/institutional key someone else is providing. Whether each student gets
   their own key or the class shares one is a course-logistics decision, not a technical
   one — worth settling ahead of time rather than per-student.
3. Store the key as an environment variable rather than pasting it into a script:
   `usethis::edit_r_environ()` opens `.Renviron` for editing; add a line
   `ANTHROPIC_API_KEY=sk-ant-...`, save, and restart R for it to take effect.
4. Tell `chattr` to default to Claude: add `options(.chattr_chat = ellmer::chat_anthropic())`
   to `.Rprofile` (open it with `usethis::edit_r_profile()`), so it's set every session
   instead of needing to be typed each time.
5. Open the chat pane via Tools → Addins → Browse Addins → "Open Chat", or bind it to a
   keyboard shortcut from that same Addins browser for quicker access.

### Does this work on RStudio Server (a remote machine)?

Yes, and for a simple reason: authentication here is just an API key sent as an HTTP
header directly from the R process to Anthropic's servers — there's no browser-based OAuth
redirect step involved (unlike, say, `gh auth login`), so it doesn't matter whether R is
running locally or on a remote server. Two things that *do* matter:

- The `.Renviron` edited in step 3 has to be the one on whichever machine actually runs the
  R process. On RStudio Server that's the server's own home directory, edited from inside
  that server-hosted RStudio session — not the student's laptop, which the server-side R
  session never sees.
- The server needs outbound network access to `api.anthropic.com`. Most machines have this
  by default, but an HPC cluster or an institutionally locked-down server sometimes doesn't
  — worth checking with whoever administers it if the chat pane can't connect.

## Fetching pipeline output into `data/`

The raw material for these projects is normally the output of an nf-core annotation
pipeline — `ampliseq`, `metatdenovo`, or `magmap` — run elsewhere, usually on an HPC
cluster, never inside this repo. That output is far too large to commit, so it's fetched
into `data/` on demand via `data/Makefile`, which RStudio's Build pane already runs (via
`project.Rproj`'s `BuildType: Makefile` and the root `Makefile`'s `cd data; make all`).

When a student wants this wired up and it isn't yet (`data/Makefile` still just says
`all:`), help them fill it in:

1. Ask which pipeline produced the data, if not already clear, for the absolute path to
   that run's output directory (`<outdir>`, conventionally named `results`), and whether
   that path is on **this same machine** or a **remote** one (e.g. an HPC cluster) — this
   decides the fetch mechanism in step 3 below. Also ask whether they have a sample table
   (treatment, site, time of year, or whatever else distinguishes their samples) — none of
   these pipelines produce one themselves, but it's needed to colour/shape the NMDS plot in
   the sanity check (see below). If they have one, copy it to `data/sample_table.tsv`.
2. Only a subset of files in each source directory actually matters, so filter rather
   than fetching everything — which files depends on the pipeline:
   - `ampliseq` → the `*.tsv` files in `<outdir>/dada2`
   - `metatdenovo` or `magmap` → the `*.tsv.gz` files in `<outdir>/summary_tables`
   - all three, in addition → `<outdir>/pipeline_info/*versions*.yml`.
     Don't narrow this to `*software_versions*.yml`.
     The exact filename order isn't consistent across pipelines — confirmed
     `nf_core_metatdenovo_software_mqc_versions.yml` on a real metatdenovo run
     (2026-09-10), where "mqc" sits between "software" and "versions" and a
     `*software_versions*` glob matches nothing.
     `*versions*.yml` matches that and any other ordering.
   Also check whether the run has Parquet copies of the summary tables alongside the
   TSVs — support is new and differs across these three pipelines (checked 2026-09), so
   don't assume from the pipeline name alone:
   - `magmap` (v1.2.0+, 2026-08-11): opt-in via `--save_parquet`; when used, every
     `summary_tables/*.tsv.gz` file gets a same-named `*.parquet` sibling.
   - `ampliseq`: Parquet support (`summary_tables/ampliseq.counts.parquet`, on by default,
     opt-out via `--skip_parquet_summary`) exists only on the `dev` branch so far — not yet
     in a release, so no run made with a released version will have it.
   - `metatdenovo`: not implemented yet (tracked as nf-core/metatdenovo#473) — no run will
     have Parquet output.
   The reliable check is the run's actual output directory, not the pipeline/version in
   the abstract: `ssh <alias> "ls <outdir>/summary_tables/*.parquet 2>/dev/null"` (use the
   `dada2` subdirectory instead for `ampliseq`). If you can't check yet — e.g. the `ssh`
   alias isn't set up until step 3 below — ask the student whether they think there are
   Parquet files to fetch.
3. Fetch via `rsync` over `ssh`, using an `ssh` config alias rather than a raw
   `user@host` — this is what makes the resulting `Makefile` reusable by teammates once
   it's committed and pushed. Each person defines the *same alias name* in their own
   `~/.ssh/config`, pointing at the same host but with their own username, so the alias
   itself must not have a username baked into it (don't call it e.g. `alice-cluster`; a
   short, cluster- or project-specific name works well, e.g. `anno`). Recommend a short
   alias name to the student and confirm they're happy with it — they'll type it in every
   fetch, and everyone else on the project will reuse the same name. Tell them where it's
   defined: their own `~/.ssh/config` (not part of this repo, and never committed — it's
   per-person, per-machine). If they don't already have an entry for this host, help them
   add one:
   ```
   Host anno
       HostName cluster.example.edu
       User their_remote_username
   ```
4. Write (or extend) `data/Makefile` with variables for the host alias and the remote
   `<outdir>` path, and one target per piece being fetched. In most cases it's simplest to
   land everything straight in `data/` itself rather than recreating the remote
   subdirectory structure locally — fetch each source into `.` (the recipes already run
   with `data/` as the working directory), not into a same-named subdirectory. Since these
   targets no longer produce a file/directory matching their own name, mark them
   `.PHONY` so `make` doesn't get confused about when to (re-)run them — harmless anyway,
   since `rsync` only re-transfers what changed. For an `ampliseq` project:
   ```makefile
   REMOTE_HOST   = anno
   REMOTE_OUTDIR = /path/to/the/run/results

   .PHONY: all dada2 pipeline_info

   all: dada2 pipeline_info

   dada2:
   	rsync -av --include='*.tsv' --exclude='*' $(REMOTE_HOST):$(REMOTE_OUTDIR)/dada2/ .

   pipeline_info:
   	rsync -av --include='*versions*.yml' --exclude='*' $(REMOTE_HOST):$(REMOTE_OUTDIR)/pipeline_info/ .
   ```
   For `metatdenovo`/`magmap`, replace the `dada2` target with a `summary_tables` one that
   fetches `*.tsv.gz` from `$(REMOTE_OUTDIR)/summary_tables/` the same way (i.e.
   `--include='*.tsv.gz' --exclude='*'`). Keep the trailing slash on the remote (source)
   side of each `rsync` — without it, rsync nests the source directory inside the
   destination instead of copying its contents into it.
5. Wire in the Parquet files, one of two ways depending on what step 2 found:
   - **They already exist remotely**: add them to the same `rsync` target (or a sibling
     one) with `--include='*.parquet'`, and prefer reading the Parquet copies over the
     TSVs in the `.qmd` once fetched — same data, smaller and faster to load.
   - **They don't exist**: every project already has `scripts/convert_to_parquet.R`
     (scaffolded by `setup_project.sh`, no need to write it) — a generic one-file-in,
     one-file-out converter meant to be called once per table from a `data/Makefile`
     pattern rule. Two pattern rules are needed, one per source extension actually being
     fetched — `ampliseq`'s `dada2/*.tsv` is uncompressed, `metatdenovo`/`magmap`'s
     `summary_tables/*.tsv.gz` isn't, and a rule for one extension silently won't match
     the other:
     ```makefile
     %.parquet: %.tsv.gz
     	Rscript ../scripts/convert_to_parquet.R $< $@

     %.parquet: %.tsv
     	Rscript ../scripts/convert_to_parquet.R $< $@
     ```
     **A pattern rule alone does nothing** — `make` only applies a pattern rule to build a
     target something else actually asks for, so list every fetched table's `.parquet`
     filename by name, rather than reaching for `$(wildcard *.tsv.gz)`/`$(patsubst ...)` to
     generate that list automatically: `make` expands `$(wildcard ...)` once, when it first
     reads the Makefile — before the `dada2`/`summary_tables` recipe has fetched anything
     into a fresh `data/` — so it would see no `.tsv`/`.tsv.gz` files yet and silently
     produce an empty list.
     A hardcoded list is also more readable for someone new to `make`.

     **Do not list the `.parquet` files directly as prerequisites of `all`, even
     hardcoded — that still fails outright on a genuinely fresh `data/`.**
     Confirmed the hard way (metatdenovo output, 2026-09-10), on the very first `make all`
     run against an empty `data/`: GNU Make resolves a pattern rule's prerequisite (here,
     whether `foo.tsv.gz` exists, to satisfy `%.parquet: %.tsv.gz` for `foo.parquet`) via a
     `stat()` done once, the first time it considers that `.parquet` target while walking
     `all`'s prerequisite list — and that happens in the same left-to-right pass as `all`'s
     other prerequisites, before the fetch recipe that actually creates `foo.tsv.gz` has
     run.
     The result is a hard, deterministic error, not a silent no-op like the `$(wildcard
     ...)` case above:
     ```
     make: *** No rule to make target 'foo.parquet', needed by 'all'.  Stop.
     ```
     A second `make all` then succeeds, because by then the `.tsv.gz` files already exist
     from the first (partially-failed) run — easy to mistake for a one-off fluke rather
     than the reproducible GNU Make behavior it actually is.
     The fix: fetch first, then hand the Parquet conversions to a fresh sub-`make` — a new
     `make` process re-`stat()`s the filesystem from scratch, after the fetch recipes have
     already run:
     ```makefile
     .PHONY: all fetch parquet dada2 pipeline_info

     all: fetch
     	$(MAKE) parquet

     fetch: dada2 pipeline_info

     parquet: ASV_table.parquet ASV_tax.<database>.parquet

     dada2:
     	rsync -av --include='*.tsv' --exclude='*' $(REMOTE_HOST):$(REMOTE_OUTDIR)/dada2/ .

     pipeline_info:
     	rsync -av --include='*versions*.yml' --exclude='*' $(REMOTE_HOST):$(REMOTE_OUTDIR)/pipeline_info/ .

     %.parquet: %.tsv.gz
     	Rscript ../scripts/convert_to_parquet.R $< $@

     %.parquet: %.tsv
     	Rscript ../scripts/convert_to_parquet.R $< $@
     ```
     It needs the `arrow` and `readr` R packages — ask the student before installing
     `arrow` if it isn't already there (`readr` is core tidyverse, usually already
     present).
6. Since fetched files now land directly in `data/` with whatever names the pipeline gave
   them, per-subdirectory `.gitignore` entries no longer make sense. Instead, check whether
   the project's `.gitignore` already ignores everything under `data/` except the tracked
   scaffolding; if not, add:
   ```
   data/*
   !data/Makefile
   !data/.gitkeep
   ```
   The whole point of fetching via `Makefile` instead of committing raw output is defeated
   if `git add .` ends up staging it anyway. `data/sample_table.tsv` (step 1) is the
   deliberate exception — small, hand-authored, and not reproducible by re-running
   anything, so it belongs in git unlike the rest of `data/`. Add `!data/sample_table.tsv`
   alongside the two exceptions above if a sample table exists.

### Same-machine source: symlink instead of steps 3-6

If step 1 established the pipeline's output directory is on **this same machine** rather
than a remote one, skip steps 3-6 above entirely and do this instead — no `ssh` alias, no
`rsync`, no `Makefile` fetch target:

1. Symlink the same files step 2 identified straight into `data/`, e.g. for `ampliseq`:
   `ln -s <outdir>/dada2/*.tsv data/` (and `ln -s <outdir>/pipeline_info/*versions*.yml
   data/`); for `metatdenovo`/`magmap`, symlink `<outdir>/summary_tables/*.tsv.gz` instead.
   If Parquet files already exist alongside (step 2), symlink those too instead of (or
   next to) the TSVs; if not, the same `scripts/convert_to_parquet.R` fallback from step 5
   above still applies — it works fine against a symlinked source, `read_tsv()` and
   friends follow symlinks transparently.
2. **Commit the symlinks directly** rather than gitignoring `data/*` — a symlink is just a
   short path string, not the actual data, so there's nothing to protect against
   accidentally committing (unlike step 6's rsync-fetched files). Simpler than steps 4/6's
   `Makefile`-target-plus-gitignore-exception dance, and sidesteps the whole class of
   `make` pattern-rule ordering bugs steps 3-5 had to work around.
3. **Tell the student clearly that this makes the project only usable on this machine** —
   the symlinks point at an absolute path that won't exist anywhere else, so they'll be
   dangling (broken) if this repo is ever cloned onto a different computer. If they think
   they'll need to work on this project from elsewhere later, use the remote `rsync`
   approach (steps 3-6) instead, even though the source happens to be local right now.

## Adding a "sanity check"

When a student asks for a "sanity check" (or similar — a first-look diagnostic on their
pipeline output), this means a specific deliverable: an NMDS ordination plus a stacked
phylum-level taxonomy composition barplot, as a new `sanity_check.qmd`. Prerequisites:
pipeline output already fetched into `data/` (see above, including a sample table if one
exists — needed to colour/shape the NMDS).

1. `git clone --depth 1 https://github.com/erikrikarddaniel/dltemplates <tmpdir>` into a
   scratch/temp directory, same as the initial project bootstrap — never inside the
   project directory, and delete it once done.
2. Copy `<tmpdir>/R/sanity_check_<pipeline>.qmd` to `sanity_check.qmd` in the project root
   (`<pipeline>` is `ampliseq`, `magmap`, or `metatdenovo`, matching whichever pipeline
   step 1 of the fetching instructions above already established), and
   `<tmpdir>/R/sanity_check_core.R` to `scripts/sanity_check_core.R` — the qmd `source()`s
   it for the shared statistics/palette-consistency logic. Unlike `convert_to_parquet.R`,
   this isn't part of the default scaffold, so it only exists in a project once a sanity
   check has actually been added.
3. Fill in the templated bits: the `__TITLE__` placeholder in the YAML header, and, for
   `metatdenovo` specifically, the `PREFIX` constant (`__ASSEMBLY_ORFCALLER__`) in the
   `constants` chunk — set it to match whichever `<assembly>.<orfcaller>` prefix is
   actually on the files in `data/` (`Sys.glob("data/*.counts.tsv.gz")` shows what's
   there if it's not obvious from context).
4. The `read-data` chunk in each template has pipeline-specific notes worth rereading
   before trusting it blindly — in particular, `ampliseq`'s comment about verifying
   `ASV_table.tsv`'s header format, and `metatdenovo`'s about which taxonomy source
   (EUKulele vs. Diamond) is actually present in this project's `data/`.
5. These templates need `RColorBrewer`, `vegan`, and `patchwork` (`metatdenovo`'s also
   combines two NMDS panels with `patchwork::plot_layout(guides = "collect")`) — ask
   before installing whichever the student doesn't already have.
6. Once it's built and rendering, ask the student whether you should walk them through the
   code and how it's set up (the `sanity_check_core.R` functions, the loader, why NMDS
   uses no transformation, the palette-consistency mechanism, etc.) — don't launch into an
   unprompted explanation, but do offer, since this is exactly the kind of code a student
   is expected to understand and eventually extend themselves, not just run.

The taxonomy barplot's non-top taxa always split into two separate stacked categories,
`Other` and `Unassigned`, rather than one combined bucket — `taxonomy_barplot_data()` in
`sanity_check_core.R` does this automatically, no per-project wiring needed.
`Unassigned` is features (ASVs/ORFs) with no classification at all at that rank (`NA`) — a
statement about classification coverage/reference-database recall.
`Other` is features that *are* classified, just individually below `threshold` — a
statement about true community diversity (many genuine low-abundance taxa).
Conflating the two into one "Other" bucket (an earlier version of this function did) hides
which of those two very different explanations actually dominates a sample, which matters
for a sanity check specifically: a mostly-`Unassigned` bar points at a reference-database
or classification-pipeline problem worth investigating, while a mostly-`Other` bar just
reflects a genuinely diverse community and is often unremarkable.
Confirmed worth the split on real data (remedios_non-polyA_overview, metatdenovo,
2026-09-10): the combined bucket ran 50-70% of TPM per sample, opaque as to why; keep an
eye out for the same pattern recurring on other real runs once this has been used a few
more times.

## Moving heavy work out of the Quarto document

Remind students that anything computationally heavy shouldn't live inline in a `.qmd` —
it re-runs on every render, which gets slow and makes rendering flaky. Instead, it belongs
in a standalone R script under `scripts/`, wired into `data/Makefile`'s `all` target so it
runs once, via RStudio's Build button (the same `make` chain used for fetching data: root
`Makefile` → `data/Makefile`), rather than every time someone knits the report. The script
writes its result into `data/`, and the `.qmd` just reads that finished file.

Two situations this comes up for a lot, worth raising proactively rather than waiting for
the student to hit the problem:

- **Consolidating taxonomies**: for each ASV (`ampliseq`) or ORF (`metatdenovo`/`magmap`),
  several fetched files may each assign a candidate taxonomy, and something has to decide
  which one to settle on per feature. That decision logic is exactly the kind of thing that
  belongs in a `scripts/` script, not inline in the report.
- **Large statistical tests**: run once and their result cached as a `data/` file, instead
  of being recomputed on every render.

As with fetched pipeline output, the result of these scripts is often too large to commit
— the same blanket `data/*` `.gitignore` pattern from the section above already covers
that, no extra bookkeeping needed as long as the script's output stays under `data/`.

There's no settled convention yet for exactly how these scripts should be structured (input
sources, output file naming, how granular the Makefile rules should be, whether some
version of `misc/makefile.library`'s `.makecall` provenance-recording pattern is worth
reusing here). Don't assume an approach — when a task like this comes up, ask the student
(or the user) how they want to structure it before writing the script or the Makefile rule.

## Principles

*(draft — to be refined)*

The structure separates raw/derived data (`data/`), code (`scripts/`), and generated output
(`figures/`, the rendered `.qmd`) so that everything except `data/` and the figures can be
regenerated from source and safely committed to git, while large data files are kept out of
version control by `.gitignore`. The `Makefile` chain and the `.makecall` convention (see
`misc/makefile.library` in dltemplates) exist to record *how* each data file was produced —
tool version, parameters, and inputs — next to the file itself, for reproducibility.
