"""
Main FastAPI server for Interview Prep Agent
Handles API endpoints for frontend communication
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

from storage import SessionStorage
from bot import create_daily_room
from evaluator import InterviewEvaluator
import threading

# Load environment variables FIRST (force override to ignore stale shell vars)
load_dotenv(override=True)

# Check if voice is configured AFTER loading env
VOICE_ENABLED = bool(os.getenv("DEEPGRAM_API_KEY")) and bool(os.getenv("DAILY_API_KEY"))

# Initialize FastAPI app
app = FastAPI(title="Forge API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize storage and evaluator
storage = SessionStorage()
evaluator = InterviewEvaluator()

# Request/Response models
class StartSessionRequest(BaseModel):
    user_id: str

class StartSessionResponse(BaseModel):
    session_id: str
    daily_room_url: str
    daily_token: str = ""

class EndSessionRequest(BaseModel):
    session_id: str

class SessionStatusResponse(BaseModel):
    current_question: str
    transcript: str
    questions_asked: int
    current_scores: dict

@app.get("/")
async def root():
    return {
        "message": "Forge API - Forge your interview skills",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/start-session", response_model=StartSessionResponse)
async def start_session(request: StartSessionRequest):
    """Create a new interview session and Daily room"""
    try:
        # Create session in storage
        session_id = storage.create_session(request.user_id)
        
        # Create Daily room
        room_info = create_daily_room(session_id)
        
        # Start bot in the room if voice is enabled
        if VOICE_ENABLED:
            from pipecat_bot import run_interview_bot
            import asyncio
            
            # Schedule bot to run in background using asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Create background task
            loop.create_task(run_interview_bot(
                room_info["url"],
                room_info.get("token", ""),  # Pass the token
                session_id, 
                storage, 
                evaluator
            ))
            print(f"✅ Voice bot started for session {session_id}")
        else:
            print(f"⚠️  Voice disabled - missing API keys (need DEEPGRAM_API_KEY and DAILY_API_KEY)")
        
        return StartSessionResponse(
            session_id=session_id,
            daily_room_url=room_info["url"],
            daily_token=room_info.get("token", "")
        )
    except Exception as e:
        import traceback
        print(f"❌ ERROR in start_session: {e}")
        print(f"❌ Full traceback:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/end-session")
async def end_session(request: EndSessionRequest):
    """End an interview session and calculate final scores"""
    try:
        session = storage.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Mark session as ended
        storage.end_session(request.session_id)
        
        # Calculate final scores and improvement
        final_scores = storage.calculate_session_scores(request.session_id)
        improvement = storage.calculate_improvement(session["user_id"])
        
        return {
            "final_scores": final_scores,
            "improvement": improvement
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session-status")
async def get_session_status(session_id: str):
    """Get current status of an active session"""
    try:
        session = storage.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get current state
        questions = session.get("questions", [])
        current_question = questions[-1]["question"] if questions else ""
        transcript = questions[-1].get("answer", "") if questions else ""
        
        return SessionStatusResponse(
            current_question=current_question,
            transcript=transcript,
            questions_asked=len(questions),
            current_scores=session.get("current_scores", {})
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions")
async def get_sessions(user_id: str):
    """Get all sessions for a user"""
    try:
        sessions = storage.get_user_sessions(user_id)
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge-map")
async def get_knowledge_map(user_id: str):
    """Get knowledge map and history for a user"""
    try:
        knowledge_map = storage.get_knowledge_map(user_id)
        return knowledge_map
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Forge API on {host}:{port}")
    print(f"📊 Weave project: {os.getenv('WEAVE_PROJECT', 'Not configured')}")
    print(f"💾 Redis: {os.getenv('REDIS_URL', 'Not configured')}")
    
    uvicorn.run(app, host=host, port=port)
