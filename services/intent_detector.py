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


def should_search_web(prompt: str):

    prompt = prompt.lower()

    return any(
        keyword in prompt
        for keyword in WEB_KEYWORDS
    )