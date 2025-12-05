# GCP Cleanup Guide for Content Creation Studio

This guide explains how to clean up all Google Cloud Platform resources created during deployment.

## 🗑️ Quick Cleanup Commands

### Option 1: Python Script (Recommended)

```bash
# Dry run - see what would be deleted without actually deleting
python deployment/cleanup_gcp.py --dry-run

# Delete core resources only (Cloud Run, Agent Engine, Docker images)
python deployment/cleanup_gcp.py

# Delete ALL resources including service account and storage bucket
python deployment/cleanup_gcp.py --all

# Delete without confirmation prompts
python deployment/cleanup_gcp.py --all --force
```

### Option 2: Shell Script

```bash
# Interactive cleanup with prompts
./deployment/cleanup_gcp.sh
```

## 📋 Resources That Will Be Deleted

### Core Resources (Always Deleted)

1. **Cloud Run Service** - `content-studio`
   - The deployed web application
   - No cost when not in use (scales to zero)

2. **Agent Engine** - Multi-agent system deployment
   - Vertex AI Reasoning Engine
   - Resource name from `AGENT_ENGINE_RESOURCE_NAME`

3. **Docker Images** - Container images in Artifact Registry
   - All images in `content-studio` repository
   - Optional: Delete the entire repository

### Optional Resources (Use `--all` flag)

4. **Service Account** - `content-studio-sa@{project}.iam.gserviceaccount.com`
   - All IAM role bindings will be removed first
   - Then the service account itself

5. **Cloud Storage Bucket** - `gs://{project}-content-studio`
   - ⚠️ **WARNING**: All files in the bucket will be deleted!
   - This includes Agent Engine staging files

### Resources NOT Deleted

The following resources remain enabled but don't incur costs:
- Enabled GCP APIs (Vertex AI, Cloud Run, etc.)
- Cloud Build history
- Cloud Logging entries
- Artifact Registry repository (if you choose to keep it)

## 🔍 Dry Run Mode

**Always run a dry run first** to see what would be deleted:

```bash
python deployment/cleanup_gcp.py --dry-run --all
```

This shows you exactly what resources exist and would be deleted, without actually deleting anything.

## 📊 Step-by-Step Cleanup Process

### Step 1: Check What Exists

```bash
# Check Cloud Run services
gcloud run services list --region=us-central1

# Check Agent Engine deployments
gcloud beta ai reasoning-engines list --region=us-central1

# Check Artifact Registry repositories
gcloud artifacts repositories list --location=us-central1

# Check storage buckets
gsutil ls
```

### Step 2: Run Dry Run

```bash
python deployment/cleanup_gcp.py --dry-run --all
```

Review the output to confirm what will be deleted.

### Step 3: Execute Cleanup

```bash
# For workshop cleanup (keep service account and bucket for reuse)
python deployment/cleanup_gcp.py

# For complete cleanup (delete everything)
python deployment/cleanup_gcp.py --all
```

### Step 4: Verify Cleanup

```bash
# Verify Cloud Run service is gone
gcloud run services list --region=us-central1

# Check that resources were deleted
# You should see no results for your service
```

## 🚨 Manual Cleanup (If Scripts Fail)

If the automated scripts fail, you can manually delete resources:

### Delete Cloud Run Service

```bash
gcloud run services delete content-studio \
    --region=us-central1 \
    --project=YOUR_PROJECT_ID \
    --quiet
```

### Delete Agent Engine

```bash
# Get the Agent Engine ID from your .env file
# Format: projects/{project}/locations/{location}/reasoningEngines/{id}

# Use the deploy script
python deployment/deploy.py --action cleanup \
    --resource_name "projects/.../locations/.../reasoningEngines/..."

# OR use gcloud command
gcloud beta ai reasoning-engines delete ENGINE_ID \
    --region=us-central1 \
    --project=YOUR_PROJECT_ID
```

### Delete Docker Images

```bash
# List images
gcloud artifacts docker images list \
    us-central1-docker.pkg.dev/YOUR_PROJECT_ID/content-studio

# Delete all images
gcloud artifacts docker images delete IMAGE_NAME --delete-tags --quiet

# Delete repository
gcloud artifacts repositories delete content-studio \
    --location=us-central1 \
    --project=YOUR_PROJECT_ID
```

### Delete Service Account

```bash
# Remove IAM bindings
gcloud projects remove-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:content-studio-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Delete service account
gcloud iam service-accounts delete \
    content-studio-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com \
    --project=YOUR_PROJECT_ID
```

### Delete Storage Bucket

```bash
# ⚠️ WARNING: This deletes ALL files!
gsutil -m rm -r gs://YOUR_BUCKET_NAME
```

## 💰 Cost Implications

### What Costs Money

- **Cloud Run**: Only when receiving requests (scales to zero)
- **Agent Engine**: Charges per query/token
- **Storage**: Very minimal (~$0.02/GB/month)
- **Artifact Registry**: ~$0.10/GB/month

### After Cleanup

After cleanup, you should have **zero or near-zero costs** related to this project:
- No active services
- No stored Docker images (if repository deleted)
- No storage bucket (if deleted)
- Enabled APIs don't cost anything when not in use

## 🔄 Redeployment After Cleanup

If you want to redeploy after cleanup:

### If you kept service account and bucket (recommended):

```bash
# Just redeploy the agent
python deployment/deploy.py --action deploy

# Update .env with new AGENT_ENGINE_RESOURCE_NAME

# Redeploy Cloud Run
./deployment/deploy-combined.sh
```

### If you deleted everything:

```bash
# Re-run full setup
./deployment/setup_gcp.sh

# Deploy agent
python deployment/deploy.py --action deploy

# Deploy Cloud Run
./deployment/deploy-combined.sh
```

## 🆘 Troubleshooting

### "Permission Denied" Errors

Ensure you're authenticated:
```bash
gcloud auth login
gcloud auth application-default login
```

### "Resource Not Found" Errors

The resource may already be deleted. This is safe to ignore.

### Agent Engine Won't Delete

Try using force delete:
```python
# In deploy.py, the cleanup function uses:
remote_app.delete(force=True)
```

Or manually from Cloud Console:
1. Go to Vertex AI → Agent Builder → Reasoning Engines
2. Select your engine
3. Click "Delete"

### "Bucket Not Empty" Errors

Force delete with:
```bash
gsutil -m rm -rf gs://YOUR_BUCKET_NAME/**
gsutil rb gs://YOUR_BUCKET_NAME
```

## 📞 Support

If you encounter issues:

1. **Check logs**: `gcloud logging read --limit=50`
2. **Cloud Console**: Review resources in [Google Cloud Console](https://console.cloud.google.com)
3. **GitHub Issues**: Report issues in the project repository

## ✅ Cleanup Checklist

Use this checklist to ensure complete cleanup:

- [ ] Cloud Run service deleted
- [ ] Agent Engine deleted
- [ ] Docker images removed from Artifact Registry
- [ ] Artifact Registry repository deleted (optional)
- [ ] Service account deleted (optional)
- [ ] IAM policy bindings removed (optional)
- [ ] Storage bucket deleted (optional)
- [ ] Verified zero active resources in Cloud Console
- [ ] Updated .env file (removed resource names)

## 🎓 Workshop Cleanup

For workshop attendees, we recommend:

**During workshop**: Keep all resources running for testing

**After workshop**:
```bash
# Keep infrastructure for reuse
python deployment/cleanup_gcp.py

# Complete removal (if not reusing)
python deployment/cleanup_gcp.py --all
```

This balances cost savings with the ability to quickly redeploy if needed.
