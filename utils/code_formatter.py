import re


CODE_BLOCK_PATTERN = re.compile(
    r"```(\w+)?\n(.*?)```",
    re.DOTALL,
)


def parse_response(response: str):
    """
    Splits a Gemini response into markdown and code blocks.

    Returns:
    [
        {
            "type": "markdown",
            "content": "..."
        },

        {
            "type": "code",
            "language": "python",
            "content": "print('Hello')"
        }
    ]
    """

    blocks = []

    last_end = 0

    for match in CODE_BLOCK_PATTERN.finditer(response):

        start, end = match.span()

        language = match.group(1) or "text"

        code = match.group(2).strip()

        markdown = response[last_end:start].strip()

        if markdown:

            blocks.append(
                {
                    "type": "markdown",
                    "content": markdown,
                }
            )

        blocks.append(
            {
                "type": "code",
                "language": language,
                "content": code,
            }
        )

        last_end = end

    remaining = response[last_end:].strip()

    if remaining:

        blocks.append(
            {
                "type": "markdown",
                "content": remaining,
            }
        )

    return blocks