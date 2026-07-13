import re

URL_PATTERN = re.compile(
    r"https?://[^\s]+"
)


def extract_url(text: str):

    match = URL_PATTERN.search(text)

    if match:
        return match.group()

    return None