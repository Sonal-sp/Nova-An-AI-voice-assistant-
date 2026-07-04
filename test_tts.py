import asyncio
from services.text_to_speech import text_to_speech

asyncio.run(
    text_to_speech("Hello! I am Nova. Nice to meet you.")
)