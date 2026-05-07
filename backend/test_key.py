"""Run this to verify your Groq API key is working."""
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY", "")
print(f"Key loaded : {'YES' if key else 'NO - check your backend/.env file'}")
print(f"Key length : {len(key)} chars")
print(f"Key starts : {key[:8]}..." if len(key) > 8 else f"Key value  : {repr(key)}")
print()

if not key or key == "your_groq_api_key_here":
    print("ERROR: GROQ_API_KEY not set in backend/.env")
    raise SystemExit(1)

print("Testing Groq API connection...")
try:
    from groq import Groq
    client = Groq(api_key=key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say hello in one word."}],
        max_tokens=10,
    )
    print("SUCCESS:", response.choices[0].message.content.strip())
except Exception as e:
    print(f"FAILED : {e}")
