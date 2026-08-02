#!/usr/bin/env python3
"""Gera a imagem de capa de um post via API Gemini (Nano Banana) e grava em WebP.

Uso tipico, a partir da raiz do repositorio:

    bin/gen-post-image.py --slug gisbr-ssl \\
        --prompt "cadeia de certificados SSL protegendo camadas de mapa"

Gera assets/images/posts/gisbr-ssl.webp e imprime o markdown pronto para colar
no post. Com --n 3 grava tres variacoes numeradas para escolha manual.

A chave vem de ~/.config/dcamargo/gemini.env (ou da variavel de ambiente
GEMINI_API_KEY, que tem precedencia). Imagens geradas carregam marca d'agua
SynthID.

Sem faturamento na chave, ha o caminho manual, coberto pela assinatura Google AI
Pro: gerar a imagem no app Gemini, no AI Studio ou no Antigravity e importa-la.

    bin/gen-post-image.py --slug gisbr-ssl --prompt "..." --print-prompt
    # cole o prompt na interface, baixe o PNG, depois:
    bin/gen-post-image.py --slug gisbr-ssl --from-file ~/Downloads/img.png \\
        --alt "<alt text>"
"""

import argparse
import base64
import io
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ENV_FILE = Path.home() / ".config" / "dcamargo" / "gemini.env"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTDIR = REPO_ROOT / "assets" / "images" / "posts"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Prompt de casa: mantem as capas coerentes com o design system do site
# (assets/css/style.css). Alterar aqui muda o visual de toda a serie.
HOUSE_STYLE = (
    "Editorial cover illustration for a technical blog about geoprocessing, "
    "transport engineering and urban planning. "
    "Flat vector illustration with thin, even linework, isometric or top-down "
    "construction, diagrammatic rather than decorative. "
    "NOT a photorealistic 3D render, no glossy materials, no volumetric reflections. "
    "Near-black background (#0a0a0c). Metallic gold accents (#d4af37) as the only "
    "saturated color, used sparingly on one focal element. Restrained and "
    "sophisticated, generous negative space, muted desaturated palette apart from "
    "the gold. Minimal ornamentation: no laurels, no badges, no filigree. "
    "No text, no letters, no numbers, no logos, no watermarks, no UI chrome, "
    "no human faces. Subject: "
)


def load_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()
    if not ENV_FILE.exists():
        sys.exit(
            f"erro: {ENV_FILE} nao existe e GEMINI_API_KEY nao esta definida.\n"
            f"crie o arquivo com a linha: GEMINI_API_KEY=<sua-chave>"
        )
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        if name.strip() == "GEMINI_API_KEY":
            value = value.strip().strip("'\"")
            if not value or value == "cole-a-chave-aqui":
                sys.exit(f"erro: o placeholder em {ENV_FILE} nao foi substituido.")
            return value
    sys.exit(f"erro: nenhuma linha GEMINI_API_KEY= encontrada em {ENV_FILE}.")


def request_image(api_key, model, prompt, aspect, size):
    """Chama a API e devolve os bytes da imagem.

    imageConfig e enviado primeiro; se o modelo nao aceitar o campo, refaz a
    chamada sem ele em vez de abortar.
    """
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect, "imageSize": size},
        },
    }

    for attempt in ("com imageConfig", "sem imageConfig"):
        req = urllib.request.Request(
            ENDPOINT.format(model=model),
            data=json.dumps(body).encode(),
            headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                payload = json.load(resp)
            break
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            message = ""
            try:
                message = json.loads(detail).get("error", {}).get("message", "")
            except json.JSONDecodeError:
                message = detail[:400]

            retriable = attempt == "com imageConfig" and exc.code == 400 and "imageConfig" in detail
            if retriable:
                body["generationConfig"].pop("imageConfig", None)
                print("aviso: modelo rejeitou imageConfig, repetindo sem ele", file=sys.stderr)
                continue

            if exc.code == 429 and "free_tier" in detail:
                sys.exit(
                    "erro 429: o projeto da chave esta no free tier, que tem cota ZERO "
                    "para modelos de imagem.\nAtive o faturamento em "
                    "https://aistudio.google.com/apikey (link 'Set up Billing' no projeto)."
                )
            sys.exit(f"erro HTTP {exc.code}: {message}")
    else:
        sys.exit("erro: nao foi possivel obter resposta da API.")

    for candidate in payload.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                return base64.b64decode(part["inlineData"]["data"])

    reason = payload.get("promptFeedback") or payload.get("candidates") or payload
    sys.exit(f"erro: resposta sem imagem. Detalhe: {json.dumps(reason)[:500]}")


def to_webp(raw, dest, max_width, max_kb):
    """Converte para WebP, redimensiona e busca a maior qualidade que cabe no limite."""
    image = Image.open(io.BytesIO(raw)).convert("RGB")
    if image.width > max_width:
        height = round(image.height * max_width / image.width)
        image = image.resize((max_width, height), Image.LANCZOS)

    for quality in (88, 82, 76, 70, 64, 58):
        buffer = io.BytesIO()
        image.save(buffer, "WEBP", quality=quality, method=6)
        if buffer.tell() <= max_kb * 1024:
            break

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(buffer.getvalue())
    return image.size, buffer.tell() / 1024, quality


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slug", required=True, help="nome do arquivo sem extensao, ex: gisbr-ssl")
    parser.add_argument("--prompt", help="o que a imagem deve mostrar (obrigatorio, exceto com --from-file)")
    parser.add_argument("--from-file", type=Path, metavar="PATH",
                        help="pula a API e importa uma imagem local (baixada do app Gemini, "
                             "do AI Studio ou do Antigravity), aplicando a mesma conversao WebP")
    parser.add_argument("--print-prompt", action="store_true",
                        help="so imprime o prompt completo com o estilo de casa, para colar "
                             "no app Gemini / AI Studio; nao chama a API")
    parser.add_argument("--alt", help="alt text; default: derivado do --prompt")
    parser.add_argument("--model", default="gemini-3.1-flash-image",
                        help="default: gemini-3.1-flash-image (Nano Banana 2). "
                             "Use gemini-3-pro-image para texto legivel na imagem.")
    parser.add_argument("--size", default="2K", choices=["1K", "2K", "4K"])
    parser.add_argument("--aspect", default="16:9")
    parser.add_argument("--n", type=int, default=1, help="numero de variacoes")
    parser.add_argument("--max-width", type=int, default=1600, help="largura maxima em px")
    parser.add_argument("--max-kb", type=int, default=200, help="tamanho alvo do WebP")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--raw-prompt", action="store_true",
                        help="usa o --prompt literal, sem o estilo de casa")
    args = parser.parse_args()

    if not args.prompt and not args.from_file:
        parser.error("informe --prompt, ou --from-file para importar uma imagem pronta.")

    prompt = None
    if args.prompt:
        prompt = args.prompt if args.raw_prompt else HOUSE_STYLE + args.prompt

    if args.print_prompt:
        print(prompt)
        return

    alt = args.alt or (args.prompt or args.slug.replace("-", " "))[:120]
    written = []

    if args.from_file:
        # Caminho sem API: a imagem foi gerada no app Gemini / AI Studio / Antigravity
        # (cobertos pela assinatura) e so passa pela normalizacao WebP.
        if not args.from_file.is_file():
            sys.exit(f"erro: {args.from_file} nao existe.")
        dest = args.outdir / f"{args.slug}.webp"
        (width, height), kb, quality = to_webp(args.from_file.read_bytes(), dest, args.max_width, args.max_kb)
        print(f"importado de {args.from_file}", file=sys.stderr)
        print(f"  {dest.relative_to(REPO_ROOT)} — {width}x{height}, {kb:.0f} KB, q{quality}", file=sys.stderr)
        written.append(dest)
    else:
        api_key = load_api_key()
        for index in range(1, args.n + 1):
            name = args.slug if args.n == 1 else f"{args.slug}-{index}"
            dest = args.outdir / f"{name}.webp"
            print(f"gerando {index}/{args.n} ({args.model}, {args.size}, {args.aspect})...", file=sys.stderr)
            raw = request_image(api_key, args.model, prompt, args.aspect, args.size)
            (width, height), kb, quality = to_webp(raw, dest, args.max_width, args.max_kb)
            print(f"  {dest.relative_to(REPO_ROOT)} — {width}x{height}, {kb:.0f} KB, q{quality}", file=sys.stderr)
            written.append(dest)

    print("\n--- frontmatter (og:image via jekyll-seo-tag) ---")
    print(f"image: /assets/images/posts/{written[0].name}")
    print("\n--- markdown, logo apos o gancho de abertura ---")
    for dest in written:
        print(f"![{alt}](/assets/images/posts/{dest.name})")


if __name__ == "__main__":
    main()
