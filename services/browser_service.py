import logging
import urllib.parse
import webbrowser
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)

# Preset shortcuts
PRESET_SHORTCUTS: Dict[str, str] = {
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chatgpt.com",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "maps": "https://www.google.com/maps",
    "google maps": "https://www.google.com/maps",
    "stackoverflow": "https://stackoverflow.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
}


def open_url(url: str) -> bool:
    """
    Opens target URL in user's default desktop web browser tab.

    Parameters
    ----------
    url : str
        Target website URL.

    Returns
    -------
    bool
        True if successfully launched, False otherwise.
    """
    if not url or not url.strip():
        logger.warning("Empty URL provided to open_url.")
        return False

    url = url.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url

    try:
        webbrowser.open_new_tab(url)
        logger.info(f"Opened URL in desktop browser: {url}")
        return True
    except Exception as e:
        logger.error(f"Failed to open URL '{url}' in browser: {e}")
        return False


def search_google(query: str) -> Tuple[bool, str]:
    """
    Performs a Google Search in default browser.

    Parameters
    ----------
    query : str
        Search query string.

    Returns
    -------
    Tuple[bool, str]
        (Success status, Target URL)
    """
    encoded = urllib.parse.quote_plus(query.strip())
    url = f"https://www.google.com/search?q={encoded}"
    success = open_url(url)
    return success, url


def search_youtube(query: str) -> Tuple[bool, str]:
    """
    Performs a YouTube Search in default browser.

    Parameters
    ----------
    query : str
        Video search query string.

    Returns
    -------
    Tuple[bool, str]
        (Success status, Target URL)
    """
    encoded = urllib.parse.quote_plus(query.strip())
    url = f"https://www.youtube.com/results?search_query={encoded}"
    success = open_url(url)
    return success, url


def search_google_maps(query: str) -> Tuple[bool, str]:
    """
    Performs a Google Maps location search in default browser.

    Parameters
    ----------
    query : str
        Location or place search query string.

    Returns
    -------
    Tuple[bool, str]
        (Success status, Target URL)
    """
    encoded = urllib.parse.quote_plus(query.strip())
    url = f"https://www.google.com/maps/search/{encoded}"
    success = open_url(url)
    return success, url


def execute_browser_action(action_type: str, target: str) -> Dict[str, Any]:
    """
    Executes specified browser action and returns formatted status dictionary.

    Parameters
    ----------
    action_type : str
        'open_preset' | 'open_url' | 'search_google' | 'search_youtube' | 'search_maps'
    target : str
        Preset name, custom URL, or search query string.

    Returns
    -------
    Dict[str, Any]
        Dictionary with 'success', 'action', 'target', 'message', 'url'.
    """
    target_clean = target.strip()
    action_type = action_type.lower()

    if action_type == "open_preset":
        preset_key = target_clean.lower()
        url = PRESET_SHORTCUTS.get(preset_key, f"https://{preset_key}.com")
        success = open_url(url)
        return {
            "success": success,
            "action": "open_shortcut",
            "target": preset_key.capitalize(),
            "url": url,
            "message": f"🌐 Opened **{preset_key.capitalize()}** in your browser.",
        }

    elif action_type == "open_url":
        success = open_url(target_clean)
        return {
            "success": success,
            "action": "open_url",
            "target": target_clean,
            "url": target_clean,
            "message": f"🔗 Opened **{target_clean}** in your browser.",
        }

    elif action_type == "search_google":
        success, url = search_google(target_clean)
        return {
            "success": success,
            "action": "search_google",
            "target": target_clean,
            "url": url,
            "message": f"🔍 Searching Google for **'{target_clean}'**...",
        }

    elif action_type == "search_youtube":
        success, url = search_youtube(target_clean)
        return {
            "success": success,
            "action": "search_youtube",
            "target": target_clean,
            "url": url,
            "message": f"▶️ Searching YouTube for **'{target_clean}'**...",
        }

    elif action_type == "search_maps":
        success, url = search_google_maps(target_clean)
        return {
            "success": success,
            "action": "search_maps",
            "target": target_clean,
            "url": url,
            "message": f"🗺️ Searching Google Maps for **'{target_clean}'**...",
        }

    return {
        "success": False,
        "action": "unknown",
        "target": target_clean,
        "url": "",
        "message": f"Unknown browser action requested.",
    }
