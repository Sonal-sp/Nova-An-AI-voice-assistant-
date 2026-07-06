import os
from dotenv import load_dotenv
from google import genai
import traceback
from config import GEMINI_MODEL, SYSTEM_PROMPT
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(conversation):
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=conversation,
        )

        return response.text

    except Exception as e:
        print(f"Gemini Error: {e}")
        return "⚠️ Sorry, I'm having trouble connecting to Gemini right now."

def transcribe_audio(audio_path: str):
    try:
        audio_file = client.files.upload(file=audio_path)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                """
You are an automatic speech recognition system.

Your task is to produce a COMPLETE VERBATIM transcript.

Rules:
- Return every spoken word.
- Do not summarize.
- Do not omit words.
- Do not paraphrase.
- Return only the transcript.
""",
                audio_file,
            ],
        )

        return response.text

    except Exception as e:
        traceback.print_exc()
        raise


