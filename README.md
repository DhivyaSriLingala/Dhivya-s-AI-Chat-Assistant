# 🤖 Dhivya AI Agent — Wikipedia RAG Chatbot

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Qwen3--32B-F55036?style=flat)
![Wikipedia](https://img.shields.io/badge/Wikipedia-Free%20API-000000?style=flat&logo=wikipedia)
![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=flat&logo=vercel)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> A full-stack **Retrieval-Augmented Generation (RAG)** AI agent that answers questions about **Dhivya Sri Lingala** by intelligently searching a personal knowledge base and Wikipedia — powered entirely by **free APIs**.

---

## 🚀 Live Demo

### 👉 Try it live → [dhivya-s-ai-chat-assistant.vercel.app](https://dhivya-s-ai-chat-assistant.vercel.app)

** Have a look at the portfolio because the Chat Assistant or the Personal Q&A AI there got this AI agent integrated in it. [dhivya-sri-lingala.vercel.app](https://dhivya-sri-lingala.vercel.app/)*

**Sample questions to ask:**
- *"Who is Dhivya Sri Lingala?"*
- *"What is she currently researching at UF?"*
- *"Tell me about her projects."*
- *"What is RAG and does she use it in her work?"*
- *"What are her technical skills?"*

---

## 👩‍💻 About Dhivya

**Dhivya Sri Lingala** is an MS Artificial Intelligence Systems student at the **University of Florida** (GPA: 3.85) and a Graduate Research Assistant at the **CATIA Lab**, building agentic AI systems at scale.

| | |
|---|---|
| 🌐 Portfolio | [dhivya-sri-lingala.vercel.app](https://dhivya-sri-lingala.vercel.app/) |
| 💼 LinkedIn | [linkedin.com/in/dhivya-sri-lingala](https://www.linkedin.com/in/dhivya-sri-lingala/) |
| 🐙 GitHub | [github.com/DhivyaSriLingala](https://github.com/DhivyaSriLingala) |
| 📧 Email | lingaladhivyasri24@gmail.com |

---

## 🔁 Build Your Own Version

Want to build a personalised AI agent for **your own resume**? Fork this repo and swap in your profile — it takes less than 10 minutes.

### Step 1 — Fork the repo

Click **Fork** at the top right of this page.

### Step 2 — Replace the knowledge base

Edit `backend/data/dhivya_profile.md` with your own information — name, education, skills, projects, experience. The file is plain Markdown, no special format required.

```markdown
# Your Name — Personal Profile

## Identity & Overview
- Full Name: ...
- Current Role: ...

## Education
...

## Technical Skills
...

## Projects
...
```

### Step 3 — Update the agent's name

In `backend/agent.py`, change the system prompt to reference your name:

```python
SYSTEM_PROMPT = """\
You are an AI assistant specialized in answering questions about [YOUR NAME].
...
"""
```

### Step 4 — Get a free Groq API key

Sign up at [console.groq.com](https://console.groq.com) — free, no credit card needed.

### Step 5 — Deploy

**Backend → [Render.com](https://render.com)** (free tier)
- Connect your forked repo
- Root directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Add env var: `GROQ_API_KEY=gsk_...`

**Frontend → [Vercel.com](https://vercel.com)** (free tier)
- Connect your forked repo
- Root directory: `frontend`
- Add env var: `VITE_API_URL=https://your-render-app.onrender.com`

That's it — your personalised AI agent is live. 🎉

---

## Table of Contents

1. [What This App Does](#1-what-this-app-does)
2. [Theory — RAG, LLMs, and Agentic AI](#2-theory--rag-llms-and-agentic-ai)
3. [System Architecture](#3-system-architecture)
4. [Tech Stack](#4-tech-stack)
5. [Project Structure](#5-project-structure)
6. [How the Agent Loop Works](#6-how-the-agent-loop-works)
7. [The Knowledge Base & Retrieval](#7-the-knowledge-base--retrieval)
8. [Run Locally](#8-run-locally)
9. [Deploy to Production](#9-deploy-to-production)
10. [API Reference](#10-api-reference)
11. [Design Decisions](#11-design-decisions)

---

## 1. What This App Does

This application is an **intelligent question-answering chatbot** that answers questions about Dhivya Sri Lingala — her education, work experience, projects, and technical skills — with accuracy guaranteed by grounding every response in verified sources.

**Key capabilities:**
- Answers personal/professional questions using a curated knowledge base built from a real resume and portfolio
- Augments answers with Wikipedia for background context (e.g. explaining a technology she uses)
- Shows which sources were searched for every response (transparent RAG)
- Multi-turn conversation — remembers what was said earlier in the chat
- 100% free to run — uses the free Groq API and the free Wikipedia API

---

## 2. Theory — RAG, LLMs, and Agentic AI

### 2.1 The Problem with Pure LLMs

Large Language Models (LLMs) like GPT-4, Claude, or Llama are trained on massive text datasets. They are excellent at language understanding and generation, but they have two critical limitations:

| Problem | Description |
|---|---|
| **Knowledge cutoff** | Training data has a cutoff date; the model knows nothing after that |
| **Hallucination** | LLMs can confidently generate false facts when they don't know the answer |

For a chatbot about a specific person like Dhivya Sri Lingala, a plain LLM would either say "I don't know" or invent details — neither is acceptable.

### 2.2 Retrieval-Augmented Generation (RAG)

**RAG** solves both problems by combining a retrieval system with a language model:

```
                 ┌──────────────────────────────────┐
                 │         RAG Pipeline              │
                 │                                  │
  User Query ──► │  1. RETRIEVE relevant documents  │
                 │         ↓                        │
                 │  2. AUGMENT the LLM prompt       │
                 │     with retrieved context       │
                 │         ↓                        │
                 │  3. GENERATE grounded answer     │ ──► Response
                 └──────────────────────────────────┘
```

Instead of asking the LLM "Who is Dhivya Sri Lingala?", RAG:
1. **Retrieves** relevant sections from the knowledge base (e.g. education, experience)
2. **Augments** the prompt: *"Using this context: [retrieved text], answer: Who is Dhivya?"*
3. **Generates** an answer grounded in the retrieved facts — not hallucinated

### 2.3 Agentic AI and Tool Use

A **basic RAG** system always retrieves before answering. An **agentic RAG** system is smarter — the LLM itself decides *whether* to retrieve, *what* to search for, and *which source* to use.

```
LLM receives question
        │
        ▼
  "Do I need more info?"
   /              \
 YES               NO
  │                │
  ▼                ▼
Call a tool    Answer directly
  │
  ▼
search_knowledge_base  OR  search_wikipedia
  │
  ▼
Receive result → generate grounded answer
```

### 2.4 BM25 — How the Knowledge Base Search Works

This app uses **BM25** (Best Match 25), a classical information retrieval algorithm, to search the knowledge base. BM25 scores each document chunk by:

1. **Term frequency** — how often query words appear in the chunk
2. **Inverse document frequency** — rare words score higher than common ones
3. **Document length normalisation** — shorter chunks aren't unfairly penalised

BM25 is fast, requires no GPU, needs no embedding model, and works well for small structured knowledge bases — making it perfect for a free, local RAG system.

### 2.5 Why Not Vector Embeddings?

Vector-embedding RAG (e.g. OpenAI embeddings + Pinecone) is powerful for large document sets but has costs — paid embedding APIs, vector databases, and GPU latency. For a personal profile with ~26 structured sections, BM25 keyword search is equally effective and entirely free.

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                           │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              React + Vite  (Vercel)                     │  │
│   │  Header · ChatWindow · MessageBubbles · InputBar        │  │
│   │  Shows search badges: which source was queried          │  │
│   └────────────────────────┬────────────────────────────────┘  │
│                            │ POST /api/chat (VITE_API_URL)      │
└────────────────────────────┼────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│               FastAPI Backend  (Render.com)                     │
│                                                                 │
│   main.py ──► agent.py (RAG Agent Loop)                        │
│                    │                                            │
│          ┌─────────┴──────────┐                                │
│          ▼                    ▼                                 │
│   search_knowledge_base   search_wikipedia                     │
│          │                    │                                 │
│   dhivya_profile.md    Wikipedia Python API                    │
│   (BM25, 26 chunks)    (free, no key needed)                   │
│          └─────────┬──────────┘                                │
│                    ▼                                            │
│           Groq API — Qwen3-32B (free tier)                     │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Loop

```
User message
     │
     ▼
Groq API call (with tools available)
     │
     ├── tool_calls? ──YES──► Execute tool(s) ──► append result ──┐
     │                                                             │
     └── no tool_calls? ──► Final answer                          │
                ▲                                                  │
                └──────────────────────────────────────────────────┘
```

---

## 4. Tech Stack

| Layer | Technology | Cost |
|---|---|---|
| LLM | Groq API — Qwen3-32B | Free (30K tokens/min) |
| Knowledge Search | BM25 (custom Python) | Free |
| Web Search | Wikipedia Python library | Free |
| Backend | FastAPI + Uvicorn | Open source |
| Backend Host | Render.com | Free tier |
| Frontend | React 18 + Vite | Open source |
| Frontend Host | Vercel | Free tier |
| Markdown render | react-markdown | Open source |

**Total running cost: $0.00**

---

## 5. Project Structure

```
Wikipedia_AI_agent/
│
├── backend/                        # Python FastAPI server (deployed on Render)
│   ├── main.py                     # FastAPI app, CORS, /api/chat endpoint
│   ├── agent.py                    # Groq agent loop with tool use
│   ├── rag/
│   │   ├── knowledge_base.py       # BM25 search over dhivya_profile.md
│   │   └── wikipedia_search.py     # Wikipedia API wrapper
│   ├── data/
│   │   └── dhivya_profile.md       # ← Personal knowledge base (edit to customise)
│   ├── requirements.txt
│   └── .python-version             # Pins Python 3.11 for Render
│
├── frontend/                       # React + Vite chat UI (deployed on Vercel)
│   ├── src/
│   │   ├── App.jsx                 # Root component, chat state, API calls
│   │   ├── index.css               # Full UI styles
│   │   └── components/
│   │       ├── ChatWindow.jsx      # Scrollable message list
│   │       ├── Message.jsx         # Message bubble + search badges
│   │       └── InputBar.jsx        # Text input + send button
│   ├── package.json
│   └── vite.config.js              # Dev proxy → backend; VITE_API_URL in prod
│
├── render.yaml                     # Render one-click deploy config
├── vercel.json                     # Vercel build config
├── .env.example                    # Template — copy to backend/.env locally
└── README.md
```

---

## 6. How the Agent Loop Works

```python
# Simplified pseudocode — see backend/agent.py for full implementation
def run_agent(messages):
    chat = [system_prompt] + messages

    for _ in range(max_iterations):
        response = groq.chat(chat, tools=[search_kb, search_wikipedia])

        if response.has_tool_calls:
            for call in response.tool_calls:
                result = execute(call.name, call.args)
                chat.append(tool_result(result))
        else:
            return response.text   # grounded final answer
```

**Example — "What is Dhivya's GPA?"**
```
→ Agent calls: search_knowledge_base("Dhivya GPA education")
← KB returns:  "MS at UF: CGPA 3.85 | BTech at KLU: CGPA 3.98"
→ Agent generates: "Dhivya has a 3.85 GPA in her MS at UF and 3.98 from KL University."
```

**Example — "What is RAG and does Dhivya use it?"**
```
→ Agent calls: search_wikipedia("Retrieval-Augmented Generation")
← Wikipedia returns: definition and background
→ Agent calls: search_knowledge_base("Dhivya RAG pipelines")
← KB returns:  CATIA Lab project, LinguaEval, this project
→ Agent generates: combined answer from both sources
```

---

## 7. The Knowledge Base & Retrieval

The knowledge base is `backend/data/dhivya_profile.md` — plain Markdown split into 26 sections covering education, skills, all work experience, all projects, and personal interests.

**BM25 scoring example:**
```
Query: "What university does Dhivya attend?"
Keywords: {university, dhivya, attend}

Education section  → overlap: {university} → score: 0.33  ✓ returned
Projects section   → overlap: {}           → score: 0.00  ✗ skipped
```

Top-4 scoring chunks are passed to the LLM as context. No embeddings, no vector DB, no GPU.

---

## 8. Run Locally

### Prerequisites
- Python 3.11+ and Node.js 18+
- Free [Groq API key](https://console.groq.com)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create .env from template
cp ../.env.example .env
# Edit .env → GROQ_API_KEY=gsk_...

python test_key.py              # Verify key works
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**

### Environment variables

| Variable | Where | Description |
|---|---|---|
| `GROQ_API_KEY` | `backend/.env` | Groq LLM key — [get one free](https://console.groq.com) |
| `VITE_API_URL` | Vercel dashboard | Render backend URL (production only) |

---

## 9. Deploy to Production

The backend runs on **Render** (free Python hosting) and the frontend on **Vercel** (free static hosting). Deploy the backend first — you need its URL before configuring the frontend.

---

### Part A — Backend on Render

#### Prerequisites
- A [Render account](https://render.com) — sign up free with GitHub
- Your Groq API key (`gsk_...`) from [console.groq.com](https://console.groq.com)
- This repo pushed to GitHub

#### Step 1 — Connect your GitHub repo

1. Log in to [render.com](https://render.com)
2. Click **New +** → **Web Service**
3. Under "Connect a repository", click **Connect GitHub**
4. Authorise Render and select **`Dhivya-s-AI-Chat-Assistant`**

> If you don't see the repo: go to **GitHub → Settings → Applications → Render → Configure** and grant access to the repo.

#### Step 2 — Configure the service

Fill in the following fields (Render may auto-detect some from `render.yaml`):

| Field | Value |
|---|---|
| **Name** | `dhivya-ai-agent-backend` (or any name) |
| **Region** | Oregon (US West) or closest to you |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | **Free** |

#### Step 3 — Add the API key

1. Scroll down to **Environment Variables**
2. Click **Add Environment Variable**
3. Add:

   | Key | Value |
   |---|---|
   | `GROQ_API_KEY` | `gsk_your_key_here` |
   | `PYTHON_VERSION` | `3.11.9` |

#### Step 4 — Deploy

Click **Create Web Service**. Render will:
1. Clone your repo
2. Run `pip install -r requirements.txt`
3. Start the FastAPI server

Build takes ~2–3 minutes. When you see **"Your service is live"**, copy the URL — it looks like:
```
https://dhivya-ai-agent-backend.onrender.com
```
You'll need this for the Vercel setup.

#### Step 5 — Verify the backend is running

Open in your browser:
```
https://dhivya-ai-agent-backend.onrender.com/api/health
```
You should see:
```json
{ "status": "ok", "model": "qwen/qwen3-32b" }
```

> **Note:** Render's free tier spins down after 15 minutes of inactivity. The first request after sleep takes ~30 seconds to wake up — this is normal. Paid tiers stay always-on.

---

### Part B — Frontend on Vercel

#### Prerequisites
- A [Vercel account](https://vercel.com) — sign up free with GitHub

#### Step 1 — Import the project

1. Log in to [vercel.com](https://vercel.com)
2. Click **Add New… → Project**
3. Find **`Dhivya-s-AI-Chat-Assistant`** and click **Import**

#### Step 2 — Configure the project

On the configuration screen, change these settings:

| Setting | Value |
|---|---|
| **Root Directory** | `frontend` ← click Edit and type this |
| **Framework Preset** | Vite (auto-detected once root is set) |
| **Build Command** | `npm run build` (leave as default) |
| **Output Directory** | `dist` (leave as default) |

> ⚠️ Setting **Root Directory to `frontend`** is critical. Without it, Vercel looks for `package.json` in the repo root and fails.

#### Step 3 — Add the environment variable

Still on the configuration screen, expand **Environment Variables** and add:

| Name | Value |
|---|---|
| `VITE_API_URL` | `https://dhivya-ai-agent-backend.onrender.com` |

Replace the URL with your actual Render backend URL from Part A Step 4.

#### Step 4 — Deploy

Click **Deploy**. Vercel will:
1. Install npm dependencies
2. Run `npm run build` (Vite bundles the React app)
3. Serve the `dist/` folder on a global CDN

Build takes ~1 minute. Your app is live at a URL like:
```
https://dhivya-s-ai-chat-assistant.vercel.app
```

#### Step 5 — Verify end-to-end

Open the Vercel URL and ask: *"Who is Dhivya Sri Lingala?"*

The chat should respond with a sourced answer, showing a **📋 Searched personal profile** badge. If you see a network error, check:
- The `VITE_API_URL` is set correctly (no trailing slash)
- The Render backend is awake (open `/api/health` directly first)

---

### Redeploying after changes

| Change | What to do |
|---|---|
| Edit `dhivya_profile.md` | Push to GitHub → Render auto-redeploys backend |
| Edit any frontend file | Push to GitHub → Vercel auto-redeploys frontend |
| Change `GROQ_API_KEY` | Render dashboard → Environment → update value → Manual Deploy |
| Change `VITE_API_URL` | Vercel dashboard → Settings → Environment Variables → update → Redeploy |

---

## 10. API Reference


### `POST /api/chat`

```json
// Request
{
  "messages": [
    { "role": "user", "content": "What is Dhivya's GPA?" }
  ]
}

// Response
{
  "response": "Dhivya has a CGPA of 3.85/4.0 in her Master's at University of Florida...",
  "search_actions": [
    { "tool": "search_knowledge_base", "query": "Dhivya GPA education" }
  ]
}
```

Multi-turn: pass the full conversation history in `messages` — the agent maintains context across turns.

### `GET /api/health`
```json
{ "status": "ok", "model": "qwen/qwen3-32b" }
```

---

## 11. Design Decisions

| Decision | Why |
|---|---|
| BM25 over vector embeddings | No embedding API cost, no vector DB, works perfectly for <30 structured sections |
| Groq over OpenAI/Anthropic | Generous free tier (30K tokens/min), no credit card, fastest inference |
| Qwen3-32B model | Best tool-use reliability on Groq's current free model lineup |
| Markdown knowledge base | Human-editable, version-controlled, zero migration cost to update |
| FastAPI + React | Fast async Python API + reactive chat UI; both widely understood |
| Render for backend | Free Python hosting, zero config for FastAPI, auto-deploys from GitHub |
| Vercel for frontend | Free static hosting, instant CDN, integrates with existing portfolio |
| Tool use over naive RAG | Agent decides what to search — avoids irrelevant retrievals, saves tokens |
| `allow_origins=["*"]` on CORS | Vercel preview URLs are dynamic; restrict to fixed domain after launch |

---

## About the Author

**Dhivya Sri Lingala** — MS Artificial Intelligence Systems @ University of Florida

Graduate Research Assistant building agentic AI systems at the CATIA Lab. Experienced in LLM development, RAG pipelines, full-stack AI applications, and production ML systems.

| | |
|---|---|
| 🌐 Portfolio | [dhivya-sri-lingala.vercel.app](https://dhivya-sri-lingala.vercel.app/) |
| 💼 LinkedIn | [linkedin.com/in/dhivya-sri-lingala](https://www.linkedin.com/in/dhivya-sri-lingala/) |
| 🐙 GitHub | [github.com/DhivyaSriLingala](https://github.com/DhivyaSriLingala) |

---

*Built with FastAPI · React · Groq · Wikipedia API · Deployed on Vercel + Render*
