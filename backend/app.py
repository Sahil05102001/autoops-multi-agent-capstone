import sys
import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.coordinator.coordinator_agent import CoordinatorAgent

# Load env
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# FastAPI app
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://autoopsagent.web.app",
        "https://autoopsagent.firebaseapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def chat(req: PromptRequest):
    """
    Accepts user prompt → sends to CoordinatorAgent → returns only first meaningful text
    """

    coordinator = CoordinatorAgent(gemini_api_key=GEMINI_API_KEY)

    try:
        response = await coordinator.run(req.prompt)

        # Extract first meaningful text
        assistant_text = ""
        if isinstance(response, dict) and "results" in response:
            for res in response["results"]:
                # Check for 'results' in res
                if "results" in res:
                    for r in res["results"]:
                        if hasattr(r, "content") and hasattr(r.content, "parts"):
                            for part in r.content.parts:
                                if hasattr(part, "text") and part.text:
                                    assistant_text = part.text
                                    break
                        if assistant_text:
                            break
                # If assistant_text found, break outer loop
                if assistant_text:
                    break

        # Fallback if nothing found
        if not assistant_text:
            assistant_text = "No response from agent."

        return {"response": assistant_text.strip()}

    except Exception as e:
        return {"error": str(e)}