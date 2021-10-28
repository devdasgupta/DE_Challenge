#!/bin/sh

main() {
  [ $# -lt 1 ] && run_cli
  case "$1" in
    -*) run_cli "$@";;
    *) exec "$@";;
  esac
}

run_cli() {
  exec python "$@"
}

main "$@"
