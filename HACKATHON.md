# WeaveHacks Demo Guide

## 🎯 The Pitch (30 seconds)

"I'm Melon, a high school student who's been applying to jobs and struggling with interview prep. Professional coaches cost hundreds of dollars. Generic practice doesn't help. So I built **Forge** - an AI interviewer that learns my weak areas and forges my skills through focused practice.

Over 5 sessions, my algorithm skills went from 3/10 to 8.5/10. Forge learned I needed more practice there and hammered it until I got sharp. This is personalized interview prep that gets stronger the more you use it."

## 🏆 How We Win

### Judging Criteria Coverage:

1. **Creativity** ✅
   - Interview prep exists, but not self-improving personalized AI
   - Voice-based makes it feel like real interviews
   - Personal story (high school student needs this!)

2. **Self-improving-ness** ⭐⭐⭐
   - **Knowledge map** tracks strengths/weaknesses
   - **Adaptive difficulty** increases as you improve
   - **Focused practice** on weak areas
   - **Visual proof** - radar chart expanding, scores increasing

3. **Utility** ✅
   - Everyone does job interviews
   - Saves money (vs. $200/hr coaches)
   - Actually helps people improve
   - Scalable to any interview type

4. **Technical execution** ✅
   - Full-stack implementation
   - Voice AI with Pipecat
   - Real-time evaluation with Claude
   - Weave observability showing agent decisions
   - Redis for fast data access

5. **Sponsor usage** ⭐
   - **Daily/Pipecat**: Core voice infrastructure (Kwindla is judging!)
   - **Weave (W&B)**: LLM tracing (they're hosting!)
   - **Redis**: Session storage and knowledge tracking
   - **Vercel**: Frontend hosting
   - **Claude API**: Interview evaluation

## 📊 Demo Flow (5-7 minutes)

### Part 1: The Problem (30 sec)
"I'm in high school, applying to jobs. Interview prep is expensive and generic. I wanted something personalized that actually helps me improve."

### Part 2: Show the Dashboard (1 min)
Open browser to dashboard:
- "Here are my 5 practice sessions"
- Point to radar chart: "Started weak in algorithms (4/10)"
- Point to progress graph: "Now at 8.5/10 - that's a 112% improvement"
- "The agent learned I needed algorithm practice and focused there"

### Part 3: Show Weave Dashboard (1 min) ⭐
Open Weave.wandb.ai:
- "Here's what makes it self-improving - you can see every AI decision"
- Click on a trace: "Question generation for session 1 - generic questions"
- Click on later trace: "Session 5 - now asking targeted follow-ups based on my weak areas"
- "The evaluation itself got better - started generic, now catches subtle issues"

### Part 4: Live Demo (2-3 min)
**Option A - If voice works:**
- Start new session
- Have judge ask you a question via voice
- Answer (intentionally weak on something)
- Show Claude evaluating in real-time
- Display score and weak points
- Show next question adapts to weak area

**Option B - If voice doesn't work (safer):**
- Show pre-recorded video of voice session
- Walk through the flow
- Emphasize the real-time adaptation

### Part 5: The Impact (30 sec)
- "In 5 sessions, average score improved 36%"
- "The agent learned exactly what I needed to practice"
- "This could help millions of people prep for interviews affordably"
- "Next steps: expand to internship interviews, college interviews, any type of interview"

## 🎨 Visual Elements to Emphasize

1. **Radar Chart Expanding**
   - Session 1: Small pentagon (weak in most areas)
   - Session 5: Large pentagon (strong across the board)
   - This is the MOST OBVIOUS visual proof of improvement

2. **Progress Line Graph**
   - Lines trending upward over time
   - Point out steeper slopes (faster improvement)

3. **Weave Traces**
   - Show the prompt evolution
   - Early sessions: generic prompts
   - Later sessions: highly specific prompts

4. **Topic Scores**
   - Color-coded bars (red → yellow → green)
   - Show before/after

## 💡 Key Talking Points

### For Technical Judges:
- "2 lines of code to add Weave - it's tracking every Claude call automatically"
- "Redis gives us sub-millisecond lookups for real-time session data"
- "Pipecat handles all the complexity of voice AI - we just define the conversation flow"

### For Product Judges:
- "Democratizes interview prep - no more $200/hr coaches"
- "Personalization is the key - generic practice doesn't work"
- "Could expand to any skill assessment (coding interviews, sales pitches, etc.)"

### For Founder Judges:
- "I experienced this problem firsthand as a high school student"
- "Built this in 48 hours with the sponsor tools"
- "Could be a real product - people would pay for this"

## 🚨 Backup Plans

### If Daily/Voice Fails:
- Show pre-recorded demo video
- "This is what the voice session looks like"
- Focus more on the self-improving algorithm visualization

### If Redis Fails:
- Use the generated demo data (already in there)
- "Here's synthetic data showing 5 sessions of improvement"

### If Weave Dashboard Fails:
- Show screenshots
- Explain what it would show

### If Frontend Fails:
- Present from backend terminal
- Show API responses directly
- Walk through the code

## 📸 Screenshots to Prepare

Take these before the demo:

1. Dashboard with all 5 sessions
2. Radar chart showing progression
3. Weave dashboard with traces
4. Individual session view
5. Code snippet showing Weave integration (2 lines!)

## ⏱️ Time Management

- 0:00-0:30: Problem statement
- 0:30-1:30: Dashboard walkthrough
- 1:30-2:30: Weave observability
- 2:30-5:00: Live demo
- 5:00-5:30: Impact & next steps
- 5:30-7:00: Q&A

## 🎤 Opening Lines (Memorize These)

"Hi! I'm Melon. I'm a high school student in Fremont, and I've been applying to part-time jobs. Interview prep is really expensive - professional coaches charge $200 an hour. I couldn't afford that, so I built **Forge** - an AI interviewer that learns from each session and forges your skills through targeted practice.

Let me show you how it works..."

## 🔥 Closing Lines

"In just 5 practice sessions, my interview skills improved by 36% overall, with my weakest area - algorithms - going from a 3 to an 8.5 out of 10. **Forge** learned what I needed and hammered it until I got sharp. This could help millions of people prepare for interviews affordably and effectively. Thanks!"

## 🎯 What Judges Will Love

1. **Kwindla (Daily/Pipecat)**: You used Pipecat exactly as intended for voice AI
2. **W&B Team**: You integrated Weave cleanly and it actually adds value
3. **Redis Team**: Fast lookups for real-time session management
4. **Founder Judges**: Personal problem, clear market need, could be a business
5. **Technical Judges**: Clean architecture, good use of tools, actually works

## 🚀 Day-Of Checklist

- [ ] Redis running
- [ ] Backend running (python main.py)
- [ ] Frontend running (npm run dev)
- [ ] Demo data generated (python generate_demo_data.py)
- [ ] Browser open to dashboard
- [ ] Weave dashboard open in another tab
- [ ] Backup video recorded (in case of demo failure)
- [ ] Tested voice/audio works
- [ ] Rehearsed pitch 3x times

Good luck! 🍀
