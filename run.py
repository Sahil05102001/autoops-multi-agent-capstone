"""
run.py
Interactive entrypoint to run the full multi-agent orchestrator pipeline.
"""

import asyncio
import os
from orchestrator.orchestrator import CoordinatorAgent
from config import GEMINI_API_KEY
from infra.logger import get_logger

async def run_user_goal(coordinator, goal: str):
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

def main():
    logger = get_logger("run")
    coordinator = CoordinatorAgent(gemini_api_key=GEMINI_API_KEY)

    # Take goal from environment variable or prompt user
    user_goal = os.environ.get("GOAL") or input("Enter your goal/task: ").strip()

    # Run the pipeline
    asyncio.run(run_user_goal(coordinator, user_goal))

if __name__ == "__main__":
    main()
