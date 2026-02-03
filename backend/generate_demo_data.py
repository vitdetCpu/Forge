"""
Generate synthetic demo data to show the self-improving aspect
This creates 5 sessions with improving scores over time
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

from storage import SessionStorage
from question_bank import get_question, get_all_topics

def generate_demo_data():
    """Generate 5 demo sessions showing improvement"""
    
    storage = SessionStorage()
    user_id = "demo_user"
    
    print("🎯 Generating demo data for showcase...")
    print(f"   User: {user_id}")
    
    # Define progression: scores improve over sessions
    # IMPORTANT: Each session should practice ALL topics to show clear progression
    sessions_data = [
        {
            "session_num": 1,
            "topics": {
                "leadership": [4.0, 4.5, 5.0],  # Weak
                "algorithms": [3.0, 3.5, 4.0],   # Very weak - focus area
                "system_design": [5.0, 5.5, 6.0], # OK
                "conflict_resolution": [4.5, 5.0, 5.5], # Weak
            }
        },
        {
            "session_num": 2,
            "topics": {
                "leadership": [5.5, 6.0, 6.0],   # Improving
                "algorithms": [5.0, 5.5, 6.0],   # Improving (focused practice)
                "system_design": [6.0, 6.5, 7.0], # Improving
                "conflict_resolution": [6.0, 6.5, 6.5], # Improving
            }
        },
        {
            "session_num": 3,
            "topics": {
                "leadership": [6.5, 7.0, 7.0],   # Getting better
                "algorithms": [6.5, 7.0, 7.5],   # Getting much better
                "system_design": [7.0, 7.5, 7.5], # Good
                "conflict_resolution": [7.0, 7.0, 7.5], # Good
            }
        },
        {
            "session_num": 4,
            "topics": {
                "leadership": [7.5, 8.0, 8.0],   # Strong
                "algorithms": [7.5, 8.0, 8.5],   # Much better - rapid improvement
                "system_design": [8.0, 8.0, 8.5], # Strong
                "conflict_resolution": [7.5, 8.0, 8.5], # Strong
            }
        },
        {
            "session_num": 5,
            "topics": {
                "leadership": [8.0, 8.5, 9.0],   # Very strong
                "algorithms": [8.5, 9.0, 9.0],   # Expert now! Biggest improvement
                "system_design": [8.5, 8.5, 9.0], # Expert
                "conflict_resolution": [8.5, 9.0, 9.0], # Expert
            }
        }
    ]
    
    for session_data in sessions_data:
        # Create session
        session_id = storage.create_session(user_id)
        print(f"\n📝 Session {session_data['session_num']} (ID: {session_id})")
        
        # Add questions for each topic
        for topic, scores in session_data["topics"].items():
            for idx, score in enumerate(scores):
                question = get_question(topic, "medium")
                
                # Generate synthetic answer
                answer = f"In my previous role at TechCorp, I {topic} by implementing a solution that resulted in measurable impact..."
                
                # Generate weak points based on score
                if score < 5:
                    weak_points = ["Missing specific metrics", "Vague impact statement", "No STAR format"]
                elif score < 7:
                    weak_points = ["Could provide more specific numbers", "Result could be stronger"]
                else:
                    weak_points = ["Minor: Could add one more concrete example"]
                
                storage.add_question(
                    session_id=session_id,
                    question=question,
                    answer=answer,
                    score=score,
                    topic=topic,
                    weak_points=weak_points
                )
                
                print(f"  ✓ {topic}: {score}/10")
        
        # Mark session as complete
        storage.end_session(session_id)
    
    print("\n✅ Demo data generated successfully!")
    print("\nResults:")
    
    # Show final knowledge map
    knowledge_map = storage.get_knowledge_map(user_id)
    print("\n📊 Final Knowledge Map:")
    for topic, score in sorted(knowledge_map["topics"].items(), key=lambda x: -x[1]):
        print(f"   {topic}: {score*10:.1f}/10")
    
    # Show improvement
    improvement = storage.calculate_improvement(user_id)
    print("\n📈 Overall Improvement:")
    for topic, change in sorted(improvement.items(), key=lambda x: -x[1]):
        print(f"   {topic}: +{change*10:.1f} points")
    
    print("\n🎉 Ready for demo! Start the frontend and backend to see the results.")

if __name__ == "__main__":
    generate_demo_data()
