# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Serve locally with live reload (http://localhost:4000)
./serve.sh

# Build only, output to _site/
./serve.sh --build

# Verification gate — same thing, via the target the Hermes engine looks for
make test

# Generate a post cover image (see Images below)
bin/gen-post-image.py --slug <slug> --prompt "<subject>" [--n 3]
```

`make test` is the project's verification gate: it runs `jekyll build`, which exits
non-zero on a Liquid error, invalid frontmatter or a missing include. It exists because
the Hermes engine (`planexec.py`) looks for a `test:` Makefile target to decide whether a
project has a gate at all; without it `run_tests` returns `None` and the review approves
on the reviewing model's word alone — on a repo that publishes straight to production.
Run it before any push.

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

## Skills

Project skills are located exclusively in `.claude/skills/<nome>/SKILL.md`:
- `site-content` — voz e tom
- `blog-post-writer` — estrutura e gravação do post

