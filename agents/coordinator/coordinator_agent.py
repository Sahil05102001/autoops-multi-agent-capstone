from infra.logger import get_logger
from agents.planner.planner_agent import PlannerAgent
from agents.researcher.research_agent import ResearchAgent
from agents.executor.executor_agent import ExecutorAgent
from agents.memory.memory_agent import MemoryAgent

class CoordinatorAgent:
    """
    CoordinatorAgent orchestrates the pipeline:
    Planner → Researcher → Executor
    """

    def __init__(self, gemini_api_key=None):
        self.logger = get_logger("coordinator")

        self.memory = MemoryAgent()
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent(api_key=gemini_api_key)
        self.executor = ExecutorAgent()

        self.logger.info("✅ Coordinator initialized with all agents.")

    async def run(self, user_input: str):
        self.logger.info(f"[Coordinator] Pipeline started for goal: {user_input}")
        plan_dict = await self.planner.plan_only(user_input)

        results = []
        for step in plan_dict["plan"]:
            task = step["task"]

            if "Research" in task:
                results.append(await self.researcher.run(task))
            elif "Execute" in task:
                results.append(await self.executor.run(task))
            else:
                results.append({"task": task, "result": "No agent available"})

        self.memory.store({"goal": user_input, "plan": plan_dict, "results": results})
        return {"plan": plan_dict, "results": results}