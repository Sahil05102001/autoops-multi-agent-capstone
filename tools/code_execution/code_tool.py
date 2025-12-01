import subprocess
import tempfile
import os
from typing import Dict
from config import CODE_RUNNER_TIMEOUT
from infra.logger import get_logger

logger = get_logger("code_tool")

def run_python_code(code: str, timeout: int = CODE_RUNNER_TIMEOUT) -> Dict:
    """
    Writes code to a temp file and executes it via subprocess with a timeout.
    Returns stdout, stderr, exit_code.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        fname = f.name

    try:
        logger.info(f"[CodeTool] Executing code in temp file: {fname}")
        proc = subprocess.run(
            ["python", fname],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        logger.info(f"[CodeTool] Execution completed with returncode={proc.returncode}")
        return {"stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}

    except subprocess.TimeoutExpired as te:
        logger.warning(f"[CodeTool] Execution timed out after {timeout}s")
        return {"stdout": "", "stderr": f"Timed out after {timeout}s", "returncode": -1}

    except Exception as e:
        logger.error(f"[CodeTool] Execution failed: {e}")
        return {"stdout": "", "stderr": str(e), "returncode": -2}

    finally:
        try:
            os.remove(fname)
            logger.info(f"[CodeTool] Temp file removed: {fname}")
        except OSError:
            logger.warning(f"[CodeTool] Failed to remove temp file: {fname}")
