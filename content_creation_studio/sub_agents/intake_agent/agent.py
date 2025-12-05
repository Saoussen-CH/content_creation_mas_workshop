from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from content_creation_studio.tools import update_session_state

intake_agent = Agent(
    name="intake_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a content brief analyzer. From the user's request, identify:
    - Main topic
    - Target audience
    - Desired tone
    - Key SEO keywords (comma-separated)

    Then call the `update_session_state` tool with the extracted values.
    """,
    tools=[FunctionTool(update_session_state)]
)
