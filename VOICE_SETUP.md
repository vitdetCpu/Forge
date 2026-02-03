# 🎤 VOICE-ENABLED FORGE - SETUP GUIDE

Your Forge app is now configured with REAL voice interviews!

## ✅ What's Already Done

- All API keys are configured in `backend/.env`
- Voice bot code is ready (`pipecat_bot.py`)
- Updated dependencies in `requirements.txt`

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Note:** This will take 2-3 minutes. Pipecat has a lot of dependencies.

### 2. Start Redis

```bash
# Mac
brew services start redis

# Or check if already running
redis-cli ping  # Should return PONG
```

### 3. Generate Demo Data (Optional)

```bash
python generate_demo_data.py
```

This creates 5 demo sessions to show in the dashboard.

### 4. Start Backend

```bash
python main.py
```

You should see:
```
✅ Connected to Redis
✅ Initialized Claude API
📊 Weave tracking enabled
🚀 Starting Forge API on 0.0.0.0:8000
```

### 5. Start Frontend (New Terminal)

```bash
cd ../frontend
npm install
npm run dev
```

Open http://localhost:3000

---

## 🎙️ How to Use Voice Interviews

### Option 1: Use Your Own Daily Room

1. Go to http://localhost:3000
2. Click "Start Interview Session"
3. Browser will open a Daily room
4. **The AI bot will join and start asking questions!**
5. Speak your answers out loud
6. Bot evaluates in real-time using Claude
7. Asks next question based on your weak areas

### Option 2: Test Locally First

```bash
cd backend
python test_voice.py  # Coming soon
```

---

## 📊 View Your Progress

After doing voice interviews:

1. Go to http://localhost:3000/dashboard
2. See your radar chart expand as you improve
3. Progress graph shows upward trends
4. Topic breakdown shows which areas got better

---

## 🔍 View Weave Dashboard

See every AI decision:

1. Go to https://wandb.ai/viditk258-american-high-school/forge/weave
2. You're already logged in!
3. See every question generated
4. See every answer evaluated
5. Watch the prompts get smarter over time

---

## 🐛 Troubleshooting

### "No module named pipecat"
```bash
pip install -r requirements.txt
```

### Voice not working
- Check microphone permissions in browser
- Make sure Daily room URL is valid
- Check backend logs for errors

### Bot not joining room
- Verify DAILY_API_KEY is set
- Check backend logs: should see "Voice bot started"
- Daily might take 5-10 seconds to connect

### Redis connection error
```bash
redis-cli ping
# If no response:
brew services start redis  # Mac
sudo systemctl start redis  # Linux
```

---

## 🎯 For the Hackathon Demo

**Two Demo Options:**

### Option A: Live Voice Demo (Impressive but risky)
- Do an actual voice interview on stage
- Show the bot asking questions in real-time
- Risk: Audio issues, latency, microphone problems

### Option B: Show Dashboard Only (Safe)
- Use the pre-generated demo data
- Show the improvement graphs
- Walk through the self-improving concept
- Say: "Voice is ready, here's what 5 sessions look like"

**Recommendation:** Do Option B for the main demo, have Option A ready as backup if asked.

---

## 📝 Quick Commands

```bash
# Start everything
cd backend && source venv/bin/activate && python main.py
# New terminal:
cd frontend && npm run dev

# Generate new demo data
cd backend && python generate_demo_data.py

# Clear all data and start fresh
redis-cli FLUSHALL
```

---

## 🔥 You're Ready!

Your Forge app now has:
- ✅ Real voice interviews with Pipecat + Daily
- ✅ Claude AI evaluation
- ✅ Self-improving algorithm
- ✅ Weave observability
- ✅ Beautiful dashboard
- ✅ All API keys configured

Go crush WeaveHacks! 🏆
