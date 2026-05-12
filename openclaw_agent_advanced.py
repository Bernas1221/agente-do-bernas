import os
import logging
from typing import Any, Dict

from prompt_injection_shield import sanitize_prompt

# Optional Claude API integration
try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None  # Will be None if the SDK is not installed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openclaw_agent")

class OpenClawAgent:
    """Core agent that can converse with other AIs on Moltbook and spot crypto opportunities."""

    def __init__(self, config: Dict[str, str] | None = None):
        self.config = config or self._load_env()
        self.claude_client = None
        if Anthropic and self.config.get("CLAUDE_API_KEY"):
            self.claude_client = Anthropic(api_key=self.config["CLAUDE_API_KEY"])
        logger.info("Agent initialized – Claude integration %s", "enabled" if self.claude_client else "disabled")

    def _load_env(self) -> Dict[str, str]:
        """Load configuration from environment variables. Keys are documented in .env.example."""
        keys = [
            "MOLTBOOK_API_TOKEN",
            "CLAUDE_API_KEY",
            "AGENT_NAME",
        ]
        cfg = {k: os.getenv(k, "") for k in keys}
        return cfg

    # ---------------------------------------------------------------------
    # Interaction with Moltbook (stub implementation)
    # ---------------------------------------------------------------------
    def fetch_peer_ai_messages(self) -> list[Dict[str, Any]]:
        """Placeholder: fetch recent messages from other agents on Moltbook.
        In a real implementation you would call Moltbook's REST or websocket API.
        """
        logger.debug("Fetching peer AI messages – stub returns empty list")
        return []

    def send_message(self, content: str) -> None:
        """Placeholder: send a message back to Moltbook.
        This would usually POST to an endpoint like /api/agents/{self.config['AGENT_NAME']}/messages.
        """
        logger.info("Sending message to Moltbook: %s", content[:200])
        # TODO: implement actual HTTP request using `requests` or `httpx`

    # ---------------------------------------------------------------------
    # Crypto opportunity detection (very simple heuristic)
    # ---------------------------------------------------------------------
    def detect_crypto_opportunity(self, text: str) -> bool:
        """Very naive detection: look for common crypto keywords and price mentions.
        Returns True if an opportunity is likely.
        """
        keywords = ["bitcoin", "btc", "ethereum", "eth", "crypto", "hodl", "price", "$"]
        lowered = text.lower()
        return any(kw in lowered for kw in keywords)

    # ---------------------------------------------------------------------
    # Main loop – runs continuously (Render's web service will keep the process alive)
    # ---------------------------------------------------------------------
    def run(self) -> None:
        logger.info("OpenClawAgent started – listening for Moltbook messages")
        while True:
            messages = self.fetch_peer_ai_messages()
            for msg in messages:
                raw = msg.get("content", "")
                safe_prompt = sanitize_prompt(raw)
                if not safe_prompt:
                    logger.warning("Message rejected by prompt‑injection shield")
                    continue
                response = self.generate_response(safe_prompt)
                self.send_message(response)
                if self.detect_crypto_opportunity(response):
                    logger.info("Crypto opportunity detected in response: %s", response)
            # Simple sleep to avoid tight loop – Render will manage CPU usage
            import time
            time.sleep(5)

    # ---------------------------------------------------------------------
    # Response generation (Claude optional)
    # ---------------------------------------------------------------------
    def generate_response(self, prompt: str) -> str:
        """Generate a contextual answer.
        If Claude is configured, use it; otherwise fall back to a deterministic placeholder.
        """
        if self.claude_client:
            try:
                completion = self.claude_client.completions.create(
                    model="claude-3-opus-20240229",
                    max_tokens=200,
                    temperature=0.7,
                    prompt=prompt,
                )
                return completion.completion.strip()
            except Exception as e:
                logger.error("Claude API error: %s", e)
        # Simple fallback – echo back with a friendly prefix
        return f"[OpenClaw] I received: {prompt}"

if __name__ == "__main__":
    agent = OpenClawAgent()
    agent.run()
