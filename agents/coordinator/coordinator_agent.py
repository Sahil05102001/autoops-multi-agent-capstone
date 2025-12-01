from infra.logger import get_logger

from agents.planner.planner_agent import PlannerAgent
from agents.researcher.research_agent import ResearchAgent
from agents.executor.executor_agent import ExecutorAgent
from agents.memory.memory_agent import MemoryAgent
from agents.evaluator.evaluator_agent import EvaluatorAgent

from agents.analyzer.analyzer_agent import AnalyzerAgent
from agents.combiner.result_combiner_agent import ResultCombinerAgent


class CoordinatorAgent:
    """
    CoordinatorAgent orchestrates the complete multi-agent pipeline:
    Planner → Researcher → Analyzer → Executor → ResultCombiner → Evaluator
    """

    def __init__(self, gemini_api_key=None):
        self.logger = get_logger("coordinator")

        # Initialize agents
        self.memory = MemoryAgent()
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent(api_key=gemini_api_key)
        self.analyzer = AnalyzerAgent()
        self.executor = ExecutorAgent()
        self.result_combiner = ResultCombinerAgent()
        self.evaluator = EvaluatorAgent()

        self.logger.info("✅ Coordinator initialized with all agents.")

    async def run(self, user_input: str):
        """
        Main pipeline execution:
        - Generate plan
        - Execute each step with appropriate agent
        - Evaluate each step
        - Store memories
        """
        self.logger.info(f"[Coordinator] Pipeline started for goal: {user_input}")

        # 1. Generate plan
        plan_dict = await self.planner.plan_only(user_input)
        self.logger.info(f"[Coordinator] Generated plan: {plan_dict}")

        results = []

        # 2. Execute each step
        for step in plan_dict["plan"]:
            task = step["task"]
            self.logger.info(f"[Coordinator] Running task: {task}")

            # Route to correct agent
            if "Research" in task:
                output = await self.researcher.run(task)

            elif "Analyze" in task:
                output = await self.analyzer.run(task)

            elif "Execute" in task:
                output = await self.executor.run(task)

            elif "Return final" in task or "Combine" in task:
                output = await self.result_combiner.run(task)

            else:
                output = {"type": "unknown", "output": "⚠ No agent available for this task"}

            # Evaluate the generated output
            evaluation = await self.evaluator.run(output)

            # Collect step results
            results.append({
                "task": task,
                "output": output,
                "evaluation": evaluation
            })

        # 3. Store everything in memory
        self.memory.store({
            "goal": user_input,
            "plan": plan_dict,
            "results": results
        })

        # 4. Return final response to caller
        return {
            "plan": plan_dict,
            "results": results
        }