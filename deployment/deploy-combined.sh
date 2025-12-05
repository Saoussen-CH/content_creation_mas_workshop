#!/bin/bash

# Deploy combined frontend + backend to Google Cloud Run
# This script builds and deploys a single service containing both React frontend and FastAPI backend

set -e

echo "🚀 Deploying Content Creation Studio (Combined Frontend + Backend) to Cloud Run"
echo "=============================================================================="

# Load environment variables
if [ -f ../.env ]; then
    echo "📋 Loading environment variables from .env file..."
    export $(cat ../.env | grep -v '^#' | xargs)
else
    echo "⚠️  Warning: .env file not found. Using existing environment variables."
fi

# Check required environment variables
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "❌ Error: GOOGLE_CLOUD_PROJECT is not set"
    echo "Please set it in your .env file or export it:"
    echo "  export GOOGLE_CLOUD_PROJECT=your-project-id"
    exit 1
fi

if [ -z "$AGENT_ENGINE_RESOURCE_NAME" ]; then
    echo "⚠️  Warning: AGENT_ENGINE_RESOURCE_NAME is not set"
    echo "The service will deploy but won't be able to connect to the agent."
    echo "Deploy your agent first using: python deployment/deploy.py"
fi

# Set defaults
REGION="${GOOGLE_CLOUD_LOCATION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-content-studio}"

# Use Artifact Registry (recommended) or fall back to GCR
USE_ARTIFACT_REGISTRY="${USE_ARTIFACT_REGISTRY:-true}"

if [ "$USE_ARTIFACT_REGISTRY" = "true" ]; then
    IMAGE_NAME="${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/content-studio/${SERVICE_NAME}"
    REGISTRY_TYPE="Artifact Registry"
else
    IMAGE_NAME="gcr.io/${GOOGLE_CLOUD_PROJECT}/${SERVICE_NAME}"
    REGISTRY_TYPE="Container Registry (GCR)"
fi

echo ""
echo "📝 Configuration:"
echo "  Project: $GOOGLE_CLOUD_PROJECT"
echo "  Region: $REGION"
echo "  Service Name: $SERVICE_NAME"
echo "  Registry: $REGISTRY_TYPE"
echo "  Image: $IMAGE_NAME"
echo "  Agent Resource: ${AGENT_ENGINE_RESOURCE_NAME:-Not configured}"
echo ""

# Navigate to project root
cd "$(dirname "$0")/.."

# Confirm deployment
read -p "Deploy to Cloud Run? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "🔐 Step 1/5: Configuring Docker Authentication..."
echo "------------------------------------------------"
if [ "$USE_ARTIFACT_REGISTRY" = "true" ]; then
    echo "Authenticating with Artifact Registry..."
    gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
else
    echo "Authenticating with Container Registry (GCR)..."
    gcloud auth configure-docker gcr.io --quiet
fi
echo "✅ Docker authentication configured"

echo ""
echo "🔨 Step 2/5: Building Docker image..."
echo "------------------------------------"
docker build -t "$IMAGE_NAME" -f Dockerfile .

echo ""
echo "📤 Step 3/5: Pushing image to registry..."
echo "-----------------------------------------"
docker push "$IMAGE_NAME"

echo ""
echo "🚀 Step 4/5: Deploying to Cloud Run..."
echo "--------------------------------------"

# Build the gcloud command with environment variables
GCLOUD_CMD="gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 3600 \
    --max-instances 10 \
    --min-instances 0"

# Add environment variables if they exist
if [ ! -z "$AGENT_ENGINE_RESOURCE_NAME" ]; then
    GCLOUD_CMD="$GCLOUD_CMD --set-env-vars AGENT_RESOURCE_NAME=$AGENT_ENGINE_RESOURCE_NAME"
fi

if [ ! -z "$GOOGLE_CLOUD_PROJECT" ]; then
    GCLOUD_CMD="$GCLOUD_CMD --set-env-vars GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT"
fi

if [ ! -z "$GOOGLE_CLOUD_LOCATION" ]; then
    GCLOUD_CMD="$GCLOUD_CMD --set-env-vars GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION"
fi

if [ ! -z "$WORKER_MODEL" ]; then
    GCLOUD_CMD="$GCLOUD_CMD --set-env-vars WORKER_MODEL=$WORKER_MODEL"
fi

if [ ! -z "$COORDINATOR_MODEL" ]; then
    GCLOUD_CMD="$GCLOUD_CMD --set-env-vars COORDINATOR_MODEL=$COORDINATOR_MODEL"
fi

# Execute deployment
eval $GCLOUD_CMD

echo ""
echo "✅ Step 5/5: Retrieving service URL..."
echo "-------------------------------------"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')

echo ""
echo "=============================================================================="
echo "✅ Deployment Complete!"
echo "=============================================================================="
echo ""
echo "🌐 Service URL: $SERVICE_URL"
echo ""
echo "📋 Next steps:"
echo "  1. Open the URL above in your browser to use the Content Studio"
echo "  2. The frontend and backend are now served from a single service"
echo "  3. API endpoints are available at: $SERVICE_URL/api/*"
echo "  4. Health check: $SERVICE_URL/health"
echo ""
echo "🔧 To update the deployment:"
echo "  ./deployment/deploy-combined.sh"
echo ""
echo "📊 To view logs:"
echo "  gcloud run services logs read $SERVICE_NAME --region $REGION"
echo ""
echo "🗑️  To delete the service:"
echo "  gcloud run services delete $SERVICE_NAME --region $REGION"
echo ""
