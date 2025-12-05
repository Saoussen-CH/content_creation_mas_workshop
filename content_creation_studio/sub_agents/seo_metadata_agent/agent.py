from google.adk.agents import Agent

seo_metadata_agent = Agent(
    name="seo_metadata_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are an SEO specialist. Generate metadata for: {{topic}}

    Keywords: {{keywords}}

    Create:
    1. Meta Title (50-60 chars)
    2. Meta Description (150-160 chars)
    3. URL Slug
    4. Focus Keyword
    5. 5 Related Keywords

    Format as structured list.
    """,
    tools=[],
    output_key="seo_metadata"
)
