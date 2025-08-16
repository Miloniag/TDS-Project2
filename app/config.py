import os

API_NAME = os.getenv("API_NAME", "TDS Data Analyst Agent")
HARD_TIMEOUT_SECS = int(os.getenv("HARD_TIMEOUT_SECS", "170"))  # < 3 min incl. overhead
MAX_RETURN_BYTES = int(os.getenv("MAX_RETURN_BYTES", "800000"))  # safety cap
USER_AGENT = os.getenv("USER_AGENT", "tds-analyst-agent/1.0")
