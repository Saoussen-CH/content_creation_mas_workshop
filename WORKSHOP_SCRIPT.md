# 🎤 Workshop Script: Building Multi-Agent Systems with Google ADK

## 📋 Workshop Overview (2 minutes)

**[OPENING]**

"Good morning/afternoon everyone! Welcome to the Content Creation Studio workshop for DevFest Fusion 4.0!

I'm [Your Name], and today we're going to build something really exciting - a complete multi-agent AI system that can create professional content packages including blog posts, social media content, and email newsletters.

**What we'll cover today:**
- ✅ Part 1-2: Building your first AI agents (1 hour)
- ✅ Part 3-6: Advanced agent patterns and workflows (2 hours)
- ✅ Part 7: The capstone project - our complete system (1 hour)
- ✅ Part 8: Deploying to production on Google Cloud (30 minutes)

**Total time:** About 4.5 hours with breaks.

**The best part?** Everything runs in Google Colab - no local setup required! Just your browser and your curiosity."

---

## 🚀 Getting Started (5 minutes)

**[SETUP INSTRUCTIONS]**

"Before we dive in, let's get everyone set up. Please open the README in our GitHub repository:

**https://github.com/Saoussen-CH/content_creation_mas_workshop**

You'll see a section called 'Workshop Notebooks - Start Here!' with colorful badges.

**Step 1:** Click the first badge - 'Part 1: First Agent'

**Step 2:** This opens Google Colab. Click 'Copy to Drive' to create your own copy

**Step 3:** We'll need a Google API key. Go to:
- **https://aistudio.google.com/app/apikey**
- Click 'Create API Key'
- Copy it - we'll use this in every notebook

**Important:** Don't share your API key with anyone!

Let me know by raising your hand when you have:
- ✋ Notebook open in Colab
- ✋ API key ready

Great! Let's begin our journey."

---

## 📓 Part 1: First Agent (20 minutes)

**[INTRODUCTION]**

"Let's start with the fundamentals. What IS an AI agent?

Think of an agent as an AI that can:
- ❌ Not just answer questions (like ChatGPT)
- ✅ But actually DO things - use tools, make decisions, complete tasks

In this first notebook, we're building an agent that can search Wikipedia and answer questions using real, up-to-date information.

**[WALKTHROUGH]**

Let me walk you through the key concepts:

**1. Installation** (Cell 1)
```python
pip install google-adk
```
This is Google's Agent Development Kit - our toolkit for building agents.

**2. Setting up your API key** (Cell 2)
Replace `'your-api-key-here'` with the API key you just created.

**3. Creating our first agent** (Cell 3)
Notice three key parts:
- `name`: What we call our agent
- `model`: We're using Gemini 2.0 Flash - fast and capable
- `instruction`: This is crucial - it tells the agent WHO it is and WHAT it can do

**4. The Wikipedia tool** (Cell 4)
This is where it gets interesting. We're giving our agent a TOOL - the ability to search Wikipedia.

**[RUN TOGETHER]**

Let's run this together:
- Everyone, run cells 1 through 5
- Watch what happens when we ask: 'Who won the 2024 Olympics gold in basketball?'

**[OBSERVE]**

See what's happening? The agent:
1. Reads your question
2. Decides 'I need to search Wikipedia'
3. Uses the tool
4. Analyzes the results
5. Gives you an answer

This is the power of agentic AI - it can use tools to accomplish tasks!

**[CHECK-IN]**

Quick show of hands:
- ✋ Who got a successful response?
- ✋ Any errors? (I'll help debug)

Take 5 minutes to experiment - try asking different questions!"

---

## 🔧 Part 2: Custom Tools (25 minutes)

**[TRANSITION]**

"Great job on Part 1! Now that you understand the basics, let's level up.

Wikipedia search is nice, but what if we want our agent to do something specific to OUR use case? That's where **custom tools** come in.

**[OPEN PART 2]**

Everyone, click the Part 2 badge in the README: 'Custom Tools'

**[CORE CONCEPT]**

In this notebook, we're building a content creation agent that needs specialized tools:
- 📊 Word counter
- 📝 Readability analyzer
- #️⃣ Hashtag generator

These aren't built-in tools - we're creating them ourselves!

**[KEY TECHNIQUE]**

Look at Cell 3 - the `@tool` decorator:
```python
@tool
def count_words(text: str) -> int:
```

This simple decorator turns ANY Python function into an agent tool. That's incredibly powerful!

**Notice:**
- Clear function name - the agent uses this to decide when to use it
- Type hints (`text: str`) - helps the agent understand what to pass
- Docstring - explains to the agent what the tool does

**[HANDS-ON]**

Let's run through this together:
- Run cells 1-4 to set up
- Cell 5: See how we give multiple tools to one agent
- Cell 6: Test it!

Try: 'Analyze this text: AI is transforming how we work and live every day'

**[OBSERVE TOGETHER]**

Watch the output - see how the agent:
1. Uses count_words
2. Then uses analyze_readability
3. Then generates hashtags
4. Finally summarizes everything

It's orchestrating multiple tools to complete a complex task!

**[CHALLENGE - 5 minutes]**

Here's a challenge: Can you add a new tool? Maybe:
- A sentiment analyzer
- An emoji suggester
- A title generator

Try modifying Cell 3 and see what happens!

**[DEBRIEF]**

Who successfully created a new tool? What did you make?

This is the foundation of everything we'll build today - agents using custom tools to solve real problems."

---

## 👥 Part 3: Agent Teams (30 minutes)

**[TRANSITION & BREAK]**

"Excellent work so far! Let's take a 10-minute break. When we come back, we'll learn how to make agents work together in teams.

Grab some coffee, stretch your legs, and we'll reconvene in 10 minutes!"

**[AFTER BREAK - INTRODUCTION]**

"Welcome back! You've built single agents with tools. Now imagine:
- One agent researches topics
- Another agent writes content
- A third agent checks quality
- A coordinator manages them all

This is multi-agent orchestration - and it's incredibly powerful!

**[OPEN PART 3]**

Click the Part 3 badge: 'Agent Teams'

**[CONCEPT EXPLANATION]**

In a multi-agent system:
- Each agent is a **specialist** - it does ONE thing really well
- A **coordinator** orchestrates them
- They work together like a real team

Look at Cell 4 - we have three specialist agents:
1. **Research Agent**: Finds information
2. **Writing Agent**: Creates content
3. **Quality Agent**: Reviews and scores

And in Cell 5, a **Coordinator** that manages them all.

**[KEY INSIGHT]**

Why multiple agents instead of one super-agent?

- ✅ **Clearer prompts**: Each agent has a focused job
- ✅ **Better results**: Specialists outperform generalists
- ✅ **Easier debugging**: Know exactly which agent needs fixing
- ✅ **Reusability**: Use the same agents in different workflows

**[HANDS-ON]**

Let's see this in action:
- Run cells 1-5 to create our team
- Cell 6: Make them work together!

Ask: 'Create a short blog post about sustainable living tips'

**[WATCH TOGETHER]**

See the magic? Each agent does its part:
- Research agent gathers info
- Writing agent creates the post
- Quality agent scores it
- Coordinator presents the final result

**[EXERCISE - 10 minutes]**

Experiment time! Try:
1. Changing the specialist instructions
2. Adding a fourth agent (maybe an SEO optimizer?)
3. Different topics

Share your best result in the chat!

**[WRAP UP]**

This is foundational to everything we're building - specialized agents working together. Next, we'll add structure to how they work."

---

## 🔗 Part 4: Sequential Workflows (25 minutes)

**[INTRODUCTION]**

"Now we're going to add STRUCTURE to our agent teams.

Sometimes, agents need to work in a specific order:
1. First, research the topic
2. Then, write a draft
3. Then, improve it
4. Finally, format it

This is a **sequential workflow** - like an assembly line!

**[OPEN PART 4]**

Click Part 4: 'Sequential Workflows'

**[CORE CONCEPT]**

Look at Cell 4 - the `SequentialAgent`:
```python
workflow = SequentialAgent(
    name="content_pipeline",
    sub_agents=[research, draft, improve, format]
)
```

This creates a pipeline where:
- Output from research → input to draft
- Output from draft → input to improve
- And so on...

**[REAL-WORLD ANALOGY]**

Think of it like cooking:
1. Prep ingredients (research)
2. Cook the meal (draft)
3. Season and adjust (improve)
4. Plate beautifully (format)

Each step builds on the previous one!

**[HANDS-ON]**

Run through cells 1-5. Watch how the workflow processes your request step-by-step.

Try: 'Create a tutorial about Python for beginners'

**[KEY OBSERVATION]**

Notice in the output - you can see each agent's work passing to the next. This transparency is crucial for debugging and quality control.

**[DISCUSSION]**

What kinds of tasks need sequential workflows?
- Content creation ✅
- Data processing ✅
- Code review processes ✅
- Customer support escalation ✅

Think about your own work - where could you use this pattern?"

---

## 🔄 Part 5: Iterative Workflows (30 minutes)

**[INTRODUCTION]**

"Sequential workflows are great when you know exactly what needs to happen. But what about when you need to IMPROVE something until it's good enough?

That's where **iterative workflows** come in - loops that keep refining until quality is achieved.

**[OPEN PART 5]**

Click Part 5: 'Iterative Workflows'

**[CONCEPT]**

Imagine you're editing an article:
1. Write a draft
2. Review it - score it
3. If score < 70: improve and go back to step 2
4. If score ≥ 70: done!

This is EXACTLY what a LoopAgent does!

**[CODE WALKTHROUGH - Cell 4]**

```python
quality_loop = LoopAgent(
    name="quality_improvement",
    sub_agents=[checker, improver],
    max_iterations=3
)
```

Key parameters:
- `sub_agents`: checker and improver work together
- `max_iterations`: safety limit (don't loop forever!)

**[THE MAGIC]**

The checker agent returns a quality score. If it's:
- **< 70**: The improver refines it, then check again
- **≥ 70**: Loop exits, content is approved!

This is how we ensure QUALITY, not just completion.

**[HANDS-ON]**

Run cells 1-5. Try:
'Write a product description for eco-friendly water bottles'

**[OBSERVE]**

Watch the iterations:
- Iteration 1: Initial score might be 60
- Iteration 2: Improved to 75 - Done!

Or maybe it takes 3 iterations. That's okay - we're prioritizing quality!

**[REAL-WORLD APPLICATIONS]**

Where do you use iterative refinement?
- Code review loops
- Design iterations
- Quality assurance
- Content editing

**[CHALLENGE - 5 minutes]**

Can you modify the quality threshold? Try changing:
- Quality score requirement (70 → 80?)
- Max iterations (3 → 5?)

See how it affects the output!"

---

## ⚡ Part 6: Parallel Workflows (30 minutes)

**[INTRODUCTION]**

"We've learned sequential (one after another) and iterative (refine until good). Now let's talk about SPEED.

What if you need to create:
- A blog post
- Social media posts
- An email newsletter
- SEO metadata

...all from the same content brief?

Running them sequentially would take too long. Let's run them in **PARALLEL**!

**[OPEN PART 6]**

Click Part 6: 'Parallel Workflows'

**[CONCEPT EXPLANATION]**

With `ParallelAgent`, multiple agents work SIMULTANEOUSLY:

```python
parallel_creation = ParallelAgent(
    name="multi_channel",
    sub_agents=[blog_writer, social_creator, email_writer, seo_agent]
)
```

Think of it like a restaurant kitchen:
- Chef 1: Makes appetizers
- Chef 2: Makes main course
- Chef 3: Makes dessert
- All at the SAME TIME!

**[EFFICIENCY GAINS]**

Sequential: 2 min + 2 min + 2 min + 2 min = 8 minutes
Parallel: max(2, 2, 2, 2) = 2 minutes!

**4x faster!**

**[HANDS-ON]**

Run cells 1-6. Try:
'Create content about healthy morning routines for busy professionals'

**[OBSERVE]**

All four content types are created simultaneously! Each specialized for its platform:
- Blog: Long-form, SEO-optimized
- Social: Short, engaging, platform-specific
- Email: Personal, clear CTA
- SEO: Keywords and meta tags

**[WHEN TO USE PARALLEL VS SEQUENTIAL]**

**Parallel**: When tasks are independent
- ✅ Multiple content formats
- ✅ Different translations
- ✅ Independent analyses

**Sequential**: When tasks depend on each other
- ✅ Research → Draft → Edit
- ✅ Extract → Transform → Load
- ✅ Design → Build → Test

**[MINI BREAK - 5 minutes]**

Great progress! Take 5 minutes. When we come back, we'll combine EVERYTHING into our capstone project!"

---

## 🎯 Part 7: Capstone Project (60 minutes)

**[BIG TRANSITION]**

"Alright everyone, this is where it all comes together!

You've learned:
- ✅ Basic agents and tools
- ✅ Agent teams
- ✅ Sequential workflows
- ✅ Iterative quality loops
- ✅ Parallel execution

Now we're going to combine ALL of these into one powerful system - the **Content Creation Studio**!

**[OPEN PART 7]**

Click Part 7: 'Capstone Project'

**[SYSTEM ARCHITECTURE EXPLANATION]**

Let me show you what we're building. Look at the diagram in the README.

This is a PRODUCTION-GRADE multi-agent system with:

**Phase 1: Intake & Research** (Sequential)
- Intake agent parses the brief
- Research agent finds trending topics

**Phase 2: Initial Draft** (Sequential)
- Content drafter creates first version

**Phase 3: Quality Loop** (Iterative - max 3 iterations)
- Quality checker scores it
- If score < 70: Content improver refines it
- Loop until quality ≥ 70

**Phase 4: Multi-Channel Creation** (Parallel)
- Blog post writer
- Social media creator
- Email newsletter writer
- SEO metadata agent
All working simultaneously!

**Phase 5: Packaging** (Sequential)
- Final packager assembles everything

**[THE MASTER ORCHESTRATOR]**

And coordinating ALL of this? The Master Orchestrator - it routes requests to the right workflow.

Two main workflows:
1. **Content Creation Coordinator**: Full pipeline we just described
2. **Content Analyzer**: Quick text analysis

**[CODE WALKTHROUGH]**

Let me highlight the key parts:

**Cell 3**: All our specialist agents
**Cell 4**: Building the workflows using Sequential, Loop, and Parallel agents
**Cell 5**: The master orchestrator that routes everything

This is 200+ lines of production code - and we understand every part because we built up to it!

**[HANDS-ON - GUIDED]**

Let's run this together, step by step:

**Step 1**: Run cells 1-5 (setup)

**Step 2**: Cell 6 - Full content creation

Try this request:
```
Create a complete content package for:
- Topic: AI tools for small business productivity
- Target Audience: Small business owners, non-technical
- Tone: Friendly and practical
- Keywords: AI tools, small business, automation, productivity
```

**Step 3**: Watch the magic happen!

This will take 2-3 minutes. Let's watch the workflow in action:
- See it parse the brief
- Research topics
- Draft content
- Improve quality (maybe 2-3 iterations)
- Generate all formats in parallel
- Package everything

**[WHILE WAITING]**

While this runs, let me explain what you're seeing:

Each agent reports its work. You can see:
- Which agent is running
- What it's doing
- The output it produces

This observability is crucial for production systems!

**[RESULTS REVIEW]**

Wow! Look at what we got:
- ✅ Professional blog post (800-1200 words)
- ✅ LinkedIn, Twitter, Instagram posts
- ✅ Email newsletter
- ✅ SEO metadata

All from one request! This is the power of orchestrated multi-agent systems.

**[EXERCISE - 20 minutes]**

Now it's your turn! Try creating content for:
1. Your own business/project
2. A topic you're passionate about
3. Something completely different

Experiment with:
- Different tones (professional, casual, humorous)
- Different audiences
- Different keywords

Share your best result!

**[CONTENT ANALYZER - BONUS]**

We also have a content analyzer. Try Cell 7:
```
Analyze this text: [paste some text]
```

It gives you:
- Word count
- Readability score
- Suggested hashtags

**[DISCUSSION - 10 minutes]**

Let's discuss:

**Q: What impressed you most about this system?**

**Q: Where could you use this in your work?**
- Marketing teams creating multi-channel campaigns?
- Content creators generating ideas?
- Documentation teams?

**Q: What would you add or change?**
- Image generation?
- Video script creation?
- Translation to multiple languages?

**[TRANSITION]**

Amazing work! We've built a complete production system.

But here's the question: Right now it runs in Colab. How do we deploy this to PRODUCTION where anyone can use it?

That's what we're covering next - and this is where it gets really exciting!"

---

## ☁️ Part 8: Deployment & Agent Engine (45 minutes)

**[LUNCH BREAK FIRST]**

"Before we dive into deployment, let's take a 30-minute lunch break. When we come back, I'll show you how to deploy our system to Google Cloud and make it accessible to the world!

See you in 30 minutes!"

**[AFTER LUNCH - INTRODUCTION]**

"Welcome back! I hope you're energized because we're about to take our system from notebook to PRODUCTION.

You've built an incredible multi-agent system. Now let's deploy it!

**[THE CHALLENGE]**

Right now our system:
- ✅ Works great in Colab
- ❌ Only you can use it
- ❌ Disappears when you close the tab
- ❌ No API for applications to call

We need to:
- ✅ Deploy to the cloud
- ✅ Make it accessible 24/7
- ✅ Provide an API
- ✅ Add a web interface

**[INTRODUCING AGENT ENGINE]**

Google Vertex AI Agent Engine is a managed service specifically for deploying agentic systems.

Think of it as:
- Heroku for agents
- Serverless for AI systems
- Fully managed, auto-scaling infrastructure

**[ARCHITECTURE OVERVIEW]**

Show the architecture diagram from README:

**Tier 1**: React Frontend (Cloud Run)
- Beautiful web interface
- Users interact here

**Tier 2**: FastAPI Backend (Cloud Run)
- REST API
- Connects to Agent Engine

**Tier 3**: Agent Engine (Vertex AI)
- Our multi-agent system
- Auto-scaling
- Fully managed

**[OPEN PART 8]**

Click Part 8: 'Deployment'

**[DEPLOYMENT WALKTHROUGH]**

For this part, I'll demonstrate while you follow along. Actual deployment requires:
- A Google Cloud account
- Billing enabled
- Some setup

**But I want you to understand HOW it works.**

**[STEP 1: Agent Engine Deployment]**

Look at Cell 3 - this is the key code:

```python
remote_app = agent_engines.create(
    agent_engine=adk_app,
    requirements=[...],
    display_name="content_creation_studio"
)
```

This packages our entire agent system and deploys it to Google Cloud.

What happens:
1. Code is packaged
2. Dependencies installed
3. Deployed to managed infrastructure
4. You get a resource name (like a URL for your agent)

**[STEP 2: Backend API]**

The backend is a FastAPI server that:
- Receives HTTP requests
- Forwards to Agent Engine
- Streams responses back

Look at the `api_server.py` code in the README.

Key endpoint:
```python
@app.post("/api/create-content")
async def create_content(request):
    # Forward to Agent Engine
    # Stream results back
```

**[STEP 3: Frontend]**

The React frontend gives users a beautiful interface:
- Form to input content brief
- Real-time progress updates
- Display formatted results

**[DEMO TIME]**

Let me show you the deployed version:

**[OPEN DEPLOYED APP IN BROWSER]**

**https://[your-cloud-run-url].run.app**

See this? This is our system running in production!

Watch as I:
1. Fill in the content brief
2. Click 'Generate'
3. Watch real-time progress
4. See all the generated content

**[OBSERVABILITY]**

In production, we need monitoring. Google Cloud provides:

**Cloud Logging**:
```bash
gcloud run services logs read content-studio
```

**Agent Tracing**:
- See exactly which agents ran
- How long each took
- What tools they used

This is crucial for debugging production issues!

**[COST DISCUSSION]**

Let's talk about costs:

**Cloud Run**:
- Scales to zero
- Only pay when requests are being handled
- ~$0.00002400 per request

**Agent Engine**:
- Pay per query/token
- Similar to API costs
- Optimized for production

**For a workshop or small project**: Maybe $5-20/month
**For production**: Scales with usage

**[DEPLOYMENT GUIDE]**

I've prepared complete deployment guides in the `deployment/` folder:

1. **setup_gcp.sh**: One-time GCP setup
2. **deploy.py**: Deploy agent to Agent Engine
3. **deploy-combined.sh**: Deploy frontend + backend
4. **cleanup_gcp.py**: Clean up everything when done

Everything is documented with step-by-step instructions!

**[CLEANUP IS IMPORTANT]**

And speaking of cleanup - to avoid unexpected charges:

```bash
python deployment/cleanup_gcp.py --all
```

This removes:
- Cloud Run services
- Agent Engine deployments
- Docker images
- Everything!

I've created a comprehensive cleanup guide so you won't have any surprises.

**[HANDS-ON - OPTIONAL]**

If you have a Google Cloud account and want to try deploying:
1. Follow the GETTING_STARTED.md guide
2. Run the deployment scripts
3. I'll help troubleshoot any issues

If not, that's okay - you understand the architecture and can deploy later!

**[Q&A - 10 minutes]**

Let's open it up for questions about deployment:
- Architecture?
- Costs?
- Scaling?
- Monitoring?
- Anything else?

**[CLOSING THOUGHTS]**

What we've covered is PRODUCTION-GRADE architecture. Many companies are deploying similar systems:
- Customer support automation
- Content generation platforms
- Data analysis pipelines
- Code review systems

You now have the knowledge and the code to build your own!"

---

## 🎓 Workshop Wrap-Up (10 minutes)

**[RECAP]**

"Wow, what a journey! Let's recap what we've accomplished today:

**✅ Part 1-2**: Built agents with custom tools
**✅ Part 3**: Created agent teams
**✅ Part 4**: Designed sequential workflows
**✅ Part 5**: Implemented iterative quality loops
**✅ Part 6**: Optimized with parallel execution
**✅ Part 7**: Combined everything into a production system
**✅ Part 8**: Learned production deployment

You didn't just learn ABOUT multi-agent systems - you BUILT one!

**[RESOURCES]**

Everything we covered is available:

**GitHub Repository**:
https://github.com/Saoussen-CH/content_creation_mas_workshop

**What's included**:
- ✅ All 8 notebooks (always available in Colab)
- ✅ Complete source code
- ✅ Deployment scripts
- ✅ Documentation
- ✅ Cleanup guides

**Star the repo** so you can find it later!

**[NEXT STEPS]**

Where do you go from here?

**1. Experiment**:
- Modify the agents
- Add new tools
- Change workflows
- Deploy your version!

**2. Learn More**:
- Google ADK documentation
- Vertex AI Agent Engine docs
- Multi-agent design patterns

**3. Build Something Real**:
- Automate a workflow at work
- Create a side project
- Build a product

**4. Share**:
- Tweet about what you built
- Blog about your experience
- Help others learn

**[COMMUNITY]**

Join the conversation:
- DevFest Fusion 4.0 community
- Google Cloud communities
- Share your projects with #DevFestFusion

**[FEEDBACK]**

I'd love your feedback:
- What was most valuable?
- What was confusing?
- What should we add?

Please fill out the feedback form [if you have one] or reach out on [your contact method].

**[FINAL THOUGHTS]**

Multi-agent AI systems are transforming how we build software. You're now equipped to:
- Design agent architectures
- Implement complex workflows
- Deploy production systems

This is just the beginning. The field is evolving rapidly, and you have the foundation to grow with it.

**Thank you for your energy, your questions, and your participation! You've been an amazing group. Now go build something incredible!**

**Questions before we wrap up?**"

---

## 📞 Post-Workshop Support

**[IF TIME PERMITS]**

"I'll stick around for 15 minutes if anyone wants:
- Help debugging their notebooks
- Guidance on deployment
- Advice on their specific use case
- Just to chat about AI agents!

Thank you again, and enjoy the rest of DevFest Fusion 4.0!"

---

## 🎯 Facilitation Tips

### Time Management
- Have a visible timer
- Give 5-minute warnings before transitions
- Be flexible - skip advanced parts if running late

### Engagement
- Ask questions frequently
- Call on specific people occasionally
- Acknowledge good questions/contributions
- Use chat for people to share results

### Troubleshooting
- Have backup notebooks ready
- Know common API key errors
- Prepare for Colab connection issues
- Have a helper if possible

### Energy Management
- Take breaks every 60-90 minutes
- Use energy shifts (discussion, hands-on, demo)
- Celebrate wins ("Great job everyone!")
- Keep enthusiasm high

### Common Issues & Solutions

**API Key Errors**:
```
Error: API key not valid
Solution: Make sure to copy the full key, check for extra spaces
```

**Colab Disconnects**:
```
Issue: Runtime disconnected
Solution: Reconnect and re-run cells from the top
```

**Import Errors**:
```
Error: Module not found
Solution: Re-run the pip install cell
```

**Rate Limiting**:
```
Error: 429 Too many requests
Solution: Wait 60 seconds, then try again
```

### Backup Plan

If live coding fails:
- Have screenshots of expected outputs
- Pre-run notebooks with results
- Show deployed production version
- Focus on concepts over execution

Good luck with your workshop! 🚀
