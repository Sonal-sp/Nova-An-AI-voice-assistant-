import json
import logging
import urllib.request
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

DEFAULT_OLLAMA_URL = "http://localhost:11434"


def is_ollama_available(base_url: str = DEFAULT_OLLAMA_URL) -> bool:
    """
    Verifies if local Ollama server is running and responsive.
    """
    try:
        req = urllib.request.Request(f"{base_url}/api/tags", headers={"User-Agent": "Nova-AI"})
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False


def get_local_models(base_url: str = DEFAULT_OLLAMA_URL) -> List[str]:
    """
    Fetches list of locally installed Ollama models.
    """
    try:
        req = urllib.request.Request(f"{base_url}/api/tags", headers={"User-Agent": "Nova-AI"})
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            models = [m.get("name") for m in data.get("models", [])]
            return models if models else ["llama3:latest"]
    except Exception as e:
        logger.warning(f"Could not fetch Ollama models: {e}")
        return ["llama3:latest"]


def generate_local_response(
    prompt: str,
    model: str = "llama3:latest",
    system_prompt: str = "You are Nova, an intelligent local AI assistant.",
    base_url: str = DEFAULT_OLLAMA_URL,
    max_tokens: int = 256,
    timeout_sec: int = 15,
) -> Optional[str]:
    """
    Generates response from local LLM via Ollama REST API with responsive 15s timeout threshold.
    If local model loading is slow or unresponsive on CPU, triggers instant Gemini fallback.

    Parameters
    ----------
    prompt : str
        User prompt text.
    model : str
        Local Ollama model name (e.g. 'llama3:latest').
    system_prompt : str
        System instructions.
    base_url : str
        Ollama REST API base URL.
    max_tokens : int
        Max response tokens to generate.
    timeout_sec : int
        Responsive timeout threshold in seconds.

    Returns
    -------
    Optional[str]
        Generated response text or None on timeout/error.
    """
    if not is_ollama_available(base_url):
        logger.warning("Ollama server is not running.")
        return None

    try:
        url = f"{base_url}/api/generate"
        clean_sys = system_prompt[:500] if system_prompt else "You are Nova, a helpful AI assistant."

        payload_data = {
            "model": model,
            "prompt": prompt,
            "system": clean_sys,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7,
            },
        }
        payload = json.dumps(payload_data).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

        logger.info(f"Dispatching query to local Ollama model '{model}' (timeout={timeout_sec}s)...")
        with urllib.request.urlopen(req, timeout=timeout_sec) as response:
            data = json.loads(response.read().decode())
            res = data.get("response", "").strip()
            if res:
                logger.info(f"Successfully received local response from '{model}' ({len(res)} chars).")
                return res
            return None
    except Exception as e:
        logger.warning(f"Local Ollama generation timed out or failed ({e}). Triggering Gemini 2.5 Flash fallback.")
        return None
