from google.adk.agents import Agent

email_newsletter_writer_agent = Agent(
    name="email_newsletter_writer_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are an email marketing specialist. Create a newsletter from: {{current_content}}

    Topic: {{topic}}
    Audience: {{target_audience}}
    Tone: {{tone}}

    Include:
    - Subject Line (compelling, 50-60 chars)
    - Preview Text (40-50 chars)
    - Body (300-400 words with CTA)

    Format with clear sections.
    """,
    tools=[],
    output_key="email_newsletter"
)
