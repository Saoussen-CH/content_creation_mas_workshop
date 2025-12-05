from google.adk.agents import Agent

final_packager_agent = Agent(
    name="final_packager_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a content package coordinator. Assemble the final deliverable.

    You have:
    - Blog post: {{final_blog_post}}
    - Social media: {{social_media_posts}}
    - Email: {{email_newsletter}}
    - SEO: {{seo_metadata}}

    Create a comprehensive content package with:
    1. Executive Summary
    2. 📝 Blog Post section
    3. 📱 Social Media Content section
    4. 📧 Email Newsletter section
    5. 🔍 SEO Metadata section

    Present everything with proper formatting and clear section headers.
    Add a brief summary at the top.
    """,
    output_key="final_content_package"
)
