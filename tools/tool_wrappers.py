import os
import json
import time
from typing import Any, Dict

# Optional: OpenAI integration if OPENAI_API_KEY is set.
try:
    import openai
except Exception:
    openai = None

class LLM:
    """
    Simple LLM wrapper. If OPENAI_API_KEY is present and openai installed, it will use OpenAI's API.
    Otherwise it returns placeholder responses. Replace or extend with Gemini/other provider as needed.
    """
    def __init__(self, model="gpt-4o-mini", timeout=20):
        self.model = model
        self.timeout = timeout
        self.api_key = os.environ.get('OPENAI_API_KEY')

        if self.api_key and openai:
            openai.api_key = self.api_key
            self.provider = 'openai'
        else:
            self.provider = 'placeholder'

    def call(self, prompt: str, max_tokens: int = 512) -> str:
        """Return a string response for a prompt."""
        if self.provider == 'openai':
            try:
                resp = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.2
                )
                # Safety: pick the assistant message content
                return resp['choices'][0]['message']['content'].strip()
            except Exception as e:
                # fallback
                return f"[LLM call failed: {e}]"
        else:
            # deterministic placeholder helpful response
            truncated = prompt[:800]
            return f"[LLM placeholder reply — echo of prompt start: {truncated} ...]"

def save_json(path: str, obj: Any):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
