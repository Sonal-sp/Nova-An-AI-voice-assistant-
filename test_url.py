from services.url_service import extract_text_from_url

text = extract_text_from_url(
    "https://techcrunch.com/"
)

print(text[:3000])