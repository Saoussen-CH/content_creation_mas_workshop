from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from content_creation_studio.tools import exit_loop, QUALITY_THRESHOLD_MET

content_improver_agent = Agent(
    name="content_improver_agent",
    model="gemini-2.5-flash",
    instruction=f"""
    You are a content improvement specialist.

    Current content: {{{{current_content}}}}
    Feedback: {{{{quality_feedback}}}}

    - IF feedback is '{QUALITY_THRESHOLD_MET}', call `exit_loop` immediately.
    - ELSE, improve the content based on issues:
      * Expand if too short (add examples, details)
      * Simplify if complex (shorter sentences, simpler words)
      * Add headings if missing
      * Add conclusion if missing

    Output the COMPLETE improved content in markdown.
    """,
    tools=[FunctionTool(exit_loop)],
    output_key="current_content"
)
