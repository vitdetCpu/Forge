"""
Redis storage layer for session data and knowledge tracking
"""

import os
import json
import redis
from datetime import datetime
from typing import Dict, List, Optional
import uuid

class SessionStorage:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis = redis.from_url(redis_url, decode_responses=True)
        print(f"✅ Connected to Redis at {redis_url}")
    
    def create_session(self, user_id: str) -> str:
        """Create a new interview session"""
        session_id = f"sess_{uuid.uuid4().hex[:8]}"
        
        session_data = {
            "id": session_id,
            "user_id": user_id,
            "started_at": datetime.now().isoformat(),
            "ended_at": None,
            "questions": [],
            "current_scores": {}
        }
        
        # Store session
        self.redis.set(f"session:{session_id}", json.dumps(session_data))
        
        # Add to user's session list
        self.redis.lpush(f"user:{user_id}:sessions", session_id)
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        data = self.redis.get(f"session:{session_id}")
        return json.loads(data) if data else None
    
    def update_session(self, session_id: str, updates: Dict):
        """Update session data"""
        session = self.get_session(session_id)
        if session:
            session.update(updates)
            self.redis.set(f"session:{session_id}", json.dumps(session))
    
    def add_question(self, session_id: str, question: str, answer: str, score: float, topic: str, weak_points: List[str]):
        """Add a question and answer to the session"""
        session = self.get_session(session_id)
        if not session:
            return
        
        question_data = {
            "question": question,
            "answer": answer,
            "score": score,
            "topic": topic,
            "weak_points": weak_points,
            "timestamp": datetime.now().isoformat()
        }
        
        session["questions"].append(question_data)
        
        # Update current scores
        if topic not in session["current_scores"]:
            session["current_scores"][topic] = []
        session["current_scores"][topic].append(score)
        
        self.redis.set(f"session:{session_id}", json.dumps(session))
        
        # Update knowledge map
        self._update_knowledge_map(session["user_id"], topic, score)
    
    def _update_knowledge_map(self, user_id: str, topic: str, score: float):
        """Update user's knowledge map with new score"""
        key = f"knowledge:{user_id}"
        
        # Get current knowledge map
        data = self.redis.get(key)
        knowledge_map = json.loads(data) if data else {}
        
        if topic not in knowledge_map:
            knowledge_map[topic] = []
        
        knowledge_map[topic].append(score)
        
        self.redis.set(key, json.dumps(knowledge_map))
    
    def end_session(self, session_id: str):
        """Mark session as ended"""
        session = self.get_session(session_id)
        if session:
            session["ended_at"] = datetime.now().isoformat()
            self.redis.set(f"session:{session_id}", json.dumps(session))
    
    def calculate_session_scores(self, session_id: str) -> Dict[str, float]:
        """Calculate average scores per topic for a session"""
        session = self.get_session(session_id)
        if not session:
            return {}
        
        topic_scores = {}
        for question in session["questions"]:
            topic = question["topic"]
            if topic not in topic_scores:
                topic_scores[topic] = []
            topic_scores[topic].append(question["score"])
        
        # Calculate averages
        return {
            topic: sum(scores) / len(scores) / 10.0  # Normalize to 0-1
            for topic, scores in topic_scores.items()
        }
    
    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """Get all sessions for a user"""
        session_ids = self.redis.lrange(f"user:{user_id}:sessions", 0, -1)
        
        sessions = []
        for session_id in session_ids:
            session = self.get_session(session_id)
            if session:
                # Calculate average score
                total_score = 0
                count = 0
                for q in session["questions"]:
                    total_score += q["score"]
                    count += 1
                
                sessions.append({
                    "id": session["id"],
                    "date": session["started_at"],
                    "started_at": session["started_at"],
                    "ended_at": session.get("ended_at"),
                    "questions_asked": len(session["questions"]),
                    "average_score": total_score / count if count > 0 else 0,
                    "questions": session["questions"]
                })
        
        return sessions
    
    def get_knowledge_map(self, user_id: str) -> Dict:
        """Get user's knowledge map and history"""
        key = f"knowledge:{user_id}"
        data = self.redis.get(key)
        knowledge_data = json.loads(data) if data else {}
        
        # Calculate current scores (average of recent scores)
        topics = {}
        for topic, scores in knowledge_data.items():
            # Use last 3 scores for current level
            recent_scores = scores[-3:] if len(scores) >= 3 else scores
            topics[topic] = sum(recent_scores) / len(recent_scores) / 10.0 if recent_scores else 0
        
        # Build history (session by session)
        sessions = self.get_user_sessions(user_id)
        
        # IMPORTANT: Reverse to get chronological order (oldest first)
        # Redis LPUSH stores newest first, but we want oldest → newest for progression
        sessions_chronological = list(reversed(sessions))
        
        history = []
        
        for idx, session in enumerate(sessions_chronological, 1):
            session_data = {"session": idx}
            
            # Calculate scores for each topic in this session
            for question in session["questions"]:
                topic = question["topic"]
                if topic not in session_data:
                    session_data[topic] = []
                session_data[topic].append(question["score"])
            
            # Average scores for this session
            for topic, scores in session_data.items():
                if topic != "session":
                    session_data[topic] = sum(scores) / len(scores) / 10.0
            
            history.append(session_data)
        
        return {
            "topics": topics,
            "history": history
        }
    
    def calculate_improvement(self, user_id: str) -> Dict[str, float]:
        """Calculate improvement per topic"""
        knowledge_map = self.get_knowledge_map(user_id)
        history = knowledge_map.get("history", [])
        
        if len(history) < 2:
            return {}
        
        first_session = history[0]
        last_session = history[-1]
        
        improvement = {}
        for topic in last_session:
            if topic == "session":
                continue
            
            if topic in first_session:
                improvement[topic] = last_session[topic] - first_session[topic]
        
        return improvement
