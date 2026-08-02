# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Serve locally with live reload
bundle exec jekyll serve

# Build for production
bundle exec jekyll build
```

Dependencies live in `vendor/bundle` (set via `.bundle/config`). Run `bundle install` if gems are missing.

Deployment is fully automatic: pushing to the `gh-pages` branch triggers the GitHub Actions workflow (`.github/workflows/deploy-pages.yml`), which builds and deploys to GitHub Pages at `dcamargo.com.br`.

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

## Skills

Project skills are located exclusively in `.claude/skills/<nome>/SKILL.md`:
- `site-content` — voz e tom
- `blog-post-writer` — estrutura e gravação do post

