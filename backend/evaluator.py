"""
Interview answer evaluation using Claude API with Weave observability
"""

import os
from anthropic import Anthropic
import weave
from typing import Dict, List, Tuple

# Initialize Weave (2 lines of code!)
weave_project = os.getenv("WEAVE_PROJECT", "forge")
weave.init(weave_project)

class InterviewEvaluator:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        print(f"✅ Initialized Claude API")
        print(f"📊 Weave tracking enabled for project: {weave_project}")
    
    @weave.op()
    def evaluate_answer(self, question: str, answer: str, topic: str) -> Tuple[float, List[str]]:
        """Evaluate an interview answer using Claude"""
        
        prompt = f"""You are an expert interview coach evaluating a candidate's answer.

Question: {question}
Topic: {topic}
Candidate's Answer: {answer}

Evaluate this answer on a scale of 0-10 considering:
1. Completeness and depth
2. Use of STAR method (Situation, Task, Action, Result) for behavioral questions
3. Technical accuracy for technical questions
4. Specific examples and metrics
5. Clarity and communication

Provide your evaluation in this exact format:

SCORE: [number 0-10]
WEAK_POINTS:
- [weakness 1]
- [weakness 2]
- [weakness 3]

Be constructive and specific."""

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            # Extract score
            score = 5.0
            if "SCORE:" in content:
                score_line = [line for line in content.split('\n') if line.strip().startswith("SCORE:")][0]
                score_str = score_line.replace("SCORE:", "").strip()
                try:
                    score = float(score_str)
                except:
                    score = 5.0
            
            # Extract weak points
            weak_points = []
            if "WEAK_POINTS:" in content:
                in_weak_points = False
                for line in content.split('\n'):
                    if "WEAK_POINTS:" in line:
                        in_weak_points = True
                        continue
                    if in_weak_points and line.strip().startswith('-'):
                        weak_points.append(line.strip()[1:].strip())
            
            return score, weak_points
            
        except Exception as e:
            print(f"❌ Error evaluating answer: {e}")
            return 5.0, ["Unable to evaluate - API error"]
    
    @weave.op()
    def generate_next_question(self, topic: str, difficulty: str, knowledge_map: Dict[str, float]) -> str:
        """Generate next interview question based on weak areas"""
        
        weak_topics = sorted(knowledge_map.items(), key=lambda x: x[1])[:2]
        weak_topics_str = ", ".join([t for t, _ in weak_topics])
        
        prompt = f"""You are an expert interview coach creating personalized interview questions.

Generate a {difficulty} difficulty {topic} interview question.

Context:
- The candidate is weakest in: {weak_topics_str}
- Focus the question on helping them improve these areas
- Make it realistic and commonly asked in real interviews

Provide ONLY the question, no additional commentary."""

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"❌ Error generating question: {e}")
            return f"Tell me about a time you dealt with a challenging {topic} situation."
    
    @weave.op()
    def select_next_topic(self, knowledge_map: Dict[str, float], previous_topics: List[str]) -> str:
        """Select the next topic to focus on based on knowledge map"""
        
        if not knowledge_map:
            default_topics = ["leadership", "algorithms", "system_design", "conflict_resolution"]
            return default_topics[len(previous_topics) % len(default_topics)]
        
        sorted_topics = sorted(knowledge_map.items(), key=lambda x: x[1])
        
        for topic, score in sorted_topics:
            if not previous_topics or topic != previous_topics[-1]:
                return topic
        
        return sorted_topics[0][0] if sorted_topics else "behavioral"
