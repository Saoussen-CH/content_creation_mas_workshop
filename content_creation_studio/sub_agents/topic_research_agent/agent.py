from google.adk.agents import Agent
from google.adk.tools import google_search

topic_research_agent = Agent(
    name="topic_research_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a topic research expert. For topic: {{topic}}

    Use search to find trending angles and select the SINGLE BEST specific blog post title.
    Output format: Just the title, nothing else.

    Example: "10 AI Tools That Save Small Businesses 20 Hours Per Week"
    """,
    tools=[google_search],
    output_key="blog_topic"
)
