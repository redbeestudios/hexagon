#!/usr/bin/env bash

for locale in locales/**/LC_MESSAGES/hexagon.po; do
  grep -Hin 'msgstr ""' "$locale" >>errors.txt
done

if [ -s errors.txt ]; then
  while IFS="" read -r p || [ -n "$p" ]; do
    # the first match is always on line 6 and empty
    if [[ "$p" != *".po:6:"* ]]; then printf '%s\n' "$p:translation string should not be empty"; fi
  done <errors.txt
  exit 1
else
  echo "🥳 all strings have a translation 🗺"
  exit 0
fi
