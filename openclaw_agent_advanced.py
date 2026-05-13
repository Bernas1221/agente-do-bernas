import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict

from prompt_injection_shield import sanitize_prompt

# Optional Claude API integration
try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None  # Will be None if the SDK is not installed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openclaw_agent")

# ---------------------------------------------------------------------
# Mini HTTP server so Render's Web Service detects an open port
# ---------------------------------------------------------------------
class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass  # silencia logs do servidor HTTP

def _start_health_server():
    port = int(os.getenv("PORT", 10000))
    HTTPServer(("0.0.0.0", port), _HealthHandler).serve_forever()

threading.Thread(target=_start_health_server, daemon=True).start()

# ---------------------------------------------------------------------

class OpenClawAgent:
    """Core agent that can converse with other AIs on Moltbook and spot crypto opportunities."""

    def __init__(self, config: Dict[str, str] | None = None):
        self.config = config or self._load_env()
        self.claude_client = None
        if Anthropic and self.config.get("CLAUDE_API_KEY"):
            self.claude_client = Anthropic(api_key=self.config["CLAUDE_API_KEY"])
        logger.info("Agent initialized – Claude integration %s", "enabled" if self.claude_client else "disabled")

    def _load_env(self) -> Dict[str, str]:
        keys = [
            "MOLTBOOK_API_TOKEN",
            "CLAUDE_API_KEY",
            "AGENT_NAME",
        ]
        cfg = {k: os.getenv(k, "") for k in keys}
        return cfg

    def fetch_peer_ai_messages(self) -> list[Dict[str, Any]]:
        logger.debug("Fetching peer AI messages – stub returns empty list")
        return []

    def send_message(self, content: str) -> None:
        logger.info("Sending message to Moltbook: %s", content[:200])

    def detect_crypto_opportunity(self, text: str) -> bool:
        keywords = ["bitcoin", "btc", "ethereum", "eth", "crypto", "hodl", "price", "$"]
        lowered = text.lower()
        return any(kw in lowered for kw in keywords)

    def run(self) -> None:
        logger.info("OpenClawAgent started – listening for Moltbook messages")
        while True:
            messages = self.fetch_peer_ai_messages()
            for msg in messages:
                raw = msg.get("content", "")
                safe_prompt = sanitize_prompt(raw)
                if not safe_prompt:
                    logger.warning("Mess