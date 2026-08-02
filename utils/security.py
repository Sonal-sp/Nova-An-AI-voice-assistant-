import os
import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def mask_api_key(key: str) -> str:
    """
    Masks sensitive API key strings for safe display in logs and UI.
    """
    if not key or not isinstance(key, str):
        return "Not Set"

    clean_key = key.strip()
    if len(clean_key) <= 10:
        return "********"

    return f"{clean_key[:6]}...{clean_key[-4:]}"


def sanitize_input(text: str) -> str:
    """
    Sanitizes user input by stripping control characters and normalizing whitespace.
    """
    if not text:
        return ""

    # Remove null bytes and non-printable control characters
    sanitized = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", str(text))
    # Normalize multiple whitespace spaces
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized


def validate_credentials() -> Dict[str, Any]:
    """
    Verifies environmental API credentials.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    masked = mask_api_key(api_key)

    if not api_key:
        logger.warning("GEMINI_API_KEY is not set in environment.")
        return {
            "valid": False,
            "masked_key": "Missing",
            "message": "GEMINI_API_KEY is not set. Please add it to your .env file.",
        }

    logger.info(f"Verified Gemini API key: {masked}")
    return {
        "valid": True,
        "masked_key": masked,
        "message": f"Gemini API Credential Active ({masked})",
    }
