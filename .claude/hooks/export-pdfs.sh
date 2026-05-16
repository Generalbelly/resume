#!/bin/bash
set -e

cd "$(git rev-parse --show-toplevel)"

gws drive files export \
  --params '{"fileId": "1lkghEoKXK8vqbNfuEZe2LljkRcltqW6zjfyl_qXkysM", "mimeType": "application/pdf"}' \
  -o Resume.pdf 2>/dev/null

gws drive files export \
  --params '{"fileId": "1AxoYYL_iyoD5UPFFEo3wpytBcWyohLfNwmuAPAQcdYE", "mimeType": "application/pdf"}' \
  -o 職務経歴書.pdf 2>/dev/null

git add Resume.pdf 職務経歴書.pdf

if ! git diff --cached --quiet; then
  git commit -m "chore: Refresh PDFs"
fi
