import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nova_config.json")

DEFAULT_SETTINGS: Dict[str, Any] = {
    "voice_speed": 1.0,
    "voice_volume": 1.0,
    "voice_gender": "Female",
    "rag_top_k": 4,
    "cross_encoder_enabled": True,
    "min_confidence_threshold": 50,
    "default_model": "gemini-2.5-flash",
    "temperature": 0.7,
    "theme": "Dark",
    "auto_save_chat": True,
}


def load_settings() -> Dict[str, Any]:
    """
    Loads persistent application settings from nova_config.json.
    Returns default settings if config file does not exist or fails to parse.
    """
    if not os.path.exists(CONFIG_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Merge with defaults to guarantee all expected keys exist
        merged = DEFAULT_SETTINGS.copy()
        merged.update(data)
        return merged
    except Exception as e:
        logger.error(f"Error loading configuration file '{CONFIG_FILE}': {e}")
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: Dict[str, Any]) -> bool:
    """
    Saves updated configuration dictionary to nova_config.json.
    """
    try:
        current = load_settings() if os.path.exists(CONFIG_FILE) else DEFAULT_SETTINGS.copy()
        current.update(settings)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=4)

        logger.info(f"Successfully saved persistent configuration to '{CONFIG_FILE}'.")
        return True
    except Exception as e:
        logger.error(f"Failed to save settings: {e}")
        return False


def get_setting(key: str, default: Any = None) -> Any:
    """
    Retrieves a specific configuration key value.
    """
    settings = load_settings()
    return settings.get(key, default)


def update_setting(key: str, value: Any) -> bool:
    """
    Updates a single configuration key value and saves to disk.
    """
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)
