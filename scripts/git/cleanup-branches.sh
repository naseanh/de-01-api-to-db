#!/usr/bin/env bash

# =========================================================
# Remote Branch Cleanup
# Deletes all remote branches except:
# - origin/main
# - origin/HEAD
# =========================================================

git branch -r \
| grep -v "origin/main" \
| grep -v "origin/HEAD" \
| sed 's/origin\///' \
| xargs -I {} git push origin --delete {}

# =========================================================
# Local Branch Cleanup
# Deletes all merged local branches except:
# - current branch
# - main
# =========================================================

git branch --merged \
| grep -v "\\*" \
| grep -v "main" \
| xargs git branch -d

# =========================================================
# Remove stale references
# =========================================================

git fetch --prune

echo "Branch cleanup complete."