#!/bin/bash

# Content Creation Studio - Vertex AI Agent Engine Deployment Script
# Based on ADK deployment best practices

set -e

echo "=========================================="
echo "  Content Creation Studio Deployment"
echo "  Target: Vertex AI Agent Engine"
echo "=========================================="
echo ""

# Check if required environment variables are set
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "❌ Error: GOOGLE_CLOUD_PROJECT environment variable not set"
    echo "Please set it with: export GOOGLE_CLOUD_PROJECT='your-project-id'"
    exit 1
fi

# Set default region if not specified
if [ -z "$GOOGLE_CLOUD_REGION" ]; then
    GOOGLE_CLOUD_REGION="us-central1"
    echo "ℹ️  Using default region: $GOOGLE_CLOUD_REGION"
fi

echo "📋 Deployment Configuration:"
echo "   Project: $GOOGLE_CLOUD_PROJECT"
echo "   Region: $GOOGLE_CLOUD_REGION"
echo ""

# Verify required files exist
echo "🔍 Verifying deployment files..."
required_files=("agent.py" "tools.py" "requirements.txt" ".env" ".agent_engine_config.json")

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Required file '$file' not found!"
        exit 1
    fi
    echo "   ✓ $file"
done

echo ""
echo "✅ All deployment files verified"
echo ""

# Confirm deployment
read -p "🚀 Deploy Content Creation Studio to Vertex AI Agent Engine? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "📦 Starting deployment..."
echo ""

# Deploy using ADK CLI
adk deploy agent_engine \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_REGION \
    . \
    --agent_engine_config_file=.agent_engine_config.json

echo ""
echo "=========================================="
echo "  ✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Test your deployed agent:"
echo "   python test_deployed_agent.py"
echo ""
echo "2. View agent in Console:"
echo "   https://console.cloud.google.com/vertex-ai/agents/agent-engines?project=$GOOGLE_CLOUD_PROJECT"
echo ""
echo "3. Monitor logs:"
echo "   https://console.cloud.google.com/logs?project=$GOOGLE_CLOUD_PROJECT"
echo ""
echo "⚠️  Remember to delete the agent when done to avoid charges:"
echo "   python cleanup.py"
echo ""
