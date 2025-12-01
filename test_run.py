# test_run.py
import asyncio
from orchestrator.orchestrator import CoordinatorAgent
from config import GEMINI_API_KEY

async def run_test_goal():
    # Initialize the coordinator with Gemini API key
    coordinator = CoordinatorAgent(gemini_api_key=GEMINI_API_KEY)

    # Define a sample test goal
    test_goal = "Research latest renewable energy trends and summarize key findings"

    print(f"\n=== Running test goal: {test_goal} ===\n")
    result = await coordinator.run(test_goal)

    # Print plan steps
    print("\n--- PLAN STEPS ---")
    for i, step in enumerate(result["plan"]["steps"], start=1):
        print(f"Step {i}: {step['step']} (Type: {step.get('type', 'execute')})")

    # Print research results
    print("\n--- RESEARCH RESULTS ---")
    for i, res in enumerate(result["research"], start=1):
        print(f"Research {i}: {res}")

    # Print execution results
    print("\n--- EXECUTION RESULTS ---")
    for i, res in enumerate(result["executions"], start=1):
        print(f"Execution {i}: {res}")

    # Print memory content
    print("\n--- MEMORY CONTENT ---")
    for session in coordinator.memory.get_all_sessions():
        print(session)

if __name__ == "__main__":
    asyncio.run(run_test_goal())
