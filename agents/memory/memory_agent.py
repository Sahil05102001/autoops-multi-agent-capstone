import logging
from typing import Any, List

class MemoryAgent:
    def __init__(self):
        self.logger = logging.getLogger("memory")
        self.data: List[Any] = []
        self.logger.info("✅ MemoryAgent initialized.")

    def store(self, entry: Any):
        """
        Store any data (task results, research response, actions, etc.)
        """
        self.logger.info(f"[MemoryAgent] Storing entry: {entry}")
        self.data.append(entry)

    def get_all(self) -> List[Any]:
        """
        Return entire memory store.
        """
        self.logger.info("[MemoryAgent] Fetching all memory entries.")
        return self.data

    def clear(self):
        """
        Optional: Clears memory.
        """
        self.logger.info("[MemoryAgent] Clearing all memory.")
        self.data = []