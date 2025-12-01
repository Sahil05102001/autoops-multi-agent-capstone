"""
Entrypoint to run a demo: create the agents, run a sample goal, print results.
Run: python main.py
"""

import asyncio
from agents.coordinator.coordinator_agent import CoordinatorAgent
from infra.logger import get_logger
from config import GEMINI_API_KEY

async def demo():
    logger = get_logger("main")
    
    # Initialize CoordinatorAgent with all agents
    coordinator = CoordinatorAgent(gemini_api_key=GEMINI_API_KEY)

    goal = "Create a short itinerary for a 2-day budget trip to Goa and produce a packing list"

    logger.info(f"[Demo] Running goal: {goal}")
    result = await coordinator.run(goal)

    # Print plan steps
    print("\n=== PLAN STEPS ===")
    for i, step in enumerate(result['plan']['plan'], start=1):
        print(f"Step {i}: {step['task']}")

    # Print results for each task
    print("\n=== RESULTS ===")
    for i, res in enumerate(result['results'], start=1):
        print(f"Task: {res['task']}")
        print(f"Output: {res['output']}")
        print(f"Evaluation: {res.get('evaluation')}")
        print("------")

    # Print memory contents
    print("\n=== MEMORY CONTENT ===")
    for session in coordinator.memory.get_all():
        print(session)

if __name__ == "__main__":
    asyncio.run(demo())