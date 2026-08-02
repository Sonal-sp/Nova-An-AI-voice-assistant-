import re
import logging
from typing import Tuple, Dict, Any, Optional

logger = logging.getLogger(__name__)

WAKE_WORDS = ["hey nova", "listen nova", "ok nova", "hello nova", "hi nova", "nova"]


def detect_wake_word(transcript: str) -> Tuple[bool, str]:
    """
    Detects if spoken transcript contains a Nova trigger phrase ('Hey Nova', 'Nova').

    Parameters
    ----------
    transcript : str
        Transcribed audio text.

    Returns
    -------
    Tuple[bool, str]
        Tuple of (is_wake_word_detected, command_payload).
    """
    if not transcript or not transcript.strip():
        return False, ""

    clean_text = transcript.strip().lower()

    for trigger in WAKE_WORDS:
        # Match trigger word at start or embedded
        pattern = r"\b" + re.escape(trigger) + r"\b"
        match = re.search(pattern, clean_text)
        if match:
            # Extract remaining text after wake word
            end_idx = match.end()
            command_payload = clean_text[end_idx:].strip()

            # Clean leading punctuation
            command_payload = re.sub(r"^[,\s.:;?!]+", "", command_payload).strip()
            if not command_payload:
                command_payload = "hello"

            logger.info(f"Wake word '{trigger}' detected. Command payload: '{command_payload}'")
            return True, command_payload

    return False, transcript.strip()


def process_voice_command(transcript: str) -> Dict[str, Any]:
    """
    Processes spoken voice input, checks for wake words, and routes to pipeline.

    Parameters
    ----------
    transcript : str
        Transcribed speech text.

    Returns
    -------
    Dict[str, Any]
        Voice command execution result.
    """
    has_wake_word, command_text = detect_wake_word(transcript)

    return {
        "wake_word_detected": has_wake_word,
        "command_text": command_text if has_wake_word else transcript.strip(),
        "raw_transcript": transcript.strip(),
    }
