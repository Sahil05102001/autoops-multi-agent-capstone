import logging

class MemoryAgent:
    def __init__(self):
        self.logger = logging.getLogger("memory")
        self.data = []
        self.logger.info("[MemoryAgent] Memory loaded successfully.")

    def store(self, entry):
        self.logger.info(f"[MemoryAgent] Storing entry: {entry}")
        self.data.append(entry)

    def get_all(self):
        return self.data