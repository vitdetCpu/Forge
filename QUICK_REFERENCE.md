# Forge - Quick Reference Card

## Commands to Remember

### Start Everything
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py

# Terminal 2 - Frontend  
cd frontend
npm run dev

# Terminal 3 - Redis (if needed)
redis-server
```

### URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Weave Dashboard: https://wandb.ai/weave

### Generate Demo Data
```bash
cd backend
source venv/bin/activate
python generate_demo_data.py
```

### Check if Redis is Running
```bash
redis-cli ping
# Should return: PONG
```

### View Redis Data
```bash
redis-cli
> KEYS *
> GET session:sess_abc123
```

## API Keys You Need

- ANTHROPIC_API_KEY (required)
- DAILY_API_KEY (optional, for voice)
- DEEPGRAM_API_KEY (optional, for voice)
- ELEVENLABS_API_KEY (optional, for voice)
- REDIS_URL (default: redis://localhost:6379)
- WEAVE_PROJECT (default: forge)

## File Structure

```
interview-prep-agent/
├── frontend/           # Next.js app
│   ├── app/           # Pages
│   │   ├── page.tsx           # Home
│   │   ├── session/page.tsx   # Interview session
│   │   └── dashboard/page.tsx # Progress dashboard
│   ├── components/    # React components
│   └── lib/api.ts     # API client
│
└── backend/           # Python API
    ├── main.py        # FastAPI server
    ├── bot.py         # Pipecat voice bot
    ├── evaluator.py   # Claude + Weave
    ├── storage.py     # Redis operations
    └── question_bank.py # Interview questions
```

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.10+)
- Activate venv: `source venv/bin/activate`
- Install deps: `pip install -r requirements.txt`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Install deps: `npm install`
- Clear cache: `rm -rf .next`

### Redis connection error
- Start Redis: `redis-server` or `brew services start redis`
- Check if running: `redis-cli ping`

### Voice not working
- Check API keys in backend/.env
- For demo, you can skip voice and just show the dashboard

### No data showing
- Run: `python generate_demo_data.py`
- Check Redis: `redis-cli KEYS *`

## Demo Checklist

- [ ] Redis running (`redis-cli ping` works)
- [ ] Backend running (visit http://localhost:8000)
- [ ] Frontend running (visit http://localhost:3000)
- [ ] Demo data exists (check dashboard)
- [ ] Weave dashboard accessible
- [ ] Rehearsed pitch
- [ ] Backup plan ready

## Key Metrics to Show

1. **Sessions completed**: 5
2. **Questions answered**: 15
3. **Average improvement**: +36%
4. **Biggest improvement**: Algorithms (3.5 → 8.5 = +142%)
5. **Response rate**: Weave shows evaluation improving

## Sponsor Integrations

✅ Daily/Pipecat - Voice infrastructure
✅ Weave (W&B) - LLM observability  
✅ Redis - Fast storage
✅ Vercel - Frontend hosting
✅ Claude API - Evaluation

## Emergency Contacts

- Anthropic API issues: Check status.anthropic.com
- Daily issues: docs.daily.co
- Redis issues: redis.io/docs
- Weave issues: wandb.ai/site/weave

