# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Serve locally with live reload (http://localhost:4000)
./serve.sh

# Build only, output to _site/
./serve.sh --build

# Verification gate — content lint + build, via the target the Hermes engine looks for
make test

# Content lint alone (instant, no container)
bin/check-content.py

# Generate a post cover image (see Images below)
bin/gen-post-image.py --slug <slug> --prompt "<subject>" [--n 3]

# Import numbered screenshots for the body of a post (see Screenshots below)
bin/add-post-images.py --slug <set> --from-cache <n>   # or 1=<file> 2=<file> ...
bin/add-post-images.py --slug <set> --apply _posts/<post>.md
```

`make test` is the project's verification gate, and it runs two independent checks:

- **`bin/check-content.py`** turns the mechanical half of the `site-content` skill into a
  real check: em dashes in body text (the rule is zero), the banned "Não é apenas X"
  structure, unproven adjectives (poderoso/robusto/intuitivo), advertising tone, `#` H1 in
  the body, incomplete frontmatter (`layout`, `title`, `lang`, `category`, `image`), a
  category that does not exist for the post's language, an EN post without `permalink`, a
  `translation:` pointing nowhere, images referenced but absent from disk, an unresolved
  `[[print N: ...]]` marker, and a numbered screenshot set used out of sequence. Note that
  the PT/EN pairing is checked through `translation:`, **not** the filename — several
  pairs use translated slugs (`oficial`/`official`, `demanda`/`demand`), so the
  `slug` + `-en` convention is not reliable.
- **`jekyll build`**, which exits non-zero on a Liquid error, invalid frontmatter or a
  missing include.

It exists because the Hermes engine (`planexec.py`) looks for a `test:` Makefile target to
decide whether a project has a gate at all; without it `run_tests` returns `None` and the
review approves on the reviewing model's word alone — on a repo that publishes straight to
production. Run it before any push.

`serve.sh` runs Jekyll inside a `ruby:3.3` podman container, because the VPS has no Ruby and no root access to install one. Gems are installed into `vendor/bundle` on first run (gitignored); later runs reuse them. On a machine that does have Ruby installed, `bundle exec jekyll serve` works directly.

The server binds to `127.0.0.1` only. To view it from another machine, open an SSH tunnel from that machine:

```bash
ssh -L 4000:localhost:4000 -L 35729:localhost:35729 diego@<ip-da-vps>
```

then browse to `http://localhost:4000`. Port 35729 carries live reload.

`_config.yml` has an `exclude:` list keeping repo working files (`CLAUDE.md`, `Skills/`, `bin/`, `serve.sh`, `Makefile`, the Gemfiles) out of the published site — anything added at the repo root that is not site content must be added there too.

Deployment is fully automatic: pushing to the `gh-pages` branch triggers the GitHub Actions workflow (`.github/workflows/deploy-pages.yml`), which builds and deploys to GitHub Pages at `dcamargo.com.br`. **A push is a publication** — there is no staging step between `gh-pages` and the live professional site. Build clean (`make test`) before pushing.

## Two ways this repo gets worked on

Besides interactive Claude Code, this project is also driven from Discord through the
Hermes agent (channel `#d-camargo-github-io`), which runs a plan → run → review → push
pipeline via `~/.hermes/skills/planexec/scripts/planexec.py`. Two consequences for
anything written here:

- The executing engine is often **Gemini (`agy`), which does not read `.claude/skills/`**.
  The site's voice and post-structure rules live there (`site-content`,
  `blog-post-writer`), so content-writing steps must be tagged `[T03]` in the plan to
  route to a Claude engine. Everything an engine must know regardless of which one it is
  belongs in **this file**, not only in a skill.
- `planexec push` is the only sanctioned way to commit from that pipeline, and it
  publishes. See `~/.hermes/skills/proj-d-camargo-github-io/SKILL.md`.

## Architecture

Jekyll 4.4 static site. No collections — content is either `_posts/` (Markdown) or plain HTML pages with YAML frontmatter.

**Layouts** (`_layouts/`):
- `default.html` — shared shell: navbar, ambient glow effects, footer, GTM/GA scripts. Nav is bilingual: detects `page.lang == 'en'` to switch link targets and show the language toggle.
- `post.html` — wraps `default`, adds post header with localized date formatting and a back-to-blog button.

**Bilingual structure**: Every page exists in two versions.
- Portuguese: root paths (`/`, `/blog/`, `/portfolio/`, `/curriculo/`)
- English: mirrored under `/en/` (`/en/`, `/en/blog/`, `/en/portfolio/`, `/en/curriculo/`)

Blog listings filter posts by language: `where_exp: "item", "item.lang != 'en'"` for PT, the inverse for EN.

**Post frontmatter**:
```yaml
---
layout: post
title: "Post Title"
lang: pt                    # 'pt' or 'en'
category: "Geoprocessamento"  # singular field, one category per post
permalink: /en/YYYY/MM/DD/slug.html   # required for English posts only
translation: /en/YYYY/MM/DD/slug.html # URL of the counterpart post in the other language; the nav language toggle uses it. On EN posts this is the PT post's date-based URL, e.g. "/2026/06/24/slug.html" (quote it) — no category in the path, see the note below. Omit if there is no counterpart — the toggle then falls back to the other language's blog index.
---
```

**Categories**: Each post declares a single `category` (singular field — the blog listings read `post.category`; do not use a plural `categories` list). The blog index (`blog/index.html` and `en/blog/index.html`) builds an interactive filter bar from the distinct categories and shows a gold badge on each card. Posts with no `category` fall back to `Geral`. Categories must be language-matched to the post — use the PT name on PT posts and the EN name on EN posts. Existing pairs:

| PT | EN |
|---|---|
| Engenharia de Transportes | Transport Engineering |
| Geoprocessamento | Geoprocessing |
| Planejamento Urbano | Urban Planning |
| Geral | General |

Note: `category` no longer appears in post URLs. `_config.yml` sets `permalink: /:year/:month/:day/:title.html`, so PT posts resolve to `/2026/06/24/slug.html` (EN posts keep their explicit `/en/...` permalink). This replaced the Jekyll default `/:categories/...`, which put the category in the path — a single-word category like `geoprocessamento` was then being rewritten into a subdomain (`geoprocessamento.dcamargo.com.br`) by the domain's URL forwarding, 404ing the page. Links are generated via `post.url`, so listings and nav follow automatically; only hardcoded cross-links between posts and EN `translation:` fields must use the date-based path.

Portuguese posts are named `YYYY-MM-DD-slug.md`; English counterparts use the same date and a matching slug with `-en` suffix, e.g. `2026-06-03-desire-lines-aon-delaunay-qgis-en.md`.

**Design system** (all in `assets/css/style.css`):
- Dark theme: `--bg-main: #0a0a0c`, `--accent: #d4af37` (metallic gold)
- Fonts: `'Cinzel'` (display headings) + `'Montserrat'` (body)
- CSS custom properties used throughout — never hard-code colors or fonts that conflict with these variables.

**Portfolio pages** (`portfolio/` and `en/portfolio/`) are plain HTML files using `layout: default`. Each page is self-contained with its own `<style>` block; there is no shared portfolio template.

**Images**: Post images go in `assets/images/posts/`; portfolio images go in `assets/images/portfolio/`.

Post cover images are generated at authoring time by `bin/gen-post-image.py` and committed as static assets — the Jekyll build never calls the API, so builds stay free, deterministic and secret-free. The script calls the Gemini image API (`gemini-3.1-flash-image`, "Nano Banana 2", by default), applies a fixed house-style prompt derived from the design system, and writes a resized WebP capped at 200KB. Generated images carry an invisible SynthID watermark.

The API key lives in `~/.config/dcamargo/gemini.env` (mode 600, outside the repo); `GEMINI_API_KEY` in the environment overrides it. **Image models have no free tier** — the key's Google Cloud project must have billing enabled, otherwise every call returns HTTP 429 with `free_tier_requests, limit: 0`. A Google AI Pro subscription does not by itself grant API access (its benefits apply to the AI Studio web interface), but it does entitle the account to $10/month in Google Cloud credits via the Google Developer Program, activated manually at google.dev, which the API usage draws from.

Without billing there is a manual route that stays within the subscription: `--print-prompt` emits the full house-style prompt to paste into the Gemini app, AI Studio or Antigravity, and `--from-file <path>` imports the downloaded image through the same WebP normalisation. Do not attempt to reuse the Antigravity OAuth token in `~/.gemini/` as an API credential — it is not one.

Posts should carry an `image:` frontmatter field pointing at the cover; `jekyll-seo-tag` turns it into `og:image`. A PT post and its EN counterpart share one image file.

**Screenshots in the body** (posts about the QGIS plugins, mostly) are a separate thing from the cover and follow their own convention, enforced by `bin/check-content.py`:

- They live in a **subfolder per post**, named after the post's subject and a sequence number: `assets/images/posts/sigbus01/`. The PT post and its EN counterpart share the same folder.
- Inside the folder they are **numbered `1.webp`, `2.webp`, `3.webp`…**, and the post's body references them **in that order, starting at 1, with no gaps**. Image 3 in the folder is the third image the reader meets. Older sets are `.png`; new ones are WebP.
- Diego sends the screenshots as **Discord attachments**, which the Hermes agent caches under `~/.hermes/cache/images/` with hash names (`img_<hash>.png`) that carry no order. The number therefore comes from him, not from the filename.

The workflow has two steps. First import. Attachments are cached in the order they were attached to the Discord message, so when that is the intended order all it takes is the count:

```bash
bin/add-post-images.py --slug sigbus02 --from-cache 3
```

The script prints which file became which number, with each file's age, so the mapping can be checked before anything else happens. Add `--start 4` to append to a set that already exists.

⚠️ **The Hermes image cache is a single global directory** — one pile for every channel and every topic, with filenames (`img_<uuid>.png`) that say nothing about where they came from. Working inside a per-post Discord topic does **not** isolate it. So an image sent in another conversation can land inside the window `--from-cache` takes; the script flags any file more than 15 minutes apart from the previous one, because attachments of one message are written seconds apart. Read the printed mapping before moving on — the failure mode is silent, the wrong image under the right number.

When the order differs, give each number explicitly instead:

```bash
bin/add-post-images.py --slug sigbus02 \
    1=~/.hermes/cache/images/img_a1b2.png \
    2=~/.hermes/cache/images/img_c3d4.png
```

The script resizes to 1600px wide and writes WebP, trying lossless first and falling back to a quality ladder only when the file would exceed 300KB — screenshots carry interface text, where compression artefacts show up early. It refuses to overwrite an existing number without `--force`.

Second, in the draft, each image is marked **at the exact point in the text where it belongs**:

```markdown
[[print 2: alt text describing the screen]]
```

and `--apply` swaps every marker for the real markdown link, once per language:

```bash
bin/add-post-images.py --slug sigbus02 --apply _posts/2026-08-05-post.md
bin/add-post-images.py --slug sigbus02 --apply _posts/2026-08-05-post-en.md
```

Markers out of sequence (`2, 1`, a repeat, a gap) abort the run and write nothing. Images already resolved by an earlier `--apply` count in that sequence, so a second batch added with `--start` is marked `[[print 4: ...]]` onwards, not renumbered from 1. An unresolved `[[print N: ...]]` marker left in a post is a gate error, so a marker can never reach production as raw text. A numbered file no post references is a gate warning.

## Skills

Project skills are located exclusively in `.claude/skills/<nome>/SKILL.md`:
- `site-content` — voz e tom
- `blog-post-writer` — estrutura e gravação do post

