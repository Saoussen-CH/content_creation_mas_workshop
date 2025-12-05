# Deployment Guide - Content Creation Studio

Complete deployment guide for DevFest Fusion 4.0 Workshop

## 📋 Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and authenticated
3. **Python 3.11+** for agent deployment

## 🚀 Quick Start Deployment

### Step 1: Configure Environment

```bash
cp .env.example .env
# Edit .env and set your GOOGLE_API_KEY and GOOGLE_CLOUD_PROJECT
```

### Step 2: Set Up GCP

```bash
cd deployment
./setup_gcp.sh
```

### Step 3: Deploy Agent to Agent Engine

```bash
python deploy.py
# Copy AGENT_ENGINE_RESOURCE_NAME to your .env file
```

### Step 4: Deploy to Cloud Run

```bash
./deploy-cloudrun.sh
```

## 📁 Files

- `setup_gcp.sh` - GCP environment setup
- `deploy.py` - Deploy agent to Agent Engine
- `deploy-combined.sh` - Deploy frontend/backend to Cloud Run
- `test_deployed_agent.py` - Test deployed agent
- `cleanup_gcp.sh` - Shell script to clean up all GCP resources
- `cleanup_gcp.py` - Python script for comprehensive cleanup
- `SETUP_GUIDE.md` - Detailed manual setup guide
- `CLEANUP_GUIDE.md` - Complete cleanup documentation

## 🧹 Cleanup

```bash
# Dry run to see what would be deleted
python cleanup_gcp.py --dry-run --all

# Delete core resources (Cloud Run, Agent Engine, Docker images)
python cleanup_gcp.py

# Delete ALL resources including service account and storage bucket
python cleanup_gcp.py --all

# Or use the shell script (interactive)
./cleanup_gcp.sh
```

For detailed cleanup instructions, see [CLEANUP_GUIDE.md](CLEANUP_GUIDE.md)

For detailed documentation, see [SETUP_GUIDE.md](SETUP_GUIDE.md)
