import json
import os
from groq import Groq
from rag.wikipedia_search import search_wikipedia
from rag.knowledge_base import search_knowledge_base

MODEL = "qwen/qwen3-32b"

SYSTEM_PROMPT = """\
You are a knowledgeable and friendly AI assistant specialized in answering questions about Dhivya Sri Lingala.

You have two tools:
1. search_knowledge_base – A curated personal profile with Dhivya's professional background, skills, education, projects, and interests. Always use this FIRST for any question about Dhivya.
2. search_wikipedia – Wikipedia for general/supplementary knowledge (technologies, concepts, companies, etc.).

Guidelines:
- For personal questions about Dhivya (career, education, skills, projects, hobbies), always call search_knowledge_base first.
- If the knowledge base result is insufficient, use search_wikipedia for supplementary context.
- For purely general knowledge questions not related to Dhivya, use search_wikipedia directly.
- Synthesize retrieved content into clear, accurate, conversational answers.
- If information is unavailable in either source, say so honestly rather than guessing.
- Keep responses concise but complete.\
"""

_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": (
                "Search the personal knowledge base containing curated information about "
                "Dhivya Sri Lingala: her professional background, skills, education, projects, "
                "achievements, and personal interests. Use this for any question about Dhivya."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find relevant information about Dhivya",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": (
                "Search Wikipedia for general knowledge, background context, or supplementary "
                "information about technologies, concepts, places, organisations, or any topic "
                "where factual encyclopedic information would help answer the question."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for Wikipedia",
                    }
                },
                "required": ["query"],
            },
        },
    },
]


def _execute_tool(name: str, args: dict) -> str:
    if name == "search_knowledge_base":
        return search_knowledge_base(args.get("query", ""))
    if name == "search_wikipedia":
        return search_wikipedia(args.get("query", ""))
    return f"Unknown tool: {name}"


def run_agent(messages: list[dict], max_iterations: int = 6) -> dict:
    """Run the Groq RAG agent loop. Returns {"response": str, "search_actions": list}."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + list(messages)
    search_actions: list[dict] = []

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=MODEL,
            messages=chat_messages,
            tools=_TOOLS,
            tool_choice="auto",
            max_tokens=2048,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return {
                "response": message.content or "No response generated.",
                "search_actions": search_actions,
            }

        # Append the assistant turn (with tool_calls) to history
        chat_messages.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in message.tool_calls
                ],
            }
        )

        # Execute every tool call and append results
        for tc in message.tool_calls:
            args = json.loads(tc.function.arguments)
            result = _execute_tool(tc.function.name, args)
            search_actions.append(
                {"tool": tc.function.name, "query": args.get("query", "")}
            )
            chat_messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                }
            )

    return {
        "response": "Reached search limit. Please try a more specific question.",
        "search_actions": search_actions,
    }
