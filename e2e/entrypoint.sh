#!/usr/bin/env bash

set -e

if [ -f "/app/out/$TEST_NAME.asc" ]; then
  asciinema rec -q "/app/out/$TEST_NAME.asc" --append -c "$@"
else
  asciinema rec -q "/app/out/$TEST_NAME.asc" -c "$@"
fi
