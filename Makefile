# Gate de verificacao do site.
#
# Existe principalmente para o motor do Hermes: o `detect_test_cmd` do
# planexec.py procura `test/test_*.py` ou um alvo `test:` num Makefile. Sem um
# dos dois, `run_tests` devolve None, e no `do_review` a expressao
# `approved = said_ok and (ok2 is not False)` aprova na palavra do Opus, sem
# fato nenhum por tras. Como aqui o push publica direto em producao
# (gh-pages -> dcamargo.com.br), um template Liquid quebrado iria ao ar.
#
# `jekyll build` sai != 0 em erro de Liquid, frontmatter invalido ou include
# ausente, entao ele e o gate honesto deste projeto.

.PHONY: test build serve

test: build

build:
	./serve.sh --build

serve:
	./serve.sh
