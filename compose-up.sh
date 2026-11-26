#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

exec \
  podman-compose \
  --file=compose.yml \
  --file=compose."${1}".yml \
  up \
  "${@:2}"
