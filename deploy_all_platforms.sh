#!/usr/bin/env bash
set -euo pipefail

echo "=== [1/4] Google Cloud & Vertex AI Deployment ==="
gcloud config set project steady-catbird-6sx2c || true
gcloud ai endpoints create --project=steady-catbird-6sx2c --region=us-central1 --display-name="Eve-Cage-Alpha" || true

echo "=== [2/4] Antigravity & Sui Immutability Vault ==="
if command -v sui &> /dev/null; then
    sui client publish --path ./move/immutability_vault
fi

echo "=== [3/4] Vercel Edge Matrix Deployment ==="
if command -v vercel &> /dev/null; then
    vercel --prod --yes
else
    echo "Run 'npm i -g vercel && vercel' to link to your Vercel team."
fi

echo "=== [4/4] GitHub Synchronization ==="
git add .
git commit -m "feat: add Vercel manifest, Gumroad monetization tiers, and multi-platform orchestration" || true
git push origin main
