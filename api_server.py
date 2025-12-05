"""FastAPI server to expose the content creation agent."""

import os
import asyncio
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

# Load environment variables
load_dotenv()

from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai.types import Content, Part
from content_creation_studio.agent import root_agent

# Initialize FastAPI app
app = FastAPI(title="Content Creation Studio API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global session service
session_service = InMemorySessionService()


class ContentRequest(BaseModel):
    """Request model for content creation."""
    topic: str
    target_audience: str
    tone: str
    keywords: str
    session_id: Optional[str] = None


class AnalyzeRequest(BaseModel):
    """Request model for text analysis."""
    text: str


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Content Creation Studio API is running",
        "agent": root_agent.name
    }


@app.post("/api/create-content")
async def create_content(request: ContentRequest):
    """
    Create a complete content package.
    Returns streaming response with real-time updates.
    """
    try:
        # Create or retrieve session
        user_id = "web_user_001"

        if request.session_id:
            try:
                session = await session_service.get_session(
                    app_name=root_agent.name,
                    user_id=user_id,
                    session_id=request.session_id
                )
            except:
                session = await session_service.create_session(
                    app_name=root_agent.name,
                    user_id=user_id
                )
        else:
            session = await session_service.create_session(
                app_name=root_agent.name,
                user_id=user_id
            )

        # Build the query
        query = f"""Create a complete content package for:
- Topic: {request.topic}
- Target Audience: {request.target_audience}
- Tone: {request.tone}
- Keywords: {request.keywords}
"""

        # Create runner with LoggingPlugin
        runner = Runner(
            agent=root_agent,
            session_service=session_service,
            app_name=root_agent.name,
            plugins=[LoggingPlugin()]
        )

        async def generate():
            """Stream events as they occur."""
            try:
                final_response = None
                event_count = 0

                # Send initial status
                yield f"data: {json.dumps({'type': 'status', 'message': 'Starting content creation workflow...', 'session_id': session.id})}\n\n"

                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session.id,
                    new_message=Content(parts=[Part(text=query)], role="user")
                ):
                    event_count += 1

                    # Send progress update
                    event_data = {
                        'type': 'event',
                        'event_id': event_count,
                        'author': event.author if hasattr(event, 'author') else 'system',
                    }

                    if hasattr(event, 'content') and event.content:
                        if event.content.parts and len(event.content.parts) > 0:
                            text = event.content.parts[0].text
                            if text:
                                event_data['content_preview'] = text[:200]

                    yield f"data: {json.dumps(event_data)}\n\n"

                    # Check if final response
                    if event.is_final_response():
                        final_response = event.content.parts[0].text
                        yield f"data: {json.dumps({'type': 'complete', 'content': final_response, 'session_id': session.id})}\n\n"
                        break

                if not final_response:
                    yield f"data: {json.dumps({'type': 'error', 'message': 'No final response received'})}\n\n"

            except Exception as e:
                error_message = str(e)
                yield f"data: {json.dumps({'type': 'error', 'message': error_message})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-text")
async def analyze_text(request: AnalyzeRequest):
    """Analyze text snippet."""
    try:
        user_id = "web_user_001"
        session = await session_service.create_session(
            app_name=root_agent.name,
            user_id=user_id
        )

        query = f"Can you analyze this text snippet:\n\n{request.text}"

        runner = Runner(
            agent=root_agent,
            session_service=session_service,
            app_name=root_agent.name
        )

        final_response = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=Content(parts=[Part(text=query)], role="user")
        ):
            if event.is_final_response():
                final_response = event.content.parts[0].text
                break

        return {
            "status": "success",
            "analysis": final_response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("❌ ERROR: GOOGLE_API_KEY not found in environment variables!")
        exit(1)

    print("✅ Starting Content Creation Studio API Server")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Docs at: http://localhost:8000/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000)
