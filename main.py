"""
Entrypoint to run a demo: create the agents, run a sample goal, print results.
Run: python main.py
"""

import asyncio
from agents.memory.memory_agent import MemoryAgent
from agents.planner.planner_agent import PlannerAgent
from agents.executor.executor_agent import ExecutorAgent
from agents.researcher.research_agent import ResearchAgent
from agents.coordinator.coordinator_agent import CoordinatorAgent
from infra.logger import get_logger
from config import GEMINI_API_KEY

async def demo():
    logger = get_logger("main")
    
    # Initialize CoordinatorAgent with memory + research + executor + planner
    coordinator = CoordinatorAgent(gemini_api_key=GEMINI_API_KEY)

    goal = "Create a short itinerary for a 2-day budget trip to Goa and produce a packing list"

    logger.info(f"[Demo] Running goal: {goal}")
    result = await coordinator.run(goal)

    print("\n=== PLAN STEPS ===")
    for i, step in enumerate(result['plan']['steps'], start=1):
        print(f"Step {i}: {step['step']} (Type: {step.get('type', 'execute')})")

    print("\n=== RESEARCH RESULTS ===")
    for i, res in enumerate(result['research'], start=1):
        print(f"Research {i}: {res}")

    print("\n=== EXECUTION RESULTS ===")
    for i, res in enumerate(result['executions'], start=1):
        print(f"Execution {i}: {res}")

    print("\n=== MEMORY CONTENT ===")
    for session in coordinator.memory.get_all_sessions():
        print(session)

if __name__ == "__main__":
    asyncio.run(demo())
