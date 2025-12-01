import logging
from typing import Dict, List

class PlannerAgent:
    def __init__(self):
        self.logger = logging.getLogger("planner")
        self.logger.info("✅ PlannerAgent initialized.")

    async def plan_only(self, goal: str) -> Dict:
        """
        Generates a simple task plan based on user goal.
        Coordinator will route these tasks to the appropriate agents.
        """
        self.logger.info(f"[Planner] Creating plan for goal: {goal}")

        plan: List[Dict] = [
            {"step": 1, "task": f"Research: {goal}"},
            {"step": 2, "task": f"Analyze results for: {goal}"},
            {"step": 3, "task": f"Execute operations for: {goal}"},
            {"step": 4, "task": f"Return final output for: {goal}"},
        ]

        return {
            "goal": goal,
            "plan": plan
        }