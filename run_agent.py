import os
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables from .env file FIRST (before importing agents!)
load_dotenv()

from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai.types import Content, Part
from content_creation_studio.agent import root_agent

async def run_agent_query(agent: "Agent", query: str, session: Session, user_id: str, session_service: InMemorySessionService):
    """Initializes a runner and executes a query for a given agent and session."""
    print(f"\n{'='*70}")
    print(f"🚀 Running query for agent: '{agent.name}'")
    print(f"{'='*70}\n")

    runner = Runner(
        agent=agent,
        session_service=session_service,
        app_name=agent.name,
        plugins=[LoggingPlugin()]
    )

    final_response = ""
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=Content(parts=[Part(text=query)], role="user")
        ):
            if event.is_final_response():
                final_response = event.content.parts[0].text
    except Exception as e:
        final_response = f"An error occurred: {e}"

    print(f"\n{'='*70}")
    print("✅ FINAL RESPONSE:")
    print(f"{'='*70}")
    # Use print instead of display and Markdown for a pure Python script
    print(final_response)
    print(f"={'='*70}\n")

    return final_response

async def run_capstone_project():
    """Run the complete Content Creation Studio system"""
    # Check for API key in environment
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY environment variable not set!")
        print("\nPlease set your API key using one of these methods:")
        print("  1. Export in terminal: export GOOGLE_API_KEY='your_api_key'")
        print("  2. Create .env file with: GOOGLE_API_KEY=your_api_key")
        print("  3. Set in your shell profile (~/.bashrc or ~/.zshrc)")
        print("\nGet your API key from: https://aistudio.google.com")
        sys.exit(1)

    print(f"✅ API Key loaded from environment")

    session_service = InMemorySessionService()
    user_id = "adk_content_creator_001"

    session = await session_service.create_session(
        app_name=root_agent.name,
        user_id=user_id
    )

    print("\n" + "🎯"*35)
    print("    CONTENT CREATION STUDIO - CAPSTONE PROJECT")
    print("🎯"*35 + "\n")

    # --- Query 1: Full Content Creation ---
    query1 = """
    Create a complete content package for:
    - Topic: Productivity hacks using AI for remote workers
    - Target Audience: Remote professionals and digital nomads
    - Tone: Conversational and helpful
    - Keywords: AI productivity, remote work, automation tools
    """
    print(f"👤 USER REQUEST 1:\n{query1}\n")
    await run_agent_query(root_agent, query1, session, user_id, session_service)

    print("\nPausing for 60 seconds to avoid rate limiting...\n")
    await asyncio.sleep(60)

    # --- Query 2: Analyze Specific Content ---
    sample_text = """
    Remote work has transformed how we think about productivity. With AI tools,
    professionals can automate repetitive tasks and focus on creative work.
    """
    query2 = f"Can you analyze this text snippet:\n\n{sample_text}"
    print(f"👤 USER REQUEST 2:\n{query2}\n")
    await run_agent_query(root_agent, query2, session, user_id, session_service)

    print("\nPausing for 60 seconds to avoid rate limiting...\n")
    await asyncio.sleep(60)

    # --- Query 3: Simulate Publishing ---
    query3 = "Publish the blog post to our blog platform"
    print(f"👤 USER REQUEST 3: {query3}\n")
    await run_agent_query(root_agent, query3, session, user_id, session_service)

    print("\n" + "✅"*35)
    print("    CAPSTONE PROJECT COMPLETE!")
    print("✅"*35 + "\n")

if __name__ == "__main__":
    asyncio.run(run_capstone_project())
