import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # Remove unwanted tags
        for tag in soup(
            [
                "script",
                "style",
                "header",
                "footer",
                "nav",
                "aside",
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        return text

    except Exception as e:

        print(e)

        return None