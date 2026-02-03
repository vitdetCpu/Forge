# Forge

**Forge your interview skills with AI that learns and adapts.**

A voice-based mock interviewer that identifies your weaknesses and focuses practice where you need it most. Every session makes you sharper.

## Features

- 🎤 **Voice-based interviews** using Daily + Pipecat
- 🧠 **Self-improving** - learns your weak areas and focuses practice there
- 📊 **Visual progress tracking** with radar charts and improvement graphs
- 🔍 **Full observability** with Weave (W&B) - see every AI decision
- ⚡ **Fast storage** with Redis

## Tech Stack

- **Frontend**: Next.js 14 (React) on Vercel
- **Backend**: Python with Pipecat framework
- **Voice**: Daily (WebRTC infrastructure)
- **AI**: Claude API (Anthropic)
- **Storage**: Redis
- **Observability**: Weave (Weights & Biases)

## Project Structure

```
interview-prep-agent/
├── frontend/          # Next.js web app
│   ├── app/          # Next.js 14 app router
│   ├── components/   # React components
│   └── lib/          # API clients
└── backend/          # Python Pipecat bot
    ├── main.py       # Entry point
    ├── bot.py        # Pipecat voice bot
    ├── evaluator.py  # Claude API integration
    └── storage.py    # Redis operations
```

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- Redis running locally or cloud instance
- API Keys:
  - Anthropic API key
  - Daily API key
  - Deepgram API key (for speech-to-text)
  - ElevenLabs API key (for text-to-speech)

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your backend URL
npm run dev
# Runs on http://localhost:3000
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py
# Runs on http://localhost:8000
```

### Redis Setup

**Local (easiest for development):**
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Or use Docker
docker run -d -p 6379:6379 redis:latest
```

**Cloud (for production):**
- Use Redis Cloud (free tier available)
- Update REDIS_URL in backend/.env

## Environment Variables

### Frontend (.env.local)

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### Backend (.env)

```
ANTHROPIC_API_KEY=sk-ant-...
DAILY_API_KEY=...
DEEPGRAM_API_KEY=...
ELEVENLABS_API_KEY=...
REDIS_URL=redis://localhost:6379
WEAVE_PROJECT=interview-prep-agent
```

## Running the App

1. Start Redis (if running locally)
2. Start backend: `cd backend && python main.py`
3. Start frontend: `cd frontend && npm run dev`
4. Open http://localhost:3000

## Demo Flow

1. Click "Start Interview Session"
2. Allow microphone access
3. Voice bot asks you questions
4. Answer naturally (speak out loud)
5. Bot evaluates your answer in real-time
6. After session, view dashboard showing improvement

## Key Features for Judges

### Self-Improving Mechanism

The agent learns your weak areas through:

1. **Initial Assessment**: Asks questions across multiple topics
2. **Scoring**: Claude evaluates each answer (0-10 scale)
3. **Knowledge Mapping**: Tracks scores per topic area
4. **Adaptive Questioning**: Focuses on low-scoring areas
5. **Progressive Difficulty**: Increases difficulty as you improve

### Observability with Weave

Every Claude API call is logged:
- Question generation prompts
- Answer evaluation logic
- Scoring decisions
- Token usage and latency

View traces at: https://wandb.ai/weave

### Tech Highlights

- **Pipecat**: Seamless voice conversation flow
- **Daily**: Production-ready voice infrastructure
- **Redis**: Fast session storage and caching
- **Weave**: Complete LLM observability (2 lines of code!)

## Deployment

### Frontend (Vercel)

```bash
cd frontend
vercel
# Follow prompts, add environment variables
```

### Backend (Options)

**Option 1: Render/Railway**
- Connect GitHub repo
- Set environment variables
- Auto-deploys

**Option 2: Google Cloud Run**
- Containerize with provided Dockerfile
- Deploy to Cloud Run

**Option 3: ngrok (for demo)**
```bash
cd backend
python main.py
# In another terminal:
ngrok http 8000
# Use ngrok URL as NEXT_PUBLIC_BACKEND_URL
```

## Development Notes

### Adding New Question Topics

Edit `backend/question_bank.py`:

```python
QUESTIONS = {
    "new_topic": [
        "Question 1",
        "Question 2",
        # Add more questions
    ]
}
```

### Adjusting Scoring Logic

Edit `backend/evaluator.py`:

```python
def evaluate_answer(question, answer, topic):
    # Customize Claude prompt for evaluation
    # Adjust scoring criteria
    pass
```

### Customizing UI

Edit components in `frontend/components/`:
- `RadarChart.tsx` - Knowledge visualization
- `SessionView.tsx` - Interview interface
- `Dashboard.tsx` - Progress tracking

## Troubleshooting

**Voice not working?**
- Check microphone permissions in browser
- Verify Daily API key is correct
- Check browser console for WebRTC errors

**Backend crashes?**
- Ensure all API keys are set
- Check Redis is running
- Verify Python dependencies installed

**Session not saving?**
- Check Redis connection
- Verify REDIS_URL environment variable
- Check backend logs for errors

## Credits

Built for WeaveHacks 2025 by Melon

## License

MIT
