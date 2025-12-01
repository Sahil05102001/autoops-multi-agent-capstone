# config.py
# Central configuration.
import os

SERPAPI_KEY = os.environ.get("SERPAPI_KEY", None)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

# Add Gemini Flash API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)

# Execution timeout (seconds) for code runner
CODE_RUNNER_TIMEOUT = int(os.environ.get("CODE_RUNNER_TIMEOUT", 10))
