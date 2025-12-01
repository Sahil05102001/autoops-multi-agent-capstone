import asyncio
import os
from orchestrator.orchestrator import CoordinatorAgent
from config import GEMINI_API_KEY
from infra.logger import get_logger


async def run_user_goal(coordinator, goal: str):
    result = await coordinator.run(goal)

    print("\n=== PLAN STEPS ===")
    for i, step in enumerate(result.get('plan', {}).get('plan', []), start=1):
        print(f"Step {i}: {step.get('task', '')}")

    print("\n=== RESULTS & EVALUATIONS ===")
    for res in result.get('results', []):
        task = res.get('task', 'Unknown task')
        print(f"\nTask: {task}")

        if 'result' in res:
            # For "No agent available" or simple result strings
            print(f"Result: {res['result']}")
            continue

        output = res.get('output', {})
        evaluation = res.get('evaluation', {})

        # Extract and print text from nested 'output' if possible
        answer_text = ""
        events = output.get('results', [])
        if events and hasattr(events[0], "content"):
            parts = events[0].content.parts
            if parts and len(parts) > 0:
                answer_text = parts[0].text
        if not answer_text:
            # For simpler structured outputs (like from executor, analyzer, result combiner)
            inner_output = output.get('output') or output.get('result')
            if inner_output:
                answer_text = inner_output
            else:
                answer_text = str(output)

        print(f"Output:\n{answer_text}")

        print("\nEvaluation:")
        for key, val in evaluation.items():
            print(f"- {key.capitalize()}: {val}")

    # Nicely format and print memory content
    print("\n=== MEMORY CONTENT ===")
    all_memory = coordinator.memory.get_all()
    if all_memory:
        for idx, entry in enumerate(all_memory, start=1):
            print(f"\nMemory Entry {idx}:")
            print(f"Goal: {entry.get('goal', '')}")

            plan = entry.get('plan', {})
            if plan:
                print("Plan:")
                for step in plan.get('plan', []):
                    print(f"  Step {step.get('step')}: {step.get('task')}")

            results = entry.get('results', [])
            for res_idx, res in enumerate(results, start=1):
                print(f"\n  Result {res_idx} for task: {res.get('task', 'Unknown')}")
                output = res.get('output', {})

                # Attempt to extract readable text from nested Event/Content
                text_to_print = ""
                events = output.get('results', [])
                if events and hasattr(events[0], "content"):
                    parts = events[0].content.parts
                    if parts and len(parts) > 0:
                        text_to_print = parts[0].text

                if not text_to_print:
                    inner_output = output.get('output') or output.get('result')
                    text_to_print = inner_output if inner_output else str(output)

                print(f"    Output:\n{text_to_print}")
    else:
        print("Memory is empty.")


async def main():
    logger = get_logger("run")
    coordinator = CoordinatorAgent(gemini_api_key=GEMINI_API_KEY)

    user_goal = os.environ.get("GOAL") or input("Enter your goal/task: ").strip()
    await run_user_goal(coordinator, user_goal)


if __name__ == "__main__":
    asyncio.run(main())
