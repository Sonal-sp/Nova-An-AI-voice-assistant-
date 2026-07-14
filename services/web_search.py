from ddgs import DDGS


def search_web(query, max_results=5):

    with DDGS() as ddgs:

        results = list(
            ddgs.text(
                query,
                max_results=max_results,
            )
        )

    return results


def format_search_results(results):

    context = ""

    for result in results:

        print("=" * 80)
        print(type(result))
        print(result)

        # Convert to a plain dict if needed
        result = dict(result)

        print(result.keys())

        title = result.get("title", "No title")
        body = result.get("body", "No description")
        url = result.get("href", "No URL")

        context += (
            f"Title: {title}\n"
            f"Summary: {body}\n"
            f"URL: {url}\n\n"
        )

    return context