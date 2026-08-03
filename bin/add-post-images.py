#!/usr/bin/env python3
"""Importa prints de tela numerados para a pasta de imagens de um post.

Complementa o gen-post-image.py: aquele gera a capa (uma imagem por post, na
raiz de assets/images/posts/); este organiza as telas que ilustram o corpo do
texto, que vao numeradas numa subpasta propria — o padrao ja usado em
assets/images/posts/sigbus01/ (1.webp, 2.webp, ...).

Fluxo de uso. Os prints chegam pelo Discord, e o Hermes os baixa em
~/.hermes/cache/images/ com nome de hash (img_<hash>.png), sem ordem util no
nome — mas na ordem em que foram anexados na mensagem. Quando essa e a ordem
desejada, basta dizer quantos vieram:

    bin/add-post-images.py --slug sigbus02 --from-cache 3

O script mostra qual arquivo virou qual numero, para conferencia. Quando a
ordem for outra, o numero vai explicito, arquivo a arquivo:

    bin/add-post-images.py --slug sigbus02 \\
        1=~/.hermes/cache/images/img_a1b2.png \\
        2=~/.hermes/cache/images/img_c3d4.png

No rascunho do post, cada imagem e marcada no ponto exato onde deve aparecer:

    [[print 2: alt text da imagem]]

e o --apply troca os marcadores pelo markdown correspondente, ja apontando
para o arquivo no disco:

    bin/add-post-images.py --slug sigbus02 --apply _posts/2026-08-05-post.md

O par PT/EN compartilha a mesma pasta de imagens: rode o --apply nos dois
arquivos, cada um com o seu alt text no idioma do post.

    bin/add-post-images.py --slug sigbus02 --list    # o que ja esta na pasta
"""

import argparse
import io
import re
import sys
import time
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "_posts"
DEFAULT_OUTDIR = REPO_ROOT / "assets" / "images" / "posts"
# Onde o Hermes grava os anexos que chegam pelo Discord.
HERMES_CACHE = str(Path.home() / ".hermes" / "cache" / "images")

# [[print 2: alt text]] — aceita img/imagem como sinonimos de print.
MARKER = re.compile(r"\[\[\s*(?:print|img|imagem)\s+(\d+)\s*:\s*([^\]]+?)\s*\]\]", re.I)

# O mesmo print ja resolvido em markdown, de um --apply anterior. Mesma forma
# que o bin/check-content.py procura no gate.
RESOLVIDO = re.compile(r"!\[[^\]]*\]\(/assets/images/posts/([^/)]+)/(\d+)\.\w+\)")

# Ladder de qualidade do lossy. Comeca mais alto que o da capa: print de tela
# tem texto de interface, e artefato em texto pequeno aparece antes que em
# ilustracao.
QUALITY_LADDER = (92, 88, 82, 76, 70)

# Intervalo, em minutos, acima do qual dois prints seguidos do --from-cache
# provavelmente NAO vieram da mesma mensagem. Anexos de uma mensagem so sao
# gravados com segundos de diferenca.
GAP_ALERTA_MIN = 15


def rel(caminho):
    """Caminho relativo a raiz do repo, para mensagem curta; absoluto se estiver fora."""
    try:
        return caminho.relative_to(REPO_ROOT)
    except ValueError:
        return caminho


def to_webp(origem, dest, max_width, max_kb):
    """Converte para WebP, redimensiona e devolve (tamanho, kb, rotulo de qualidade).

    Tenta lossless primeiro: em print de tela, area chapada comprime bem e o
    texto da interface sai perfeito. So cai para o lossy quando o lossless
    estoura o teto de tamanho.
    """
    image = Image.open(io.BytesIO(origem)).convert("RGB")
    if image.width > max_width:
        height = round(image.height * max_width / image.width)
        image = image.resize((max_width, height), Image.LANCZOS)

    buffer = io.BytesIO()
    image.save(buffer, "WEBP", lossless=True, method=6)
    rotulo = "lossless"

    if buffer.tell() > max_kb * 1024:
        for quality in QUALITY_LADDER:
            buffer = io.BytesIO()
            image.save(buffer, "WEBP", quality=quality, method=6)
            rotulo = f"q{quality}"
            if buffer.tell() <= max_kb * 1024:
                break

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(buffer.getvalue())
    return image.size, buffer.tell() / 1024, rotulo


def parse_pares(itens):
    """Traduz os argumentos posicionais em {numero: caminho}.

    Forma padrao: `N=caminho`. Caminhos soltos sao numerados na ordem em que
    aparecem, mas misturar as duas formas e erro: o numero de um print e
    informacao demais para sair de uma inferencia silenciosa.
    """
    com_numero = [i for i in itens if re.match(r"^\d+=", i)]
    if com_numero and len(com_numero) != len(itens):
        sys.exit("erro: nao misture `N=caminho` com caminhos soltos — "
                 "ou todos levam numero, ou nenhum leva.")

    mapa = {}
    for posicao, item in enumerate(itens, start=1):
        if com_numero:
            numero, _, caminho = item.partition("=")
            numero = int(numero)
            if numero < 1:
                sys.exit(f"erro: numero invalido em {item!r} (a sequencia comeca em 1).")
        else:
            numero, caminho = posicao, item

        if numero in mapa:
            sys.exit(f"erro: numero {numero} informado duas vezes.")
        origem = Path(caminho).expanduser()
        if not origem.is_file():
            sys.exit(f"erro: {origem} nao existe.")
        mapa[numero] = origem
    return mapa


def arquivo_do_numero(pasta, numero):
    """Devolve o arquivo `numero.*` que ja esta na pasta, se houver.

    Aceita qualquer extensao porque os conjuntos antigos sao .png; os novos
    saem em .webp.
    """
    achados = sorted(pasta.glob(f"{numero}.*"))
    return achados[0] if achados else None


def importar(pasta, mapa, args):
    if not args.force:
        ocupados = [n for n in sorted(mapa) if arquivo_do_numero(pasta, n)]
        if ocupados:
            existentes = ", ".join(arquivo_do_numero(pasta, n).name for n in ocupados)
            sys.exit(f"erro: {existentes} ja existe(m) em {rel(pasta)}. "
                     f"Use --force para substituir, ou outro numero.")

    escritos = []
    for numero in sorted(mapa):
        origem = mapa[numero]
        # Um numero so pode ter um arquivo: se o antigo era .png, ele sai.
        antigo = arquivo_do_numero(pasta, numero)
        if antigo and antigo.suffix != ".webp":
            antigo.unlink()
            print(f"  removido {antigo.name} (substituido pelo webp)", file=sys.stderr)

        dest = pasta / f"{numero}.webp"
        (w, h), kb, rotulo = to_webp(origem.read_bytes(), dest, args.max_width, args.max_kb)
        print(f"  {numero}.webp — {w}x{h}, {kb:.0f} KB, {rotulo}  <- {origem.name}",
              file=sys.stderr)
        escritos.append(numero)
    return escritos


def aplicar(pasta, slug, caminho_post):
    """Troca os marcadores [[print N: alt]] do post pelo markdown da imagem."""
    post = Path(caminho_post)
    if not post.is_file():
        post = POSTS_DIR / caminho_post
    if not post.is_file():
        sys.exit(f"erro: post {caminho_post} nao encontrado.")

    texto = post.read_text()
    marcadores = list(MARKER.finditer(texto))
    if not marcadores:
        print(f"aviso: nenhum marcador [[print N: ...]] em {post.name}", file=sys.stderr)
        return 0

    # 1, 2, 3... na ordem de leitura, sem pulo e sem repeticao: e o que faz "a
    # imagem 3" do texto ser a terceira imagem que o leitor encontra. Mesma
    # regra que o bin/check-content.py cobra no gate, para que os dois nunca
    # discordem. Os prints ja resolvidos por um --apply anterior contam na
    # sequencia; sem isso, acrescentar prints a um post pronto (o caso do
    # --start) daria falso "fora da sequencia".
    pendentes = [int(m.group(1)) for m in marcadores]
    leitura = sorted([(m.start(), int(m.group(2))) for m in RESOLVIDO.finditer(texto)
                      if m.group(1) == slug]
                     + [(m.start(), n) for m, n in zip(marcadores, pendentes)])
    numeros = [n for _, n in leitura]
    esperado = list(range(1, len(numeros) + 1))
    if numeros != esperado:
        sys.exit(f"erro: em {post.name} os prints de {slug}/ estao fora da sequencia "
                 f"({', '.join(map(str, numeros))}, contando os ja resolvidos); "
                 f"o padrao e {', '.join(map(str, esperado))}, na ordem de leitura. "
                 f"Renumere; nada foi escrito.")

    faltando = [n for n in pendentes if not arquivo_do_numero(pasta, n)]
    if faltando:
        disponiveis = ", ".join(sorted(p.name for p in pasta.glob("*.*"))) or "(pasta vazia)"
        sys.exit(f"erro: {post.name} referencia print(s) {', '.join(map(str, faltando))}, "
                 f"que nao estao em {rel(pasta)}. Na pasta: {disponiveis}. "
                 f"Importe antes de aplicar; nada foi escrito.")

    def troca(m):
        arquivo = arquivo_do_numero(pasta, int(m.group(1)))
        return f"![{m.group(2)}](/assets/images/posts/{slug}/{arquivo.name})"

    post.write_text(MARKER.sub(troca, texto))
    print(f"  {post.name} — {len(marcadores)} marcador(es) resolvido(s): "
          f"{', '.join(map(str, pendentes))}", file=sys.stderr)
    return len(marcadores)


def do_cache(quantos, cache_dir, inicio):
    """Pega os `quantos` prints mais recentes do cache do Hermes, em ordem de chegada.

    Anexo de Discord vira arquivo com nome de hash, mas o Hermes os grava na
    ordem em que vieram na mensagem, entao a data de modificacao preserva a
    ordem em que o Diego anexou. Evita que um modelo tenha que transcrever
    caminho de hash na mao, que e onde esse tipo de fluxo costuma errar.

    ATENCAO: o cache e UM SO, global (get_image_cache_dir do Hermes) — nao ha
    pasta por canal nem por topico, e o nome do arquivo (img_<uuid>.png) nao
    diz de onde veio. Imagem mandada em qualquer outro canal cai na mesma pilha
    e pode entrar aqui. Dai o mapa impresso e o alerta de intervalo: a falha
    seria silenciosa, com a imagem errada no numero certo.
    """
    cache = Path(cache_dir).expanduser()
    if not cache.is_dir():
        sys.exit(f"erro: {cache} nao existe — informe --cache-dir.")

    imagens = [p for p in cache.iterdir()
               if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}]
    if len(imagens) < quantos:
        sys.exit(f"erro: --from-cache {quantos}, mas ha {len(imagens)} imagem(ns) em {cache}.")

    recentes = sorted(imagens, key=lambda p: p.stat().st_mtime)[-quantos:]
    agora = time.time()
    print(f"do cache {cache} (mais antigo primeiro = ordem em que foram anexados):",
          file=sys.stderr)
    anterior = None
    furos = []
    for numero, origem in enumerate(recentes, start=inicio):
        mtime = origem.stat().st_mtime
        idade = (agora - mtime) / 60
        marca = "  <-- confira: nao chegou agora" if idade > 360 else ""
        if anterior is not None and (mtime - anterior) / 60 > GAP_ALERTA_MIN:
            marca += f"  <-- {(mtime - anterior) / 60:.0f} min depois do anterior"
            furos.append(numero)
        print(f"  {numero} <- {origem.name}  ({idade:.0f} min atras){marca}", file=sys.stderr)
        anterior = mtime

    if furos:
        print(f"AVISO: {len(furos)} print(s) com intervalo grande para o anterior — o "
              f"cache do Hermes e global (toda imagem de todo canal cai nele), entao "
              f"pode haver imagem de outra conversa no meio. Confira o mapa acima antes "
              f"de seguir; se estiver errado, apague a pasta e refaca com `N=arquivo`.",
              file=sys.stderr)
    return {numero: origem for numero, origem in enumerate(recentes, start=inicio)}


def listar(pasta, slug):
    arquivos = sorted(pasta.glob("*.*"), key=lambda p: (len(p.stem), p.stem))
    if not arquivos:
        print(f"{rel(pasta)} esta vazia.")
        return
    print(f"{rel(pasta)}:")
    for arquivo in arquivos:
        kb = arquivo.stat().st_size / 1024
        print(f"  {arquivo.name:<12} {kb:>7.0f} KB   /assets/images/posts/{slug}/{arquivo.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pares", nargs="*", metavar="N=ARQUIVO",
                        help="prints a importar, ex: 1=~/.hermes/cache/images/img_a1b2.png")
    parser.add_argument("--slug", required=True,
                        help="nome da subpasta do conjunto em assets/images/posts/, ex: sigbus02")
    parser.add_argument("--apply", action="append", default=[], metavar="POST",
                        help="troca os marcadores [[print N: alt]] deste post pelo markdown "
                             "da imagem; repita para o par PT/EN")
    parser.add_argument("--from-cache", type=int, metavar="N",
                        help="importa os N prints mais recentes do cache do Hermes, "
                             "na ordem em que foram anexados no Discord")
    parser.add_argument("--start", type=int, default=1, metavar="N",
                        help="numero do primeiro print com --from-cache (default: 1); "
                             "use para acrescentar a um conjunto que ja existe")
    parser.add_argument("--cache-dir", default=HERMES_CACHE,
                        help=f"onde o Hermes grava os anexos (default: {HERMES_CACHE})")
    parser.add_argument("--list", action="store_true", help="mostra o que ja esta na pasta")
    parser.add_argument("--force", action="store_true",
                        help="substitui numeros que ja existem na pasta")
    parser.add_argument("--max-width", type=int, default=1600, help="largura maxima em px")
    parser.add_argument("--max-kb", type=int, default=300,
                        help="teto do WebP; acima disso cai do lossless para o lossy")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    args = parser.parse_args()

    if "/" in args.slug or args.slug.startswith("."):
        sys.exit("erro: --slug e o nome de uma subpasta, sem barras.")

    if args.pares and args.from_cache:
        sys.exit("erro: --from-cache pega os arquivos sozinho; nao passe caminhos junto.")
    if args.from_cache is not None and args.from_cache < 1:
        sys.exit("erro: --from-cache espera quantos prints importar (1 ou mais).")
    if args.start < 1:
        sys.exit("erro: --start comeca em 1.")

    importando = bool(args.pares or args.from_cache)
    pasta = args.outdir / args.slug
    if not (importando or args.apply or args.list):
        parser.error("informe prints para importar, --from-cache, --apply, ou --list.")
    if not pasta.exists() and not importando:
        sys.exit(f"erro: {rel(pasta)} nao existe — importe os prints primeiro.")

    escritos = []
    if importando:
        mapa = (do_cache(args.from_cache, args.cache_dir, args.start) if args.from_cache
                else parse_pares(args.pares))
        pasta.mkdir(parents=True, exist_ok=True)
        print(f"importando para {rel(pasta)}/", file=sys.stderr)
        escritos = importar(pasta, mapa, args)

    for post in args.apply:
        aplicar(pasta, args.slug, post)

    if args.list:
        listar(pasta, args.slug)
    elif escritos and not args.apply:
        print("\n--- marcadores para colar no rascunho, no ponto exato de cada imagem ---")
        for numero in escritos:
            print(f"[[print {numero}: descreva a tela]]")
        print("\ndepois: bin/add-post-images.py --slug "
              f"{args.slug} --apply _posts/<post>.md")


if __name__ == "__main__":
    main()
