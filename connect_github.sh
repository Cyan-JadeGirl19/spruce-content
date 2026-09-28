#!/bin/bash
# One-command GitHub connect:
#   ./connect_github.sh https://github.com/<you>/<repo>.git ghp_yourToken [branch]
# Token: create a Fine-grained PAT → github.com/settings/personal-access-tokens
#   → Repository access: only the repo → Permissions: Contents = Read & Write.
# NOTE: the token is used only for this push and is NOT stored in any file.
set -e
URL="$1"; TOKEN="$2"; BR="${3:-main}"
if [ -z "$URL" ] || [ -z "$TOKEN" ]; then
  echo "usage: ./connect_github.sh <repo-url> <personal-access-token> [branch=main]"; exit 1
fi
cd "$(dirname "$0")"
git remote remove origin 2>/dev/null || true
git remote add origin "https://x-access-token:${TOKEN}@${URL#https://}"
if [ ! -d .git/objects ] || [ -z "$(git log --oneline -1 2>/dev/null)" ]; then
  git -c user.name="Spruce Media" -c user.email="media@spruce.example" commit -m "Spruce Oct 2026 content system: 80 graphics, 8 videos, calendar, design engine"
fi
git branch -M "$BR" 2>/dev/null || true
git -c user.name="Spruce Media" -c user.email="media@spruce.example" push -u origin "$BR" 2>&1 | sed "s/${TOKEN}/***TOKEN***/g"
git remote remove origin
echo "✅ Pushed to $URL (token not stored anywhere)"
