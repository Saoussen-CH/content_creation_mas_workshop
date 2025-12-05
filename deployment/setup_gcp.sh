#!/bin/bash

# Google Cloud Platform Setup Script
# Sets up all required APIs, service accounts, and permissions for Content Creation Studio

set -e

echo "=========================================="
echo "  GCP Setup for Content Creation Studio"
echo "=========================================="
echo ""

# Load environment variables from .env file
# Try deployment/.env first, then parent .env
if [ -f "./.env" ]; then
    echo "Loading environment variables from deployment/.env..."
    set -a
    source ./.env 2>/dev/null || true
    set +a
elif [ -f "../.env" ]; then
    echo "Loading environment variables from ../.env..."
    set -a
    source ../.env 2>/dev/null || true
    set +a
fi

# Check required environment variables
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "Error: GOOGLE_CLOUD_PROJECT not set"
    echo "Set it in .env file or export GOOGLE_CLOUD_PROJECT='your-project-id'"
    exit 1
fi

# Set defaults
REGION=${GOOGLE_CLOUD_LOCATION:-us-central1}

echo "Configuration:"
echo "   Project: $GOOGLE_CLOUD_PROJECT"
echo "   Region: $REGION"
echo ""

# Confirm setup
read -p "Proceed with GCP setup? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

echo ""
echo "=========================================="
echo "Step 1: Set Default Project"
echo "=========================================="
echo ""

gcloud config set project $GOOGLE_CLOUD_PROJECT
echo "Default project set to: $GOOGLE_CLOUD_PROJECT"

echo ""
echo "=========================================="
echo "Step 2: Enable Required APIs"
echo "=========================================="
echo ""

APIS=(
    "aiplatform.googleapis.com"           # Vertex AI / Agent Engine
    "run.googleapis.com"                  # Cloud Run
    "cloudbuild.googleapis.com"           # Cloud Build
    "artifactregistry.googleapis.com"     # Artifact Registry (replaces GCR)
    "storage.googleapis.com"              # Cloud Storage
    "iam.googleapis.com"                  # IAM
    "cloudresourcemanager.googleapis.com" # Resource Manager
)

echo "Enabling APIs (this may take a few minutes)..."
for api in "${APIS[@]}"; do
    echo "  - Enabling $api..."
    gcloud services enable $api --project=$GOOGLE_CLOUD_PROJECT
done

echo "All APIs enabled successfully!"

echo ""
echo "=========================================="
echo "Step 3: Create Artifact Registry Repository"
echo "=========================================="
echo ""

# Check if repository exists
if gcloud artifacts repositories describe content-studio \
    --location=$REGION \
    --project=$GOOGLE_CLOUD_PROJECT &>/dev/null; then
    echo "Artifact Registry repository 'content-studio' already exists"
else
    echo "Creating Artifact Registry repository..."
    gcloud artifacts repositories create content-studio \
        --repository-format=docker \
        --location=$REGION \
        --description="Docker repository for Content Creation Studio" \
        --project=$GOOGLE_CLOUD_PROJECT
    echo "Artifact Registry repository created!"
fi

echo ""
echo "=========================================="
echo "Step 4: Configure Docker Authentication"
echo "=========================================="
echo ""

echo "Configuring Docker to authenticate with Artifact Registry..."
gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

echo ""
echo "Configuring Docker for legacy GCR (gcr.io) if needed..."
gcloud auth configure-docker gcr.io --quiet

echo ""
echo "=========================================="
echo "Step 5: Create Service Account (Optional)"
echo "=========================================="
echo ""

SERVICE_ACCOUNT_NAME="content-studio-sa"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com"

# Check if service account exists
if gcloud iam service-accounts describe $SERVICE_ACCOUNT_EMAIL \
    --project=$GOOGLE_CLOUD_PROJECT &>/dev/null; then
    echo "Service account '$SERVICE_ACCOUNT_NAME' already exists"
else
    echo "Creating service account..."
    gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
        --display-name="Content Creation Studio Service Account" \
        --description="Service account for Content Creation Studio applications" \
        --project=$GOOGLE_CLOUD_PROJECT
    echo "Service account created!"
fi

echo ""
echo "=========================================="
echo "Step 6: Grant IAM Roles to Service Account"
echo "=========================================="
echo ""

ROLES=(
    "roles/aiplatform.user"           # Access to Vertex AI / Agent Engine
    "roles/run.invoker"               # Invoke Cloud Run services
    "roles/storage.objectViewer"      # Read from Cloud Storage
    "roles/logging.logWriter"         # Write logs
)

echo "Granting roles to service account..."
for role in "${ROLES[@]}"; do
    echo "  - Granting $role..."
    gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
        --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
        --role="$role" \
        --condition=None \
        --quiet > /dev/null
done

echo "All roles granted successfully!"

echo ""
echo "=========================================="
echo "Step 7: Create Cloud Storage Bucket (Optional)"
echo "=========================================="
echo ""

# Use existing bucket from .env or create new one
if [ -n "$GOOGLE_CLOUD_STORAGE_BUCKET" ]; then
    BUCKET_NAME="${GOOGLE_CLOUD_STORAGE_BUCKET#gs://}"
    echo "Using existing bucket from .env: gs://$BUCKET_NAME"
else
    BUCKET_NAME="${GOOGLE_CLOUD_PROJECT}-content-studio"
fi

# Check if bucket exists
if gsutil ls -b gs://$BUCKET_NAME &>/dev/null; then
    echo "Storage bucket 'gs://$BUCKET_NAME' already exists"
else
    echo "Creating Cloud Storage bucket..."
    gcloud storage buckets create gs://$BUCKET_NAME \
        --location=$REGION \
        --project=$GOOGLE_CLOUD_PROJECT
    echo "Storage bucket created!"
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "  Project: $GOOGLE_CLOUD_PROJECT"
echo "  Region: $REGION"
echo "  Artifact Registry: ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/content-studio"
echo "  Service Account: $SERVICE_ACCOUNT_EMAIL"
echo "  Storage Bucket: gs://$BUCKET_NAME"
echo ""
echo "Next Steps:"
echo ""

# Check if .env needs updating
ENV_FILE="../.env"
if [ ! -f "$ENV_FILE" ] || ! grep -q "GOOGLE_CLOUD_STORAGE_BUCKET" "$ENV_FILE"; then
    echo "1. Add to your .env file (in project root):"
    echo "   GOOGLE_CLOUD_STORAGE_BUCKET=gs://$BUCKET_NAME"
    echo ""
fi

if [ ! -f "$ENV_FILE" ] || ! grep -q "AGENT_ENGINE_RESOURCE_NAME" "$ENV_FILE"; then
    echo "2. Deploy your agent to Agent Engine:"
    echo "   cd deployment"
    echo "   python deploy.py"
    echo ""
    echo "   Then add the output to your .env file:"
    echo "   AGENT_ENGINE_RESOURCE_NAME=projects/.../locations/.../reasoningEngines/..."
    echo ""
fi

echo "3. Deploy frontend and backend to Cloud Run:"
echo "   cd deployment"
echo "   ./deploy-cloudrun.sh"
echo ""
echo "All set! Your GCP environment is ready for the workshop."
echo ""
