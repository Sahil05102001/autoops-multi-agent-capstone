import subprocess
import tempfile
import os
from typing import Dict
from config import CODE_RUNNER_TIMEOUT
from infra.logger import get_logger

logger = get_logger("code_tool")

def run_python_code(code: str, timeout: int = CODE_RUNNER_TIMEOUT) -> Dict:
    """
    Runs Python code inside an isolated temporary file using subprocess.
    Returns a dictionary:
      - stdout: normal output
      - stderr: errors (if any)
      - returncode: 0 success, non-zero failure
    """

    # Create temporary .py file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write(code)
        filename = temp_file.name

    logger.info(f"[CodeTool] Executing code file: {filename}")

    try:
        # Execute code
        process = subprocess.run(
            ["python", filename],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        logger.info(
            f"[CodeTool] Finished (exit={process.returncode}) "
            f"stdout_length={len(process.stdout)}, stderr_length={len(process.stderr)}"
        )

        return {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "returncode": process.returncode,
        }

    except subprocess.TimeoutExpired:
        logger.warning(f"[CodeTool] Timeout after {timeout} seconds")
        return {"stdout": "", "stderr": f"Timed out after {timeout}s", "returncode": -1}

    except Exception as e:
        logger.error(f"[CodeTool] Unexpected error: {e}")
        return {"stdout": "", "stderr": str(e), "returncode": -2}

    finally:
        # Cleanup temp file
        try:
            os.remove(filename)
            logger.info(f"[CodeTool] Removed temp file: {filename}")
        except OSError:
            logger.warning(f"[CodeTool] Could not delete temp file: {filename}")