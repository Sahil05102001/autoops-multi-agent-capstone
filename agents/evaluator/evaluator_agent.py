# agents/evaluator/evaluator_agent.py

from typing import Any, Dict, List

class EvaluatorAgent:
    def __init__(self):
        pass

    async def run(self, agent_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the output from ResearchAgent or ExecutorAgent.
        Returns a simple evaluation with:
        - success flag
        - error detection
        - quality notes
        """

        # Code execution result
        if agent_output.get("type") == "code_run":
            stderr = agent_output["output"].get("stderr", "")
            success = (stderr == "")
            return {
                "success": success,
                "error": stderr if not success else None,
                "notes": "Code executed successfully" if success else "Code failed"
            }

        # Research text result
        if agent_output.get("type") == "research":
            text = agent_output.get("output", "")
            return {
                "success": True,
                "notes": "Research text generated.",
                "length": len(str(text))
            }

        # Default evaluation
        return {
            "success": True,
            "notes": "Generic task executed."
        }