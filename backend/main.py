from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import run_agent

app = FastAPI(title="Dhivya AI Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Vercel preview URLs are dynamic; restrict to your domain after launch
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


class SearchAction(BaseModel):
    tool: str
    query: str


class ChatResponse(BaseModel):
    response: str
    search_actions: list[SearchAction]


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty")

    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    try:
        result = run_agent(messages)
        return ChatResponse(
            response=result["response"],
            search_actions=[SearchAction(**a) for a in result["search_actions"]],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health():
    return {"status": "ok", "model": "qwen/qwen3-32b"}
