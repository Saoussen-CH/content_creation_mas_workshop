# GCP Setup Guide for Content Creation Studio

This guide walks you through setting up Google Cloud Platform for the Content Creation Studio workshop.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and authenticated
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
3. **Project created** in Google Cloud Console

## Quick Setup (Automated)

Run the automated setup script to configure everything:

```bash
cd deployment
./setup_gcp.sh
```

This script will:
- ✅ Enable all required APIs
- ✅ Create Artifact Registry repository
- ✅ Configure Docker authentication
- ✅ Create service account with proper permissions
- ✅ Create Cloud Storage bucket

## Manual Setup (Step by Step)

If you prefer to set up manually or want to understand each step:

### 1. Set Your Project

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

### 2. Enable Required APIs

```bash
gcloud services enable aiplatform.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    storage.googleapis.com \
    iam.googleapis.com \
    cloudresourcemanager.googleapis.com
```

**APIs Explained:**
- `aiplatform.googleapis.com` - Vertex AI / Agent Engine
- `run.googleapis.com` - Cloud Run for hosting frontend/backend
- `cloudbuild.googleapis.com` - Build Docker containers
- `artifactregistry.googleapis.com` - Store Docker images
- `storage.googleapis.com` - Cloud Storage for agent data
- `iam.googleapis.com` - Identity and Access Management
- `cloudresourcemanager.googleapis.com` - Project management

### 3. Create Artifact Registry Repository

GCR (gcr.io) is deprecated. We use Artifact Registry instead:

```bash
gcloud artifacts repositories create content-studio \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker repository for Content Creation Studio"
```

### 4. Configure Docker Authentication

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### 5. Create Service Account (Optional but Recommended)

```bash
# Create service account
gcloud iam service-accounts create content-studio-sa \
    --display-name="Content Creation Studio Service Account"

# Grant roles
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT="content-studio-sa@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/run.invoker"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/storage.objectViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/logging.logWriter"
```

### 6. Create Cloud Storage Bucket (Optional)

```bash
gcloud storage buckets create gs://${GOOGLE_CLOUD_PROJECT}-content-studio \
    --location=us-central1
```

## Verify Setup

Check that everything is configured correctly:

```bash
# Check enabled APIs
gcloud services list --enabled | grep -E "aiplatform|run|build|artifact"

# Check Artifact Registry
gcloud artifacts repositories list

# Check service account
gcloud iam service-accounts list | grep content-studio

# Check storage bucket
gcloud storage ls
```

## Update .env File

After setup, update your `.env` file:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1

# Storage (if created)
GOOGLE_CLOUD_STORAGE_BUCKET=gs://your-project-id-content-studio

# API Key
GOOGLE_API_KEY=your-google-ai-api-key
```

## Common Issues

### Issue: "Permission denied" errors

**Solution:** Ensure you have the required roles on your user account:
```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="user:your-email@example.com" \
    --role="roles/owner"
```

### Issue: "API not enabled" errors

**Solution:** Enable the specific API:
```bash
gcloud services enable <api-name>.googleapis.com
```

### Issue: "Artifact Registry repository does not exist"

**Solution:** Create the repository first:
```bash
./setup_gcp.sh
```

### Issue: "Docker authentication failed"

**Solution:** Re-authenticate:
```bash
gcloud auth login
gcloud auth configure-docker us-central1-docker.pkg.dev
```

## Next Steps

After completing GCP setup:

1. **Deploy Agent to Agent Engine:**
   ```bash
   python deployment/deploy.py
   ```

2. **Copy the Agent Resource Name** from the output and add to `.env`:
   ```bash
   AGENT_ENGINE_RESOURCE_NAME=projects/.../locations/.../reasoningEngines/...
   ```

3. **Deploy Frontend and Backend to Cloud Run:**
   ```bash
   ./deployment/deploy-cloudrun.sh
   ```

## Cost Considerations

- **Vertex AI Agent Engine**: Pay per request + compute time
- **Cloud Run**: Pay for actual usage (requests + compute time)
- **Artifact Registry**: Storage costs for Docker images
- **Cloud Storage**: Storage costs for agent data

**Tip:** Use the free tier and delete resources when not in use to minimize costs.

## Cleanup

To remove all created resources:

```bash
# Delete Cloud Run services
gcloud run services delete content-studio-backend --region=us-central1
gcloud run services delete content-studio-frontend --region=us-central1

# Delete Artifact Registry repository
gcloud artifacts repositories delete content-studio --location=us-central1

# Delete storage bucket
gcloud storage rm -r gs://${GOOGLE_CLOUD_PROJECT}-content-studio

# Delete service account
gcloud iam service-accounts delete content-studio-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com
```

## Resources

- [Google Cloud Console](https://console.cloud.google.com)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Artifact Registry Documentation](https://cloud.google.com/artifact-registry/docs)
