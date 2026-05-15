#!/usr/bin/env bash

set -e

echo "========================================="
echo "Remote Branch Cleanup"
echo "========================================="

git branch -r \
| grep -v "origin/main" \
| grep -v "origin/HEAD" \
| sed 's/origin\///' \
| xargs -I {} git push origin --delete {}

echo ""
echo "========================================="
echo "Local Branch Cleanup"
echo "========================================="

git branch \
| grep -v "\\*" \
| grep -v "main" \
| xargs git branch -D

echo ""
echo "========================================="
echo "Pruning stale references"
echo "========================================="

git fetch --prune

echo ""
echo "Branch cleanup complete."