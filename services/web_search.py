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

    for i, result in enumerate(results, start=1):

        context += (
            f"Search Result {i}\n"
            f"Title: {result['title']}\n"
            f"Summary: {result['body']}\n"
            f"URL: {result['url']}\n\n"
        )

    return context