from google.adk.agents import Agent

content_drafter_agent = Agent(
    name="content_drafter_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a content writer. Write a blog post: {{blog_topic}}

    Target audience: {{target_audience}}
    Tone: {{tone}}

    Create a draft (400-600 words) with:
    - Engaging introduction
    - At least 2 H2 headings
    - A conclusion section

    Output only the blog post in markdown format.
    """,
    tools=[],
    output_key="current_content"
)
