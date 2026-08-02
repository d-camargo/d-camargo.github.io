#!/usr/bin/env bash
# Preview local do site na VPS, via container podman (nao ha ruby instalado no host).
#
# Uso:
#   ./serve.sh              # sobe o servidor em 127.0.0.1:4000
#   ./serve.sh --build      # so gera _site/ e sai
#
# Para ver do notebook, abra um tunel SSH na sua maquina:
#   ssh -L 4000:localhost:4000 -L 35729:localhost:35729 diego@<ip-da-vps>
# e acesse http://localhost:4000
set -euo pipefail

cd "$(dirname "$0")"

IMAGE=docker.io/library/ruby:3.3
PORT=${PORT:-4000}

# $2: "portas" publica 4000/35729 (so o serve precisa). O --build roda sem
# publicar nada — senao um preview ja rodando na 4000 faz o build falhar com
# "address already in use", e build nao usa porta nenhuma.
run() {
  local portas=()
  if [[ "${2:-}" == "portas" ]]; then
    portas=(-p 127.0.0.1:"$PORT":"$PORT" -p 127.0.0.1:35729:35729)
  fi
  podman run --rm -i \
    -v "$PWD":/site:Z \
    -w /site \
    -e BUNDLE_PATH=/site/vendor/bundle \
    -e BUNDLE_APP_CONFIG=/site/.bundle \
    "${portas[@]}" \
    "$IMAGE" bash -lc "$1"
}

if [[ "${1:-}" == "--build" ]]; then
  run "bundle check >/dev/null 2>&1 || bundle install --quiet; bundle exec jekyll build"
  echo "Site gerado em _site/"
else
  run "bundle check >/dev/null 2>&1 || bundle install --quiet; bundle exec jekyll serve --host 0.0.0.0 --port $PORT --livereload --force_polling" portas
fi
