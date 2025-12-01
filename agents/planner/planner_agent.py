import logging

class PlannerAgent:
    def __init__(self):
        self.logger = logging.getLogger("planner")
        self.logger.info("✅ PlannerAgent initialized.")

    async def plan_only(self, goal: str):
        self.logger.info(f"[Planner] Creating plan for goal: {goal}")
        # Simple plan example
        plan = [
            {"step": 1, "task": f"Research: {goal}"},
            {"step": 2, "task": f"Analyze data related to: {goal}"},
            {"step": 3, "task": f"Execute operations for: {goal}"},
            {"step": 4, "task": "Return final combined result"},
        ]
        return {"goal": goal, "plan": plan}