#!/usr/bin/env python3
"""Gate de conteudo dos posts: torna verificavel a parte mecanica do site-content.

Roda como parte do `make test`, junto com o build. O build pega template
quebrado; este pega o texto fora das regras da casa (os "AI tells" que a skill
site-content proibe) e frontmatter incompleto.

Existe pelo mesmo motivo do Makefile (ver C29 no DECISOES.md do Hermes): sem um
gate factual, o review do motor aprova na palavra do modelo. Regra que so vive
numa skill e conselho; regra que roda no gate e limite.

    bin/check-content.py            # falha (exit 1) se houver erro
    bin/check-content.py --quiet    # so imprime problemas
"""

import argparse
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
POSTS = REPO / "_posts"

# Pares PT/EN validos. A categoria precisa bater com o idioma do post.
CATEGORIAS = {
    "pt": {"Engenharia de Transportes", "Geoprocessamento", "Planejamento Urbano", "Geral"},
    "en": {"Transport Engineering", "Geoprocessing", "Urban Planning", "General"},
}

# Marcas de texto gerado que a skill site-content proibe explicitamente.
TELLS = [
    (re.compile(r"—"),
     "em dash no corpo (regra: zero; use dois-pontos, virgula, parenteses ou quebre a frase)"),
    (re.compile(r"\bNão é (apenas|somente|só|sobre)\b", re.I),
     "estrutura binaria 'Não é apenas/sobre X' (proibida)"),
    (re.compile(r"\b(poderos[ao]|robust[ao]|intuitiv[ao]|revolucionári[ao]|inovador[ao]?)\b", re.I),
     "adjetivo batido sem prova concreta"),
    (re.compile(r"\b(game[- ]?chang\w+|cutting[- ]edge|revolutionary|powerful|robust|intuitive)\b", re.I),
     "adjetivo batido sem prova concreta (EN)"),
    (re.compile(r"O futuro (já )?chegou|jornada incrível|virada de chave", re.I),
     "tom publicitario / grandiosidade artificial"),
    (re.compile(r"^# ", re.M),
     "H1 no corpo (o title do frontmatter ja e o H1)"),
]


def parse(texto):
    """Devolve (frontmatter dict, corpo, linha em que o corpo comeca)."""
    if not texto.startswith("---"):
        return {}, texto, 1
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return {}, texto, 1
    bruto, corpo = partes[1], partes[2]
    fm = {}
    for linha in bruto.splitlines():
        if ":" in linha and not linha.startswith((" ", "\t", "#")):
            k, _, v = linha.partition(":")
            fm[k.strip()] = v.strip().strip("\"'")
    return fm, corpo, bruto.count("\n") + 2


def url_do_post(nome, fm):
    """URL publica do post, para casar com o `translation:` do par."""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", nome)
    if not m:
        return None
    a, mes, d, slug = m.groups()
    if fm.get("lang") == "en":
        return fm.get("permalink") or f"/en/{a}/{mes}/{d}/{slug}.html"
    return f"/{a}/{mes}/{d}/{slug}.html"


def checar():
    erros, avisos = [], []
    arquivos = sorted(POSTS.glob("*.md"))
    if not arquivos:
        return [("_posts/", 0, "nenhum post encontrado")], []

    urls = {}
    dados = {}
    for f in arquivos:
        fm, corpo, off = parse(f.read_text())
        dados[f] = (fm, corpo, off)
        u = url_do_post(f.name, fm)
        if u:
            urls[u] = f.name

    for f in arquivos:
        fm, corpo, off = dados[f]
        rel = f"_posts/{f.name}"

        def err(linha, msg):
            erros.append((rel, linha, msg))

        # --- frontmatter obrigatorio ---
        for campo in ("layout", "title", "lang", "category", "image"):
            if campo not in fm:
                err(1, f"frontmatter sem `{campo}:`")

        lang = fm.get("lang")
        if lang and lang not in ("pt", "en"):
            err(1, f"lang invalido: {lang!r} (use pt ou en)")

        cat = fm.get("category")
        if cat and lang in CATEGORIAS and cat not in CATEGORIAS[lang]:
            err(1, f"categoria {cat!r} nao existe para lang={lang} "
                   f"(validas: {', '.join(sorted(CATEGORIAS[lang]))})")

        if lang == "en" and "permalink" not in fm:
            err(1, "post EN sem `permalink:` (obrigatorio)")

        # --- par bilingue, pelo translation (o nome do arquivo NAO e confiavel:
        #     ha pares com slug traduzido, ex. oficial/official) ---
        tr = fm.get("translation")
        if tr:
            if tr not in urls:
                err(1, f"`translation: {tr}` nao aponta para nenhum post existente")
        else:
            avisos.append((rel, 1, "sem `translation:` — post sem par no outro idioma"))

        # --- imagem declarada existe no disco ---
        img = fm.get("image")
        if img and not (REPO / img.lstrip("/")).exists():
            err(1, f"`image: {img}` nao existe no disco")
        for m in re.finditer(r"!\[[^\]]*\]\((/assets/[^)]+)\)", corpo):
            if not (REPO / m.group(1).lstrip("/")).exists():
                err(off + corpo[:m.start()].count("\n"), f"imagem {m.group(1)} nao existe no disco")

        # --- marcas de texto gerado ---
        for rx, msg in TELLS:
            for m in rx.finditer(corpo):
                linha = off + corpo[: m.start()].count("\n")
                trecho = corpo[max(0, m.start() - 30): m.start() + 40].replace("\n", " ").strip()
                err(linha, f"{msg} → ...{trecho}...")

    return erros, avisos


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="so imprime problemas")
    args = ap.parse_args()

    erros, avisos = checar()

    for rel, linha, msg in avisos:
        print(f"aviso  {rel}:{linha}: {msg}")
    for rel, linha, msg in erros:
        print(f"ERRO   {rel}:{linha}: {msg}")

    n = len(list(POSTS.glob("*.md")))
    if erros:
        print(f"\n{len(erros)} erro(s) em {n} posts. Gate REPROVADO.")
        return 1
    if not args.quiet:
        print(f"conteudo OK: {n} posts, 0 erros, {len(avisos)} aviso(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
