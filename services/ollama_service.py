import json
import logging
import urllib.request
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

DEFAULT_OLLAMA_URL = "http://localhost:11434"


def is_ollama_available(base_url: str = DEFAULT_OLLAMA_URL) -> bool:
    """
    Verifies if local Ollama server is running.
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
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            models = [m.get("name") for m in data.get("models", [])]
            return models if models else ["llama3:latest", "mistral:latest"]
    except Exception as e:
        logger.warning(f"Could not fetch Ollama models: {e}")
        return ["llama3:latest", "mistral:latest", "gemma:latest", "phi3:latest"]


def generate_local_response(
    prompt: str,
    model: str = "llama3:latest",
    system_prompt: str = "You are Nova, an intelligent offline local AI assistant.",
    base_url: str = DEFAULT_OLLAMA_URL,
) -> Optional[str]:
    """
    Generates response from local LLM via Ollama REST API endpoint.
    """
    try:
        url = f"{base_url}/api/generate"
        payload_data = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
        }
        payload = json.dumps(payload_data).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data.get("response", "").strip()
    except Exception as e:
        logger.error(f"Local Ollama generation failed: {e}")
        return f"⚠️ Local Offline Model Error: Unable to connect to Ollama server at `{base_url}`. ({e})"
