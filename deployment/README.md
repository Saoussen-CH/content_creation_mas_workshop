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
- `deploy-cloudrun.sh` - Deploy frontend/backend to Cloud Run
- `SETUP_GUIDE.md` - Detailed manual setup guide
- `cleanup.py` - Remove deployed resources

## 🧹 Cleanup

```bash
python cleanup.py
```

For detailed documentation, see [SETUP_GUIDE.md](SETUP_GUIDE.md)
