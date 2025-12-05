import os
from dotenv import load_dotenv

# Ensure environment variables are loaded (especially GOOGLE_API_KEY)
load_dotenv()

from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent, Agent
from google.adk.tools.agent_tool import AgentTool
from content_creation_studio.sub_agents.intake_agent.agent import intake_agent
from content_creation_studio.sub_agents.topic_research_agent.agent import topic_research_agent
from content_creation_studio.sub_agents.content_drafter_agent.agent import content_drafter_agent
from content_creation_studio.sub_agents.quality_checker_agent.agent import quality_checker_agent
from content_creation_studio.sub_agents.content_improver_agent.agent import content_improver_agent
from content_creation_studio.sub_agents.blog_post_writer_agent.agent import blog_post_writer_agent
from content_creation_studio.sub_agents.social_media_creator_agent.agent import social_media_creator_agent
from content_creation_studio.sub_agents.email_newsletter_writer_agent.agent import email_newsletter_writer_agent
from content_creation_studio.sub_agents.seo_metadata_agent.agent import seo_metadata_agent
from content_creation_studio.sub_agents.content_analyzer_agent.agent import content_analyzer_agent
from content_creation_studio.sub_agents.final_packager_agent.agent import final_packager_agent

# --- Sequential: Research and Draft ---
research_and_draft_workflow = SequentialAgent(
    name="research_and_draft_workflow",
    sub_agents=[topic_research_agent, content_drafter_agent]
)

# --- Loop: Quality Improvement ---
quality_improvement_loop = LoopAgent(
    name="quality_improvement_loop",
    sub_agents=[quality_checker_agent, content_improver_agent],
    max_iterations=3
)

# --- Parallel: Multi-Channel Content Creation ---
parallel_content_creation = ParallelAgent(
    name="parallel_content_creation",
    sub_agents=[
        blog_post_writer_agent,
        social_media_creator_agent,
        email_newsletter_writer_agent,
        seo_metadata_agent
    ]
)

# --- Full Content Workflow ---
full_content_workflow = SequentialAgent(
    name="full_content_workflow",
    sub_agents=[
        intake_agent,
        research_and_draft_workflow,
        quality_improvement_loop,
        parallel_content_creation,
        final_packager_agent
    ]
)

# Create a content creation coordinator that runs the full workflow
content_creation_coordinator = Agent(
    name="content_creation_coordinator",
    model="gemini-2.5-flash",
    instruction="""
    You are a content creation coordinator. When user requests full content creation,
    delegate to the full_content_workflow to execute the complete pipeline:
    - Parse content brief
    - Research topics
    - Draft content
    - Improve quality
    - Create multi-channel content
    - Package deliverables

    Pass the user's request through to the workflow.
    """,
    sub_agents=[full_content_workflow]
)

# Wrap agents/workflows as tools
content_creation_tool = AgentTool(agent=content_creation_coordinator)
content_analyzer_tool = AgentTool(agent=content_analyzer_agent)

master_orchestrator_agent = Agent(
    name="master_orchestrator_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are the Master Content Creation Studio orchestrator. Delegate tasks to specialists.

    - For FULL content creation (topic research → draft → improve → multi-channel content),
      use `content_creation_tool`. Pass the complete user request with topic, audience, tone, and keywords.

    - For ANALYZING existing text (readability, word count, hashtags),
      use `content_analyzer_tool`.

    Always delegate to the appropriate tool. Present specialist responses clearly to the user.
    """,
    tools=[content_creation_tool, content_analyzer_tool]
)

root_agent = master_orchestrator_agent
