import logging
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

class ResearchAgent:
    def __init__(self, api_key=None):
        self.logger = logging.getLogger("research")
        self.api_key = api_key

        retry_config = types.HttpRetryOptions(
            attempts=5,
            exp_base=7,
            initial_delay=1,
            http_status_codes=[429, 500, 503, 504],
        )

        self.agent = Agent(
            name="researcher_agent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                api_key=self.api_key,
                retry_options=retry_config,
            ),
            description="Research agent to answer queries.",
            instruction="Use Google Search for current info if unsure.",
            tools=[google_search],
        )

        self.runner = InMemoryRunner(agent=self.agent)
        self.logger.info("✅ ResearchAgent initialized.")

    async def run(self, query: str):
        """
        Runs a research query through Gemini ADK.
        Output is normalized to structure expected by Coordinator + Evaluator.
        """
        self.logger.info(f"🔍 Researching: {query}")

        try:
            response = await self.runner.run_debug(query)

            # Handle ADK output forms (list or object)
            if isinstance(response, list):
                results_list = response
                summary_text = " ".join([str(r) for r in response])
            else:
                results_list = (
                    getattr(response, "results", None)
                    or [str(response)]
                )
                summary_text = (
                    getattr(response, "summary", None)
                    or str(response)
                )

            return {
                "type": "research",        # REQUIRED FOR EVALUATOR
                "query": query,
                "output": summary_text,
                "results": results_list,
            }

        except Exception as e:
            self.logger.error(f"❌ Gemini ADK call failed: {e}")

            return {
                "type": "research",
                "query": query,
                "output": f"Research failed: {e}",
                "results": [],
            }