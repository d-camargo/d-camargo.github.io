---
name: site-content
description: Use this skill when writing or editing any content for the dcamargo Jekyll site — including blog posts, portfolio pages, and any other page on the site. Covers both Portuguese (primary) and English (secondary) versions. Use it whenever writing text for a new post, portfolio entry, section description, or page body, even if the user doesn't explicitly mention the skill.
---

# Site Content Writing — dcamargo.com.br

## Site Identity

Diego Camargo's personal site for a Civil/Transportation Engineer and educator at CEFET-MG. Content spans technical projects (GIS tools, Python scripts, data tools), urban mobility research, and educational work. The audience is professional peers, students, and the broader geospatial/transport community.

## Voice and Tone

- **Professional but human.** Write as an expert talking to a colleague, not a CV bullet point.
- **First-person implied.** The site belongs to Diego — writing reflects his perspective and experience.
- **Show the "why".** Always explain the motivation behind a project or post, not just the what.
- **Avoid marketing fluff.** No "revolutionary", "cutting-edge", "game-changing". Describe impact concretely.
- **Portuguese is primary.** Write PT first, then EN. Both versions must be equivalent in quality — not just translated.

## Writing Style — What to Strictly Avoid

These rules apply to ALL content on the site (blog posts, portfolio pages, section descriptions):

- **No binary/cliché structures.** Never use "Não é sobre X. É sobre Y" or "Não é sorte. É método."
- **No generic opening hooks.** Do not start with "O que a maioria das pessoas não percebe é...", "Pouca gente sabe...", or "Aqui está o que ninguém está falando...".
- **No advertisement tone.** Avoid "A tecnologia está transformando o mundo...", "O futuro já chegou", or "Uma jornada incrível que está apenas começando."
- **No artificial grandeur.** Don't inflate ordinary steps into turning points: never write "Não foi apenas um projeto. Foi uma virada de chave" or "Não foi apenas uma reunião. Foi um marco."
- **No fluff or exaggeration.** Cut excessive adverbs, adjectives, and rhetorical dashes used for drama. Be direct.
- **Zero em dashes (`—`) in body text.** It is a classic AI tell (same rule as the `conteudo-universal` skill). Use a colon, parentheses, a comma, or split the sentence.
- **No repetition for padding.** Never restate the same idea with different words to fill space.
- **No clichéd adjectives** for tech things: avoid "poderoso", "robusto", "intuitivo" unless you can prove it concretely.

The test: read the text aloud. If it sounds like a radio ad, a LinkedIn post, or something an AI would generate unprompted — rewrite it.

## Text Formatting Rules

- `text-align: justify` on all body paragraphs (`p`) in both portfolio pages and blog posts.
- Line height: 1.6 (portfolio) or 1.8 (blog posts).
- Keep paragraphs focused: one idea per paragraph, 3–5 sentences max.
- Use `<strong>` for emphasis on key terms, not for decorative bold.

## Portfolio Pages

### Structure

Follow this order — don't skip sections:

1. **O Problema / The Problem** — What gap or pain point existed? Be specific. Avoid abstract statements.
2. **A Solução / The Solution** — How was it addressed? If there's an evolution over time, use the timeline component.
3. **Funcionalidades Principais / Key Features** — One `<p>` per feature, leading with `<strong>Feature name:</strong>`. No nested bullets inside the project-content div.
4. **Stack Tecnológica / Technology Stack** — Use `.tech-badge` spans, not a prose list.
5. **Impacto / Impact** — Concrete outcome: time saved, people reached, problems solved.

### Timeline Component (when project evolved over years)

```html
<div class="timeline-item">
    <div class="timeline-year">YEAR — Label</div>
    <p style="margin-bottom:0">Description here.</p>
</div>
```

Use only when there are ≥2 meaningful milestones. Group events from the same year into one item.

### Links at the End (optional)

```html
<div class="project-links">
    <a href="URL" target="_blank" class="btn primary-btn"><i class="fas fa-external-link-alt"></i> Label</a>
    <a href="URL" target="_blank" class="btn secondary-btn"><i class="fab fa-github"></i> Label</a>
</div>
```

### Header image (optional but recommended)

Place before `.project-content` div:
```html
<div class="project-image" style="text-align:center; margin-bottom: 2rem;">
    <img src="{{ '/assets/images/portfolio/IMAGE.webp' | relative_url }}" alt="Alt text" style="max-width:800px; width:100%; border-radius:12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
</div>
```

## Blog Posts

### Front Matter

PT post (`_posts/YYYY-MM-DD-slug.md`):

```yaml
---
layout: post
title: "Título do Post"
lang: pt
translation: /en/YYYY/MM/DD/slug.html   # URL of the EN counterpart (its permalink); omit if none
category: "Geoprocessamento"            # singular field, one category, PT name
---
```

EN post (`_posts/YYYY-MM-DD-slug-en.md`, same date, slug + `-en`):

```yaml
---
layout: post
title: "Post Title"
lang: en
translation: "/geoprocessamento/YYYY/MM/DD/slug.html"  # PT post's URL — includes the lowercase PT category segment (spaces kept), so quote it
permalink: /en/YYYY/MM/DD/slug.html     # required for EN posts
category: "Geoprocessing"               # EN name of the same category
---
```

Rules:
- Never use plural `categories` — listings read `post.category`.
- Category names must match the language of the post. Existing pairs: Engenharia de Transportes / Transport Engineering, Geoprocessamento / Geoprocessing, Planejamento Urbano / Urban Planning, Geral / General.
- The `translation` field feeds the nav language toggle; without it the toggle falls back to the other language's blog index.
- Date comes from the filename; no `date:` field is used.

### Structure

- Open with a **hook** — one concrete sentence about what the post solves or reveals.
- Use `## H2` headings to break up sections. Keep them descriptive, not generic ("Como instalar" not "Instalação").
- End with a **call to action** or takeaway — what should the reader do or think next?
- For EN posts: keep the same structure as PT but adapt idioms; don't translate literally.

## Bilingual Files

Every PT portfolio page at `portfolio/NAME.html` must have a matching EN version at `en/portfolio/NAME.html` with:
- `lang: en` in front matter
- Equivalent content, not word-for-word translation
- Correct English terminology (see "Terminology" below)

Every PT blog post at `_posts/DATE-NAME.md` must have an EN version at `_posts/DATE-NAME-en.md`.

## Terminology

| PT | EN (correct) |
|---|---|
| Curso Técnico em Trânsito | Traffic Operations Technical Program |
| Curso Técnico em Estradas | Road Building Technical Program |
| EPTNM | Secondary-Level Technical Education (EPTNM) |
| Ensino Médio | Secondary education |
| Bimestre | Quarter (academic quarter) |
| Mapa de Turma | Class map (grade/attendance spreadsheet) |
| SIGAA | SIGAA (institutional academic system) |
| CEFET-MG | CEFET-MG (Federal Center for Technological Education of Minas Gerais) |

## Portfolio Index Cards

When adding a project to `portfolio/index.html` and `en/portfolio/index.html`, always wrap in an `<a>` tag so the card is clickable. Use the same cover image in both the card and the project page.

```html
<a href="{{ '/portfolio/NAME.html' | relative_url }}" style="text-decoration: none; color: inherit; display: block;">
    <div class="portfolio-item">
        <div class="portfolio-bg" style="background-image: url('IMAGE_URL');"></div>
        <div class="portfolio-content">
            <h3>Project Title</h3>
            <span class="portfolio-category">Category</span>
        </div>
    </div>
</a>
```

Also add to `index.html` (PT) and `en/index.html` (EN) main page portfolio grid — replace a placeholder card, keeping the grid at 3 items.
