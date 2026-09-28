# Connecting this repo to GitHub

## Option A — I push it for you (give me 2 things)
1. **The repo URL** — e.g. `https://github.com/yourname/spruce-content.git`
   (create it at github.com/new — empty repo, no README, private recommended)
2. **A Fine-grained Personal Access Token** — create at:
   github.com/settings/personal-access-tokens/new
   - Token name: `spruce-push`
   - Expiration: 7 days (short!)
   - Repository access: *Only select repositories* → pick the new repo
   - Permissions → Repository → **Contents: Read and write**
   Then run (or paste the URL+token in chat and I'll run it):
   ```
   ./connect_github.sh https://github.com/you/spruce-content.git ghp_xxx main
   ```
   The script pushes, then **removes the remote so the token is never stored**.
   Revoke the token afterwards for full safety.

## Option B — push it yourself from your own machine
1. Download the workspace folder `spruce/`
2. `cd spruce && git init -b main && git add -A && git commit -m "Spruce Oct 2026 content system"`
3. `git remote add origin https://github.com/you/spruce-content.git`
4. `git push -u origin main` (browser login or your own token)

## Option C — GitHub Desktop (no terminal)
Download the folder → GitHub Desktop → File → Add local repository →
select the `spruce` folder → Publish repository.
