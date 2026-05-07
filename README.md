# 🤖 Dhivya AI Agent — Wikipedia RAG Chatbot

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA%20%2F%20Qwen3-F55036?style=flat)
![Wikipedia](https://img.shields.io/badge/Wikipedia-Free%20API-000000?style=flat&logo=wikipedia)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> A full-stack **Retrieval-Augmented Generation (RAG)** AI agent that answers questions about **Dhivya Sri Lingala** by intelligently searching a personal knowledge base and Wikipedia — powered entirely by **free APIs**.

**Live Demo**: [dhivya-sri-lingala.vercel.app](https://dhivya-sri-lingala.vercel.app/) &nbsp;|&nbsp; **Portfolio**: [dhivya-sri-lingala.vercel.app](https://dhivya-sri-lingala.vercel.app/)

---

## Table of Contents

1. [What This App Does](#1-what-this-app-does)
2. [Theory — RAG, LLMs, and Agentic AI](#2-theory--rag-llms-and-agentic-ai)
3. [System Architecture](#3-system-architecture)
4. [Tech Stack](#4-tech-stack)
5. [Project Structure](#5-project-structure)
6. [How the Agent Loop Works](#6-how-the-agent-loop-works)
7. [The Knowledge Base & Retrieval](#7-the-knowledge-base--retrieval)
8. [Setup & Running Locally](#8-setup--running-locally)
9. [API Reference](#9-api-reference)
10. [Sample Questions to Try](#10-sample-questions-to-try)
11. [Customising the Knowledge Base](#11-customising-the-knowledge-base)
12. [Design Decisions](#12-design-decisions)

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
1. **Retrieves** relevant sections from the knowledge base (e.g., education, experience)
2. **Augments** the prompt: *"Using this context: [retrieved text], answer: Who is Dhivya?"*
3. **Generates** an answer grounded in the retrieved facts — not hallucinated

**Why this matters:** The LLM can only say what the retrieved documents say. It becomes a language *formatter* rather than a *fact inventor*.

### 2.3 Agentic AI and Tool Use

A **basic RAG** system always retrieves before answering. An **agentic RAG** system is smarter — the LLM itself decides *whether* to retrieve, *what* to search for, and *which source* to use.

This is called **tool use** (also known as function calling):

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
(search KB or
 Wikipedia)
        │
        ▼
  Receive tool result
        │
        ▼
  "Do I have enough now?"
   /              \
 YES               NO
  │                │
  ▼                ▼
Answer        Call another tool
```

The LLM in this app is given two tools:
- `search_knowledge_base` — searches the personal profile
- `search_wikipedia` — searches Wikipedia

It decides autonomously which to call, with what query, and when to stop searching and generate the final answer. This is the essence of an **AI agent**.

### 2.4 BM25 — How the Knowledge Base Search Works

This app uses **BM25** (Best Match 25), a classical information retrieval algorithm, to search the knowledge base. BM25 scores each document chunk by:

1. **Term frequency** — how often query words appear in the chunk
2. **Inverse document frequency** — rare words score higher than common ones
3. **Document length normalisation** — shorter chunks aren't unfairly penalised

BM25 is fast, requires no GPU, needs no embedding model, and works well for small structured knowledge bases — making it perfect for a free, local RAG system.

### 2.5 Why Not Vector Embeddings?

Vector-embedding-based RAG (e.g. using OpenAI embeddings + Pinecone) is powerful for large document sets but has costs:
- Requires an embedding API (paid) or a local model (needs GPU)
- Requires a vector database
- Adds latency and complexity

For a personal profile with ~26 structured sections, BM25 keyword search is equally effective and entirely free. This is a deliberate design choice for accessibility.

---

## 3. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                           │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              React + Vite Frontend                      │  │
│   │                                                         │  │
│   │   ┌──────────┐  ┌───────────────┐  ┌────────────────┐  │  │
│   │   │  Header  │  │  Chat Window  │  │  Input Bar     │  │  │
│   │   └──────────┘  │               │  └────────────────┘  │  │
│   │                 │  ┌──────────┐ │                       │  │
│   │                 │  │ Message  │ │  Shows:               │  │
│   │                 │  │ Bubbles  │ │  • User messages      │  │
│   │                 │  └──────────┘ │  • AI responses       │  │
│   │                 │  ┌──────────┐ │  • Search badges      │  │
│   │                 │  │ Typing   │ │    (which source)     │  │
│   │                 │  │Indicator │ │                       │  │
│   │                 │  └──────────┘ │                       │  │
│   │                 └───────────────┘                       │  │
│   └────────────────────────┬────────────────────────────────┘  │
│                            │ POST /api/chat                     │
└────────────────────────────┼────────────────────────────────────┘
                             │ (Vite proxy → localhost:8000)
┌────────────────────────────▼────────────────────────────────────┐
│                     FastAPI Backend                             │
│                                                                 │
│   main.py ──► agent.py (RAG Agent Loop)                        │
│                    │                                            │
│          ┌─────────┴──────────┐                                │
│          ▼                    ▼                                 │
│   search_knowledge_base   search_wikipedia                     │
│          │                    │                                 │
│          ▼                    ▼                                 │
│   ┌─────────────┐    ┌────────────────┐                        │
│   │ dhivya_     │    │ Wikipedia      │                        │
│   │ profile.md  │    │ Python API     │                        │
│   │ (26 chunks) │    │ (free, no key) │                        │
│   └─────────────┘    └────────────────┘                        │
│          │                    │                                 │
│          └─────────┬──────────┘                                │
│                    ▼                                            │
│           ┌────────────────┐                                    │
│           │  Groq API      │                                    │
│           │  Qwen3-32B     │                                    │
│           │  (free tier)   │                                    │
│           └────────────────┘                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Loop (Detailed)

```
POST /api/chat  { messages: [...] }
        │
        ▼
  run_agent(messages)
        │
        ▼
  Build chat history + system prompt
        │
        ▼
  ┌─────────────────────────────────┐
  │        GROQ API CALL            │  ◄─────────────────────┐
  │   model: qwen3-32b              │                        │
  │   tools: [search_kb, search_wp] │                        │
  └──────────────┬──────────────────┘                        │
                 │                                           │
         ┌───────┴────────┐                                  │
         ▼                ▼                                  │
   tool_calls?        stop_reason=end                        │
         │                │                                  │
         ▼                ▼                                  │
   Execute tool    Return final text                         │
   append result        │                                    │
   to messages     { response,                               │
         │           search_actions }                        │
         └────────────────────────────────────────────────── ┘
```

---

## 4. Tech Stack

| Layer | Technology | Purpose | Cost |
|---|---|---|---|
| **LLM** | Groq API — Qwen3-32B | Language model, tool use decisions | Free (30K tokens/min) |
| **Knowledge Search** | BM25 (custom implementation) | Search personal profile chunks | Free |
| **Web Search** | Wikipedia Python library | Encyclopedic context | Free |
| **Backend** | FastAPI + Uvicorn | REST API server | Free / Open source |
| **Frontend** | React 18 + Vite | Chat UI | Free / Open source |
| **Markdown** | react-markdown + remark-gfm | Render formatted responses | Free / Open source |
| **Env Config** | python-dotenv | Load API keys from `.env` | Free / Open source |

**Total running cost: $0.00**

---

## 5. Project Structure

```
Wikipedia_AI_agent/
│
├── backend/                        # Python FastAPI server
│   ├── main.py                     # FastAPI app, CORS, /api/chat endpoint
│   ├── agent.py                    # Groq agent loop with tool use
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── knowledge_base.py       # BM25 search over dhivya_profile.md
│   │   └── wikipedia_search.py     # Wikipedia API wrapper
│   ├── data/
│   │   └── dhivya_profile.md       # Personal knowledge base (edit this!)
│   ├── requirements.txt
│   ├── test_key.py                 # API key diagnostic script
│   └── .env                        # GROQ_API_KEY (not committed)
│
├── frontend/                       # React + Vite chat UI
│   ├── src/
│   │   ├── main.jsx                # React entry point
│   │   ├── App.jsx                 # Root component, chat state, API calls
│   │   ├── index.css               # Full UI styles
│   │   └── components/
│   │       ├── ChatWindow.jsx      # Scrollable message list
│   │       ├── Message.jsx         # Individual message bubble + search badges
│   │       └── InputBar.jsx        # Text input + send button
│   ├── index.html
│   ├── package.json
│   └── vite.config.js              # Dev server + /api proxy to backend
│
├── .env.example                    # Template for environment variables
└── README.md                       # This file
```

---

## 6. How the Agent Loop Works

The agent is implemented as an iterative loop in [`backend/agent.py`](backend/agent.py):

```python
# Simplified pseudocode
def run_agent(messages):
    chat_history = [system_prompt] + messages

    for iteration in range(max_iterations):
        response = groq.chat(chat_history, tools=[search_kb, search_wikipedia])

        if response has tool_calls:
            for each tool_call:
                result = execute_tool(tool_call.name, tool_call.args)
                append tool_result to chat_history

        else:  # model decided it has enough info
            return response.text
```

**Example trace for "What is Dhivya's GPA?":**

```
Turn 1 → Groq decides: call search_knowledge_base("Dhivya GPA education")
       ← KB returns: "Master of Science... CGPA: 3.85/4.0 ... KL University CGPA: 3.98/4.0"

Turn 2 → Groq has enough context, generates final answer:
       ← "Dhivya has a 3.85 GPA in her MS at University of Florida and
           a 3.98 GPA from her BTech at KL University."
```

**Example trace for "What is RAG and does Dhivya use it?":**

```
Turn 1 → Groq decides: call search_wikipedia("Retrieval-Augmented Generation RAG")
       ← Wikipedia returns: definition and background of RAG

Turn 2 → Groq decides: call search_knowledge_base("Dhivya RAG pipelines projects")
       ← KB returns: CATIA Lab work with RAG, LinguaEval project, this project

Turn 3 → Groq generates final answer combining both sources
```

---

## 7. The Knowledge Base & Retrieval

### Structure

The knowledge base is a single Markdown file (`backend/data/dhivya_profile.md`) divided into 26 sections:

```
# Dhivya Sri Lingala — Personal Profile
## Identity & Overview
## Education
### Master of Science — Artificial Intelligence Systems
### Bachelor of Technology — ...
## Technical Skills
### Programming Languages
### Generative AI & Agentic AI
... (26 sections total)
## Work Experience
### Graduate Research Assistant — UF CATIA Lab
### Software Developer Intern — Areksoft Technologies
### AI/ML Apprentice — Microsoft
## Projects
### SmartFin AI
### Emowise
### LinguaEval
### Text-to-Image Conversion
### Wikipedia AI Agent (this project)
## Interests & Goals
```

### How BM25 Search Works (Step by Step)

1. **Load** — On first search, `dhivya_profile.md` is parsed into 26 chunks, one per markdown section
2. **Tokenise** — Each chunk and the query are split into lowercase words, stop-words removed
3. **Score** — Each chunk gets a score based on keyword overlap with the query
4. **Return** — Top-4 highest-scoring chunks are returned as context to the LLM

```python
# Scoring example
query = "What university does Dhivya attend?"
query_keywords = {"university", "dhivya", "attend"}

chunk_1 (Education section):
   keywords = {"university", "florida", "masters", "cgpa", ...}
   overlap = {"university"} → score = 1/3 = 0.33  ✓

chunk_2 (Projects section):
   keywords = {"smartfin", "fastapi", "loan", ...}
   overlap = {} → score = 0  ✗
```

---

## 8. Setup & Running Locally

### Prerequisites

- Python 3.11+
- Node.js 18+
- A free [Groq API key](https://console.groq.com) (sign in with Google → API Keys → Create)

### Step 1 — Clone the repository

```bash
git clone https://github.com/DhivyaSriLingala/wikipedia-ai-agent.git
cd wikipedia-ai-agent
```

### Step 2 — Backend setup

```powershell
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1       # Windows PowerShell
# source venv/bin/activate         # Mac / Linux

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
copy ..\\.env.example .env
# Edit .env → set GROQ_API_KEY=gsk_...
```

### Step 3 — Verify the API key

```powershell
python test_key.py
# Expected output: SUCCESS: Hello.
```

### Step 4 — Start the backend

```powershell
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 5 — Frontend setup (new terminal)

```powershell
cd frontend
npm install
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in 300ms
  ➜  Local:   http://localhost:5173/
```

### Step 6 — Open the app

Navigate to **http://localhost:5173** and start asking questions!

### Environment Variables

| Variable | Description | Where to get |
|---|---|---|
| `GROQ_API_KEY` | Groq LLM API key | [console.groq.com](https://console.groq.com) |

---

## 9. API Reference

### `POST /api/chat`

Accepts a conversation history and returns the agent's response.

**Request body:**
```json
{
  "messages": [
    { "role": "user", "content": "What is Dhivya's GPA?" }
  ]
}
```

**Response:**
```json
{
  "response": "Dhivya has a CGPA of 3.85/4.0 in her Master's at University of Florida...",
  "search_actions": [
    { "tool": "search_knowledge_base", "query": "Dhivya GPA education" }
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `messages` | `array` | Full conversation history (role: `user` or `assistant`) |
| `response` | `string` | The agent's final answer (Markdown formatted) |
| `search_actions` | `array` | Which tools were called and with what queries |

### `GET /api/health`

```json
{ "status": "ok", "model": "qwen/qwen3-32b" }
```

---

## 10. Sample Questions to Try

### About Dhivya
```
Who is Dhivya Sri Lingala?
What is she currently studying?
What is her GPA?
Where did she do her undergrad?
What programming languages does she know?
Tell me about her experience at Microsoft.
What projects has she built?
What is the CATIA Lab project about?
What are her career interests?
How can I contact her?
```

### Combining Personal + Wikipedia Context
```
What is RAG and does Dhivya use it in her work?
What is LangChain and has she worked with it?
What is Bloom's Taxonomy and why is it relevant to Dhivya's research?
What is FastAPI and where has she used it?
What is multimodal AI and which of her projects uses it?
```

---

## 11. Customising the Knowledge Base

The knowledge base is just a Markdown file — no database, no reindexing required.

**To update it:**
1. Edit `backend/data/dhivya_profile.md`
2. Save the file
3. The next API request will automatically pick up the changes (no server restart needed)

**To adapt this for someone else:**
1. Replace `backend/data/dhivya_profile.md` with a new profile
2. Update the system prompt in `backend/agent.py` (change the name)
3. Update the UI copy in `frontend/src/App.jsx` and `frontend/src/components/ChatWindow.jsx`

The RAG pipeline is completely persona-agnostic.

---

## 12. Design Decisions

| Decision | Why |
|---|---|
| **BM25 over vector embeddings** | No embedding API cost, no vector DB, works well for structured <30-section KB |
| **Groq over OpenAI/Anthropic** | Free tier with fast inference; no credit card needed |
| **Qwen3-32B model** | Strong tool-use accuracy on Groq's free tier |
| **Markdown knowledge base** | Human-editable, version-controllable, no migration needed to update |
| **FastAPI + React** | FastAPI for fast async Python API; React for reactive chat UI |
| **Vite proxy for /api** | Single origin in development; no CORS preflight issues |
| **Tool use over naive RAG** | Agent decides what to search — avoids irrelevant retrievals and saves tokens |
| **Multi-turn history** | Full conversation passed each request; model maintains context naturally |

---

## About the Author

**Dhivya Sri Lingala** — MS Artificial Intelligence Systems @ University of Florida (GPA: 3.85)

Graduate Research Assistant building agentic AI systems at the CATIA Lab. This project was built as part of her AI engineering work at **Stackyon**.

- Portfolio: [dhivya-sri-lingala.vercel.app](https://dhivya-sri-lingala.vercel.app/)
- LinkedIn: [linkedin.com/in/dhivya-sri-lingala](https://www.linkedin.com/in/dhivya-sri-lingala/)
- GitHub: [github.com/DhivyaSriLingala](https://github.com/DhivyaSriLingala)

---

*Built with FastAPI · React · Groq · Wikipedia API · Python*
