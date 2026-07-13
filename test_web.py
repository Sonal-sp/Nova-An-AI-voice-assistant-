from services.web_search import search_web

results = search_web("Latest AI news")

for result in results:

    print(result)