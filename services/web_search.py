from ddgs import DDGS


def search_web(query, max_results=5):
    """
    Search the web using DuckDuckGo.
    Returns formatted search results.
    """

    try:
        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=max_results,
            )

            for result in search_results:

                results.append(
                    {
                        "title": result.get("title", ""),
                        "body": result.get("body", ""),
                        "url": result.get("href", ""),
                    }
                )

        return results

    except Exception as e:

        print("Web Search Error:", e)

        return []