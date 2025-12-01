import asyncio
from agents.coordinator.coordinator_agent import CoordinatorAgent
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

async def main():
    user_input = "whats your model name"
    coordinator = CoordinatorAgent(gemini_api_key=GEMINI_API_KEY)
    output = await coordinator.run(user_input)
    print(output)

if __name__ == "__main__":
    asyncio.run(main())