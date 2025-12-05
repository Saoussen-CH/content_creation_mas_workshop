"""
Test script for deployed Content Creation Studio on Vertex AI Agent Engine

This script connects to your deployed agent and runs test queries.
"""

import os
import asyncio
import vertexai
from vertexai import agent_engines

# Configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
REGION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

if not PROJECT_ID:
    raise ValueError("Please set GOOGLE_CLOUD_PROJECT environment variable")


async def test_deployed_agent():
    """Test the deployed Content Creation Studio agent."""

    print("=" * 70)
    print("  Testing Deployed Content Creation Studio")
    print("=" * 70)
    print(f"Project: {PROJECT_ID}")
    print(f"Region: {REGION}")
    print()

    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=REGION)

    # Get the deployed agent
    print("🔍 Retrieving deployed agent...")
    agents_list = list(agent_engines.list())

    if not agents_list:
        print("❌ No agents found. Please deploy first using deploy.sh")
        return

    remote_agent = agents_list[0]  # Get most recent agent
    print(f"✅ Connected to: {remote_agent.resource_name}")
    print()

    # Test 1: Content Analysis
    print("=" * 70)
    print("TEST 1: Text Analysis")
    print("=" * 70)

    test_text = """
    Artificial intelligence is transforming how we work and live.
    AI tools can automate repetitive tasks, analyze data, and provide insights.
    Remote workers are using AI to boost productivity and creativity.
    """

    query1 = f"Analyze this text:\n\n{test_text}"
    print(f"Query: {query1[:100]}...")
    print("\nResponse:")

    async for item in remote_agent.async_stream_query(
        message=query1,
        user_id="test_user_001"
    ):
        print(item)

    print("\n")

    # Test 2: Content Creation (abbreviated for testing)
    print("=" * 70)
    print("TEST 2: Content Creation")
    print("=" * 70)

    query2 = """Create a complete content package for:
    - Topic: AI productivity tools for developers
    - Target Audience: Software developers
    - Tone: Technical but accessible
    - Keywords: AI, productivity, development tools
    """

    print(f"Query: {query2}")
    print("\nResponse:")

    async for item in remote_agent.async_stream_query(
        message=query2,
        user_id="test_user_001"
    ):
        print(item)

    print()
    print("=" * 70)
    print("✅ Testing Complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_deployed_agent())
