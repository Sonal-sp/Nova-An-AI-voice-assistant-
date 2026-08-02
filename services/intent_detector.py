import re
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

WEB_KEYWORDS = [
    "latest",
    "today",
    "news",
    "current",
    "weather",
    "stock",
    "price",
    "live",
    "update",
    "recent",
    "headline",
    "who won",
    "score",
    "match",
]


def should_search_web(prompt: str) -> bool:
    """
    Checks if prompt implies live web search intent.
    """
    if not prompt:
        return False
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in WEB_KEYWORDS)


def detect_browser_intent(prompt: str) -> Optional[Dict[str, str]]:
    """
    Detects if the user prompt is a desktop browser command.

    Supported intent forms:
    - Open shortcuts: "open github", "launch gmail", "open chatgpt", "open youtube"
    - Open URL: "open reddit.com", "navigate to https://example.com"
    - YouTube Search: "search youtube for python tutorials"
    - Maps Search: "search maps for coffee near me", "search google maps for pizza"
    - Google Search: "search google for streamlit components"

    Returns
    -------
    Optional[Dict[str, str]]
        Dictionary with 'action_type' and 'target', or None if no browser intent found.
    """
    if not prompt or not prompt.strip():
        return None

    clean_prompt = prompt.strip()

    # 1. YouTube Search
    yt_match = re.search(
        r"(?:search\s+youtube\s+for|youtube\s+search|find\s+on\s+youtube|search\s+on\s+youtube)\s+(.+)",
        clean_prompt,
        re.IGNORECASE,
    )
    if yt_match:
        return {"action_type": "search_youtube", "target": yt_match.group(1).strip()}

    # 2. Google Maps Search
    maps_match = re.search(
        r"(?:search\s+(?:google\s+)?maps\s+for|maps\s+search|find\s+on\s+maps|show\s+on\s+maps)\s+(.+)",
        clean_prompt,
        re.IGNORECASE,
    )
    if maps_match:
        return {"action_type": "search_maps", "target": maps_match.group(1).strip()}

    # 3. Explicit Google Search command
    g_match = re.search(
        r"(?:search\s+google\s+for|google\s+search|search\s+on\s+google)\s+(.+)",
        clean_prompt,
        re.IGNORECASE,
    )
    if g_match:
        return {"action_type": "search_google", "target": g_match.group(1).strip()}

    # 4. Open Presets or URLs ("open github", "launch gmail", "open twitter.com", "go to chatgpt")
    open_match = re.search(
        r"^(?:open|launch|go\s+to|navigate\s+to)\s+([a-zA-Z0-9.\-_:/]+(?:\.[a-zA-Z]{2,})?)$",
        clean_prompt,
        re.IGNORECASE,
    )
    if open_match:
        target = open_match.group(1).strip()
        target_lower = target.lower()

        presets = ["github", "gmail", "chatgpt", "youtube", "google", "maps", "stackoverflow", "linkedin", "reddit"]
        if target_lower in presets:
            return {"action_type": "open_preset", "target": target_lower}

        if "." in target or target_lower.startswith("http"):
            return {"action_type": "open_url", "target": target}

        return {"action_type": "open_preset", "target": target_lower}

    return None