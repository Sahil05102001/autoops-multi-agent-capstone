import asyncio
import os
from dotenv import load_dotenv
from agents.coordinator.coordinator_agent import CoordinatorAgent

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

async def main():
    user_input = "What's your model name?"
    coordinator = CoordinatorAgent(gemini_api_key=GEMINI_API_KEY)

    print("\n🚀 Running Coordinator Pipeline...\n")
    output = await coordinator.run(user_input)

    print("\n==== FINAL OUTPUT ====")
    print(output)

if __name__ == "__main__":
    asyncio.run(main())