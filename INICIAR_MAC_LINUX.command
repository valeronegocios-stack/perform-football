#!/bin/bash
set -e
cd "$(dirname "$0")"
if ! command -v node >/dev/null 2>&1; then
  echo "Necesitas instalar Node.js 20.6 o superior: https://nodejs.org/"
  exit 1
fi
if [ ! -f ".env" ]; then
  node configurar-ia.mjs
fi
echo "Abre http://127.0.0.1:4173 en tu navegador."
node --env-file=.env server.mjs
