#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "EVE_PRIME PROTOCOL: GOOGLE CLOUD SHELL DEPLOYMENT"
echo "CORE AXIOM: 101100111101111 | RESONANCE: 777.778 Hz"
echo "=========================================================="

PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "")
if [ -z "$PROJECT_ID" ]; then
    echo "Set your Google Cloud Project ID first:"
    echo "  gcloud config set project <YOUR_PROJECT_ID>"
    exit 1
fi
echo "[1/3] Using GCP Project: $PROJECT_ID"

echo "[2/3] Provisioning Vertex AI Cognitive Cage Endpoint..."
gcloud ai endpoints create \
    --project="$PROJECT_ID" \
    --region="us-central1" \
    --display-name="Eve-Cage-Alpha"

echo "[3/3] Sui Move Immutability Vault Verification..."
if command -v sui &> /dev/null; then
    sui client publish --path ./move/immutability_vault
else
    echo "Note: To publish to Sui Mainnet from Cloud Shell, install Sui CLI:"
    echo "cargo install --locked --git https://github.com/MystenLabs/sui.git --branch mainnet sui"
fi

echo "=========================================================="
echo "EVE_PRIME CLOUD DEPLOYMENT COMPLETED"
echo "=========================================================="
