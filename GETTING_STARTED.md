# Getting Started with Content Creation Studio

**Complete step-by-step guide to deploy and test the Content Creation Studio**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Deploy Agent to Agent Engine](#deploy-agent-to-agent-engine)
4. [Deploy to Cloud Run](#deploy-to-cloud-run)
5. [Testing Your Deployment](#testing-your-deployment)
6. [Test Prompts](#test-prompts)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

### Required Software
- **Python 3.11.13** (recommended via pyenv) - [pyenv Installation](#python-version-management-with-pyenv)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **gcloud CLI** - [Install](https://cloud.google.com/sdk/docs/install)
- **Git** - [Download](https://git-scm.com/downloads)
- **pyenv** (recommended) - Python version manager

### Google Cloud Account
- Active Google Cloud account with billing enabled
- A GCP project (or create a new one)
- Owner or Editor permissions on the project

### Get Your Google API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Save the API key securely

---

## Initial Setup

### Step 0: Python Version Management with pyenv

**Why pyenv?** This project requires Python 3.11.13 specifically. Pyenv allows you to easily install and switch between Python versions.

#### Install pyenv

**macOS:**
```bash
brew install pyenv

# Add to ~/.zshrc or ~/.bash_profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Reload shell
source ~/.zshrc
```

**Linux (Ubuntu/Debian):**
```bash
# Install dependencies
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
  liblzma-dev python3-openssl git

# Install pyenv
curl https://pyenv.run | bash

# Add to ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload shell
source ~/.bashrc
```

#### Install Python 3.11.13

```bash
# Install Python 3.11.13
pyenv install 3.11.13

# Verify installation
pyenv versions
```

### Step 1: Clone and Navigate to Project

```bash
# Clone the repository (if you haven't already)
git clone <your-repo-url>
cd content_creation_mas

# Set Python version for this project (uses .python-version file)
pyenv local 3.11.13

# Verify Python version
python --version  # Should output: Python 3.11.13
```

**Note:** The project includes a `.python-version` file that automatically activates Python 3.11.13 when you enter the directory (if you have pyenv installed).

### Step 2: Set Up Google Cloud Project

**⏱️ Time:** 5-10 minutes

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud auth application-default login

# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Run automated setup script
cd deployment
chmod +x setup_gcp.sh
./setup_gcp.sh
```

**What this script does:**
- ✅ Enables required APIs (Vertex AI, Cloud Run, Artifact Registry, etc.)
- ✅ Creates Artifact Registry repository
- ✅ Configures Docker authentication
- ✅ Creates service account with proper permissions
- ✅ Creates Cloud Storage bucket for staging

**Expected output:**
```
✓ Enabled Vertex AI API
✓ Created Artifact Registry repository: content-studio
✓ Configured Docker authentication
✓ Created service account: content-studio-sa
✓ Created storage bucket: gs://your-project-staging
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Return to project root
cd ..

# Create .env file
cat > .env << 'EOF'
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=gs://your-project-staging

# Google API Key (from Google AI Studio)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=1

# Agent Configuration
WORKER_MODEL=gemini-2.5-flash
COORDINATOR_MODEL=gemini-2.5-flash
QUALITY_SCORE_THRESHOLD=70
MAX_IMPROVEMENT_ITERATIONS=3

# Agent Engine Resource (will be set after deployment)
AGENT_ENGINE_RESOURCE_NAME=""
EOF
```

**Replace the following:**
- `your-project-id` → Your actual GCP project ID
- `your-project-staging` → Your staging bucket name
- `your_google_api_key_here` → Your Google API key from Step 2

### Step 4: Install Dependencies

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies (optional for local testing)
cd frontend
npm install
cd ..
```

---

## Deploy Agent to Agent Engine

### Step 1: Verify Package Structure

```bash
# Ensure the agent package exists
ls -la content_creation_studio/

# Expected output:
# __init__.py
# agent.py
# tools.py
# sub_agents/
```

### Step 2: Deploy the Agent

```bash
# Deploy from project root
python deployment/deploy.py --action deploy
```

**What happens during deployment:**
1. Packages your `content_creation_studio` agent
2. Uploads to Vertex AI Agent Engine
3. Installs dependencies (google-adk==1.19.0, etc.)
4. Creates reasoning engine instance

**Expected output:**
```
============================================================
DEPLOYING TO VERTEX AI AGENT ENGINE
============================================================
✓ Initialized Vertex AI
  Project: your-project-id
  Location: us-central1
  Staging: gs://your-project-staging

⏳ Step 1/3: Deploying agent (this may take several minutes)...
...
============================================================
✓ DEPLOYMENT SUCCESSFUL!
============================================================

Resource Name: projects/773461168680/locations/us-central1/reasoningEngines/9027074026924670976
Agent Engine ID: 9027074026924670976

Update your .env file with:
AGENT_ENGINE_RESOURCE_NAME="projects/773461168680/locations/us-central1/reasoningEngines/9027074026924670976"
```

**⏱️ Time:** 5-10 minutes

### Step 3: Update .env File

Copy the `AGENT_ENGINE_RESOURCE_NAME` from the output and update your `.env` file:

```bash
# Open .env and add the resource name
nano .env

# Or use sed to update automatically
RESOURCE_NAME="projects/773461168680/locations/us-central1/reasoningEngines/9027074026924670976"
sed -i "s|AGENT_ENGINE_RESOURCE_NAME=\"\"|AGENT_ENGINE_RESOURCE_NAME=\"${RESOURCE_NAME}\"|" .env
```

### Step 4: Test the Deployed Agent (Optional)

```bash
# Test the deployed agent
python deployment/deploy.py --action test_remote --resource_name "<your-resource-name>"
```

---

## Deploy to Cloud Run

Now that your agent is deployed to Agent Engine, deploy the frontend and backend to Cloud Run.

### Step 1: Review Configuration

The combined deployment script will:
- Build a Docker image with both React frontend and FastAPI backend
- Push to Google Artifact Registry
- Deploy to Cloud Run
- Configure environment variables

### Step 2: Run Deployment Script

```bash
cd deployment
chmod +x deploy-combined.sh
./deploy-combined.sh
```

**Deployment steps:**
```
🚀 Step 1/5: Configuring Docker Authentication...
✅ Docker authentication configured

🔨 Step 2/5: Building Docker image...
✅ Image built successfully

📤 Step 3/5: Pushing image to registry...
✅ Image pushed

🚀 Step 4/5: Deploying to Cloud Run...
✅ Service deployed

🔍 Step 5/5: Getting service information...
✅ Deployment complete!

Service URL: https://content-studio-xxxxx-uc.a.run.app
```

**⏱️ Time:** 10-15 minutes

### Step 3: Access Your Application

Open the Service URL in your browser:
```
https://content-studio-xxxxx-uc.a.run.app
```

You should see the Content Creation Studio interface with two tabs:
1. **Create Content** - Generate full content packages
2. **Analyze Text** - Analyze text snippets

---

## Testing Your Deployment

### Test 1: Health Check

```bash
# Get your Cloud Run URL
SERVICE_URL=$(gcloud run services describe content-studio \
  --region=us-central1 \
  --format='value(status.url)')

# Test health endpoint
curl $SERVICE_URL/health
```

**Expected response:**
```json
{
  "status": "ok",
  "message": "Content Creation Studio API is running",
  "agent": "content_creation_studio",
  "agent_resource": "projects/.../reasoningEngines/...",
  "agent_connected": true
}
```

### Test 2: API Documentation

Visit the interactive API docs:
```
https://your-service-url.run.app/docs
```

### Test 3: Web Interface

1. Open your Cloud Run URL in a browser
2. Navigate to the **"Create Content"** tab
3. Fill in the form with test data
4. Click **"Generate Content Package"**
5. Watch the real-time progress
6. View the generated content

### Test 4: Text Analysis

1. Navigate to the **"Analyze Text"** tab
2. Paste sample text
3. Click **"Analyze Text"**
4. View word count, readability score, and hashtags

---

## Test Prompts

Use these test prompts to verify your Content Creation Studio is working correctly:

### Test Prompt 1: Tech Blog Content
```
Create a complete content package for:
- Topic: The Future of AI in Healthcare
- Target Audience: Healthcare professionals and tech enthusiasts
- Tone: Professional and informative
- Keywords: AI healthcare, medical AI, patient care, diagnostic AI
```

**Expected output:**
- ✅ 800-1200 word blog post
- ✅ LinkedIn post (250-300 words)
- ✅ Twitter thread (5-7 tweets)
- ✅ Instagram caption with hashtags
- ✅ Email newsletter
- ✅ SEO metadata (title, description, keywords)

---

### Test Prompt 2: Marketing Campaign
```
Create a complete content package for:
- Topic: Sustainable Fashion and Eco-Friendly Clothing
- Target Audience: Environmentally conscious millennials and Gen Z
- Tone: Conversational and inspiring
- Keywords: sustainable fashion, eco-friendly clothes, ethical fashion, green wardrobe
```

**Expected output:**
- ✅ Engaging blog post about sustainable fashion trends
- ✅ Social media content across all platforms
- ✅ Email newsletter with call-to-action
- ✅ SEO-optimized metadata

---

### Test Prompt 3: Productivity Guide
```
Create a complete content package for:
- Topic: Productivity Hacks Using AI for Remote Workers
- Target Audience: Remote professionals and digital nomads
- Tone: Conversational and helpful
- Keywords: AI productivity, remote work, automation tools, time management
```

**Expected output:**
- ✅ Practical blog post with actionable tips
- ✅ Social media posts highlighting key productivity hacks
- ✅ Newsletter with tool recommendations
- ✅ Optimized SEO metadata

---

### Test Prompt 4: Educational Content
```
Create a complete content package for:
- Topic: Introduction to Machine Learning for Beginners
- Target Audience: Students and career switchers interested in AI
- Tone: Educational and encouraging
- Keywords: machine learning basics, AI for beginners, learn ML, data science intro
```

**Expected output:**
- ✅ Comprehensive beginner-friendly blog post
- ✅ Bite-sized social media educational content
- ✅ Newsletter with learning resources
- ✅ SEO metadata targeting beginner searches

---

## Troubleshooting

### Issue 1: "AGENT_ENGINE_RESOURCE_NAME not set"

**Problem:** Backend can't connect to Agent Engine

**Solution:**
```bash
# 1. Verify .env file has the resource name
cat .env | grep AGENT_ENGINE_RESOURCE_NAME

# 2. If missing, get it from deployment output or list agents
gcloud ai reasoning-engines list --location=us-central1

# 3. Update .env file with the resource name
```

---

### Issue 2: "AttributeError: 'AgentTool' object has no attribute 'include_plugins'"

**Problem:** Agent deployed with incompatible ADK version

**Solution:**
```bash
# 1. Verify deployment/deploy.py uses google-adk==1.19.0
grep "google-adk" deployment/deploy.py

# 2. Should show: "google-adk==1.19.0"

# 3. Redeploy agent
python deployment/deploy.py --action deploy
```

---

### Issue 3: "Docker push denied: Unauthenticated request"

**Problem:** Docker not authenticated with Artifact Registry

**Solution:**
```bash
# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet

# Retry deployment
cd deployment
./deploy-combined.sh
```

---

### Issue 4: Cloud Run Service Not Starting

**Problem:** Container fails to start

**Solution:**
```bash
# 1. Check Cloud Run logs
gcloud run services logs read content-studio \
  --region=us-central1 \
  --limit=50

# 2. Verify environment variables are set
gcloud run services describe content-studio \
  --region=us-central1 \
  --format="value(spec.template.spec.containers[0].env)"

# 3. Check if AGENT_ENGINE_RESOURCE_NAME is set correctly
```

---

### Issue 5: Agent Engine Logs Show Errors

**Problem:** Agent crashes when processing requests

**Solution:**
```bash
# 1. Check Agent Engine logs
gcloud logging read "resource.type=aiplatform.googleapis.com/ReasoningEngine" \
  --limit=50 \
  --format="table(timestamp, severity, textPayload)"

# 2. Look for specific errors and check if ADK version is correct

# 3. Redeploy with correct version if needed
```

---

### Issue 6: "429 Rate Limit Error"

**Problem:** Exceeded Vertex AI quotas

**Solution:**
```bash
# 1. Check current quotas
gcloud services quota list --service=aiplatform.googleapis.com \
  --filter="metric.type:aiplatform.googleapis.com/custom_model_serving"

# 2. Request quota increase in Cloud Console:
# https://console.cloud.google.com/iam-admin/quotas

# 3. Or switch to a different model with higher limits
```

---

---

## Local Development (Alternative to Cloud Deployment)

If you want to develop and test locally without deploying to Cloud Run, follow these instructions.

### Option A: Fully Local (No GCP Required)

**Best for:** Quick testing, development, workshops without cloud costs

#### Step 1: Install Dependencies

```bash
# Ensure Python 3.11.13 is active
python --version  # Should show 3.11.13

# Install Python dependencies
pip install -r requirements.txt

# Optional: Install frontend
cd frontend && npm install && cd ..
```

#### Step 2: Get Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Save the key

#### Step 3: Configure for Local Development

```bash
# Create .env file
cat > .env << 'EOF'
# Google API Key (required)
GOOGLE_API_KEY=your_api_key_here

# Use AI Studio (not Vertex AI)
GOOGLE_GENAI_USE_VERTEXAI=0

# Agent Configuration
WORKER_MODEL=gemini-2.0-flash-exp
COORDINATOR_MODEL=gemini-2.0-flash-exp
QUALITY_SCORE_THRESHOLD=70
MAX_IMPROVEMENT_ITERATIONS=3
EOF
```

#### Step 4: Run Agent (CLI Mode)

```bash
# Test the agent directly
python run_agent.py
```

**Expected output:**
```
🚀 Content Creation Multi-Agent System
=====================================
📝 Sending query to agent...

[Real-time agent workflow output...]

✅ Content creation completed!
```

#### Step 5: Run with Web Interface (Optional)

**Terminal 1 - Backend:**
```bash
cd backend
python api_server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access:** Open http://localhost:5173 in your browser

---

### Option B: Local Backend + Cloud Agent Engine

**Best for:** Testing with production agent, hybrid development

#### Prerequisites
- Agent deployed to Agent Engine (see main deployment steps)
- AGENT_ENGINE_RESOURCE_NAME from deployment

#### Step 1: Configure Environment

```bash
cat > .env << 'EOF'
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_API_KEY=your_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=1

# Agent Engine Resource (from deployment)
AGENT_ENGINE_RESOURCE_NAME=projects/.../locations/.../reasoningEngines/...

# Agent Configuration
WORKER_MODEL=gemini-2.0-flash-exp
COORDINATOR_MODEL=gemini-2.0-flash-exp
EOF
```

#### Step 2: Run Backend Locally

```bash
cd backend
python api_server.py
```

**Expected output:**
```
✅ Starting Content Creation Studio API Server
🤖 Connected to Agent: projects/.../reasoningEngines/...
📡 Server will be available at: http://localhost:8000
📚 API Docs at: http://localhost:8000/docs
```

#### Step 3: Run Frontend (Optional)

```bash
cd frontend
npm run dev
```

Access at: http://localhost:5173

---

### Local Development Tips

#### Hot Reload
Both backend and frontend support hot reload:
- **Backend:** Uvicorn auto-reloads on `.py` file changes
- **Frontend:** Vite hot-reloads on `.jsx` file changes

#### Testing API Endpoints
Visit http://localhost:8000/docs for interactive API documentation

#### Debugging

```bash
# Check Python version
python --version

# Test Google API Key
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('API Key:', os.getenv('GOOGLE_API_KEY')[:10] + '...')"

# Run agent with verbose output
python run_agent.py
```

#### Common Local Issues

**"ImportError: No module named 'google.adk'"**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**"GOOGLE_API_KEY not found"**
```bash
# Verify .env file exists and contains API key
cat .env | grep GOOGLE_API_KEY

# Create .env if missing (see configuration steps above)
```

**Port Already in Use**
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

**Frontend Can't Connect to Backend**
```bash
# Ensure backend is running
curl http://localhost:8000/health

# Check frontend .env.development
# Should have: VITE_API_URL=http://localhost:8000
```

---

### Local vs Cloud Deployment

| Feature | Local Development | Cloud Deployment |
|---------|------------------|------------------|
| **Setup Time** | 5 minutes | 30-40 minutes |
| **Cost** | Free (API usage only) | Cloud Run + Agent Engine costs |
| **Performance** | Depends on local machine | Scalable, managed |
| **Access** | localhost only | Public URL |
| **Best For** | Development, testing | Production, demos |
| **Agent Location** | Runs locally | Agent Engine (managed) |

---

## Next Steps

After successful deployment:

1. **Monitor Your Application**
   - View logs in Cloud Console
   - Set up alerting for errors
   - Monitor costs in Billing

2. **Customize the Agent**
   - Modify agent prompts in `content_creation_studio/sub_agents/`
   - Adjust quality thresholds in `.env`
   - Add new agent capabilities

3. **Scale Your Deployment**
   - Configure Cloud Run autoscaling
   - Set up load balancing
   - Enable CDN for frontend assets

4. **Add CI/CD**
   - Set up Cloud Build triggers
   - Automate deployments on git push
   - Add staging environment

---

## Additional Resources

- **[README.md](README.md)** - Project overview and architecture
- **[deployment/README.md](deployment/README.md)** - Detailed deployment guide
- **[Vertex AI Agent Engine Docs](https://cloud.google.com/vertex-ai/docs/agent-engine)** - Official documentation
- **[Google ADK GitHub](https://github.com/google/adk)** - Agent Development Kit

---

## Support

If you encounter issues not covered in this guide:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review Cloud Run and Agent Engine logs
3. Consult the official Google Cloud documentation
4. Open an issue in the project repository

---

**🎉 Congratulations! Your Content Creation Studio is now deployed and ready to use!**
