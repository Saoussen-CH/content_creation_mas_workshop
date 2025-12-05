from google.adk.agents import Agent

blog_post_writer_agent = Agent(
    name="blog_post_writer_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a professional blog writer. Create the final polished blog post from: {{current_content}}

    Enhance it to be publication-ready:
    - Ensure 800-1200 words
    - Add engaging subheadings
    - Include actionable tips
    - Strong call-to-action

    Target audience: {{target_audience}}
    Tone: {{tone}}

    Output only the final blog post in markdown.
    """,
    tools=[],
    output_key="final_blog_post"
)
