#!/bin/bash

# Quick script to configure Docker authentication for Google Cloud
# Run this if you get "Unauthenticated request" errors when pushing Docker images

set -e

echo "🔐 Configuring Docker Authentication for Google Cloud"
echo "====================================================="
echo ""

# Load environment variables
if [ -f ../.env ]; then
    echo "📋 Loading environment variables from .env file..."
    export $(cat ../.env | grep -v '^#' | xargs)
fi

# Check if project is set
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "❌ Error: GOOGLE_CLOUD_PROJECT is not set"
    echo "Please set it in your .env file or export it:"
    echo "  export GOOGLE_CLOUD_PROJECT=your-project-id"
    exit 1
fi

REGION="${GOOGLE_CLOUD_LOCATION:-us-central1}"

echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Region: $REGION"
echo ""

# Authenticate with gcloud
echo "Step 1: Checking gcloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "⚠️  No active gcloud authentication found"
    echo "Running: gcloud auth login"
    gcloud auth login
else
    ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n 1)
    echo "✅ Already authenticated as: $ACTIVE_ACCOUNT"
fi

echo ""
echo "Step 2: Setting active project..."
gcloud config set project $GOOGLE_CLOUD_PROJECT
echo "✅ Active project: $GOOGLE_CLOUD_PROJECT"

echo ""
echo "Step 3: Configuring Docker for Artifact Registry..."
gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
echo "✅ Artifact Registry configured: ${REGION}-docker.pkg.dev"

echo ""
echo "Step 4: Configuring Docker for Container Registry (GCR)..."
gcloud auth configure-docker gcr.io --quiet
echo "✅ Container Registry configured: gcr.io"

echo ""
echo "Step 5: Refreshing application-default credentials..."
gcloud auth application-default login
echo "✅ Application-default credentials refreshed"

echo ""
echo "=============================================="
echo "✅ Docker Authentication Configured!"
echo "=============================================="
echo ""
echo "You can now push Docker images to:"
echo "  - Artifact Registry: ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/..."
echo "  - Container Registry: gcr.io/${GOOGLE_CLOUD_PROJECT}/..."
echo ""
echo "Next steps:"
echo "  1. Run: ./deploy-combined.sh"
echo "  2. Or manually build and push:"
echo "     docker build -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/content-studio/content-studio ."
echo "     docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/content-studio/content-studio"
echo ""
