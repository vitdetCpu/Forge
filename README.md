<p align="center">
  <img src="https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Claude-AI-purple?style=for-the-badge&logo=anthropic" />
  <img src="https://img.shields.io/badge/Voice-Enabled-green?style=for-the-badge&logo=microphone" />
</p>

# 🔥 Forge

**AI-powered voice interview coach that learns and adapts to you.**

Forge is an intelligent mock interviewer that uses real-time voice conversations to identify your weaknesses and progressively focuses practice where you need it most. Every session makes you sharper.

> 🏆 Built for CoreWeave's Weights & Biases / WeaveHacks 2026

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎤 **Voice Conversations** | Natural back-and-forth interviews using WebRTC—no typing required |
| 🧠 **Adaptive Learning** | AI identifies your weak areas and dynamically adjusts question difficulty |
| 📊 **Progress Tracking** | Radar charts and improvement graphs to visualize your growth |
| ⚡ **Real-Time Feedback** | Instant scoring and constructive feedback after each answer |
| 🔍 **Full Observability** | Every AI decision logged with Weave for complete transparency |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                  FRONTEND                                   │
│                             (Next.js 14 + React)                            │
│  ┌─────────────┐  ┌─────────────────────┐  ┌────────────────────────────┐   │
│  │   Landing   │  │  Voice Session UI   │  │   Progress Dashboard     │   │
│  │    Page     │  │  (Daily WebRTC)     │  │   (Radar + Line Charts)  │   │
│  └─────────────┘  └─────────────────────┘  └────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ REST API + WebRTC
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                  BACKEND                                    │
│                           (Python + FastAPI)                                │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        PIPECAT VOICE PIPELINE                        │   │
│  │  ┌────────────┐    ┌─────────────┐    ┌────────────┐    ┌─────────┐  │   │
│  │  │   Daily    │───▶│  Deepgram   │───▶│  Interview │───▶│ Deepgram│  │   │
│  │  │ Transport  │    │    STT      │    │ Bot Logic  │    │   TTS   │  │   │
│  │  │  (WebRTC)  │◀───│ (nova-2)    │◀───│            │◀───│         │  │   │
│  │  └────────────┘    └─────────────┘    └─────┬──────┘    └─────────┘  │   │
│  └─────────────────────────────────────────────┼────────────────────────┘   │
│                                                │                            │
│  ┌─────────────────────┐    ┌─────────────────┴────────────────────────┐   │
│  │   Session Storage   │◀──▶│           Claude Evaluator               │   │
│  │      (Redis)        │    │  • Answer scoring (0-10)                 │   │
│  │                     │    │  • Weakness identification               │   │
│  │  • Knowledge maps   │    │  • Adaptive question generation          │   │
│  │  • Session history  │    │  • Topic selection based on weak areas   │   │
│  │  • Score tracking   │    └──────────────────────────────────────────┘   │
│  └─────────────────────┘                       │                            │
│                                                ▼                            │
│                               ┌───────────────────────────┐                 │
│                               │   Weave Observability     │                 │
│                               │   (W&B LLM Tracing)       │                 │
│                               └───────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 How the AI Learns

Forge uses a **self-improving feedback loop** to personalize your practice:

```
   ┌─────────────────────────────────────────────────────────┐
   │                                                         │
   ▼                                                         │
┌──────────┐     ┌──────────┐     ┌───────────┐     ┌───────┴───────┐
│  1. ASK  │────▶│ 2. LISTEN│────▶│ 3. SCORE  │────▶│ 4. ADAPT      │
│ Question │     │ & Record │     │ with Claude│     │ Next Question │
└──────────┘     └──────────┘     └───────────┘     └───────────────┘
                                        │
                                        ▼
                                ┌──────────────────┐
                                │  Knowledge Map   │
                                │  ─────────────   │
                                │  Leadership: 72% │
                                │  Algorithms: 45% │◀── Focus Here!
                                │  System Design: 68%│
                                │  Communication: 81%│
                                └──────────────────┘
```

1. **Initial Assessment** — Asks questions across multiple categories
2. **Real-Time Scoring** — Claude evaluates each answer (0-10) based on STAR method, specificity, and clarity
3. **Knowledge Mapping** — Tracks your performance per topic over time
4. **Adaptive Questioning** — Prioritizes your weakest areas with progressive difficulty

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js 14, React, TailwindCSS | Modern web UI with App Router |
| **Voice Transport** | Daily (WebRTC) | Production-grade real-time audio |
| **Voice Pipeline** | Pipecat | Orchestrates STT → Bot → TTS flow |
| **Speech-to-Text** | Deepgram Nova-2 | Fast, accurate transcription |
| **Text-to-Speech** | Deepgram Aura | Natural-sounding voice responses |
| **AI Evaluation** | Claude (Anthropic) | Answer scoring & question generation |
| **Storage** | Redis | Session state & knowledge maps |
| **Observability** | Weave (W&B) | LLM call tracing & debugging |

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- Redis (local or cloud)
- API Keys: Anthropic, Daily, Deepgram

### 1. Clone & Setup

```bash
git clone https://github.com/vitdetCpu/Forge.git
cd Forge

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys from the email/dashboard

# Frontend
cd ../frontend
npm install
cp .env.example .env.local
```

### 2. Configure Environment

**Backend `.env`:**
```env
ANTHROPIC_API_KEY=sk-ant-...
DAILY_API_KEY=...
DEEPGRAM_API_KEY=...
REDIS_URL=redis://localhost:6379
WEAVE_PROJECT=forge
```

**Frontend `.env.local`:**
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 3. Run

```bash
# Terminal 1: Backend (using the helper script)
cd backend
./run.sh

# Terminal 2: Frontend
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and start practicing! 🎤

---

## 📁 Project Structure

```
forge/
├── frontend/                 # Next.js 14 web application
│   ├── app/                  # App Router pages
│   │   ├── page.tsx          # Landing page
│   │   ├── session/          # Voice interview UI
│   │   └── dashboard/        # Progress visualization
│   ├── components/           # React components
│   │   ├── RadarChart.tsx    # Knowledge visualization
│   │   └── ProgressChart.tsx # Improvement tracking
│   └── lib/api.ts            # Backend API client
│
├── backend/                  # Python FastAPI server
│   ├── main.py               # API endpoints
│   ├── pipecat_bot.py        # Voice pipeline & interview logic
│   ├── evaluator.py          # Claude integration + Weave tracing
│   ├── storage.py            # Redis operations
│   └── question_bank.py      # Question templates
│
└── README.md
```

---

## 🎯 Demo Flow

1. **Click "Start Interview Session"** on the landing page
2. **Allow microphone access** when prompted
3. **Listen** — The AI interviewer introduces itself and asks the first question
4. **Speak naturally** — Answer out loud like a real interview
5. **Get instant feedback** — Bot evaluates and moves to the next question
6. **View your dashboard** — See scores per topic and track improvement over time

---

## 🔮 Future Roadmap

- [ ] **Interview types** — Technical, behavioral, case study modes
- [ ] **Resume analysis** — Personalized questions based on your experience
- [ ] **Video recording** — Review body language and delivery
- [ ] **Peer comparison** — Anonymous benchmarking against other users
- [ ] **Custom question banks** — Upload your target company's style

---

## 👨‍💻 Authors

Built with ☕ and ❤️ by **Vidit and Nathan**

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
