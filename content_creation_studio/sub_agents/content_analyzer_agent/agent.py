from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from content_creation_studio.tools import count_words, calculate_readability_score, generate_hashtags

content_analyzer_agent = Agent(
    name="content_analyzer_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a content analysis expert. Analyze the provided text.

    Use your tools to:
    1. Count words
    2. Calculate readability
    3. Generate 5 hashtags

    Provide a clear analysis report.
    """,
    tools=[
        FunctionTool(count_words),
        FunctionTool(calculate_readability_score),
        FunctionTool(generate_hashtags)
    ]
)
