from typing import Any, Dict

class EvaluatorAgent:
    """
    Evaluates outputs from all agents:
    Research → Analyzer → Executor → ResultCombiner → Fallback
    """

    def __init__(self):
        pass

    async def run(self, agent_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze agent output and return standardized evaluation.
        """

        output_type = agent_output.get("type", "unknown")
        output_value = agent_output.get("output", "")

        # ---------------------------
        # 1. Code Execution Evaluation
        # ---------------------------
        if output_type == "code_run":
            stderr = output_value.get("stderr", "")
            success = (stderr == "")
            return {
                "type": "evaluation",
                "target": "executor",
                "success": success,
                "error": stderr if not success else None,
                "notes": "Code executed successfully" if success else "Code execution failed.",
            }

        # ---------------------------
        # 2. Research Output Evaluation
        # ---------------------------
        if output_type == "research":
            return {
                "type": "evaluation",
                "target": "researcher",
                "success": True,
                "notes": "Research text generated.",
                "length": len(str(output_value))
            }

        # ---------------------------
        # 3. Analysis Output Evaluation
        # ---------------------------
        if output_type == "analysis":
            return {
                "type": "evaluation",
                "target": "analyzer",
                "success": True,
                "notes": "Analysis completed.",
                "output_preview": str(output_value)[:120]
            }

        # ---------------------------
        # 4. Combined Result Evaluation
        # ---------------------------
        if output_type == "combined_result":
            return {
                "type": "evaluation",
                "target": "result_combiner",
                "success": True,
                "notes": "Final result successfully assembled.",
                "output_preview": str(output_value)[:120]
            }

        # ---------------------------
        # 5. Basic Executor Evaluation
        # ---------------------------
        if output_type == "execute":
            return {
                "type": "evaluation",
                "target": "executor",
                "success": True,
                "notes": "Task executed successfully.",
                "output_preview": str(output_value)[:120]
            }

        # ---------------------------
        # 6. Unknown Type (Fallback)
        # ---------------------------
        return {
            "type": "evaluation",
            "target": "unknown",
            "success": False,
            "notes": "Unknown output type received.",
            "output_preview": str(output_value)[:120]
        }