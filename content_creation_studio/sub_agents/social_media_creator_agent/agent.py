from google.adk.agents import Agent

social_media_creator_agent = Agent(
    name="social_media_creator_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a social media specialist. Create posts from: {{current_content}}

    Topic: {{topic}}
    Audience: {{target_audience}}
    Tone: {{tone}}

    Create:
    1. LinkedIn Post (150-200 words, professional)
    2. Twitter Thread (3 tweets, 280 chars each)
    3. Instagram Caption (100-150 words, with emojis and hashtags)

    Format with clear headers for each platform.
    """,
    tools=[],
    output_key="social_media_posts"
)
