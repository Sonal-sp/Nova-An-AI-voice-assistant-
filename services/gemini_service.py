import os
import logging
from typing import List, Any, Optional
from dotenv import load_dotenv
from google import genai
import traceback
from PIL import Image

from config import GEMINI_MODEL, SYSTEM_PROMPT
from utils.settings import get_setting

load_dotenv()
logger = logging.getLogger(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(conversation: List[Any]) -> str:
    """
    Sends conversational messages to Gemini model using dynamic settings for model and temperature.
    """
    try:
        model_name = get_setting("default_model", GEMINI_MODEL)
        temperature = float(get_setting("temperature", 0.7))

        response = client.models.generate_content(
            model=model_name,
            contents=conversation,
            config=genai.types.GenerateContentConfig(
                temperature=temperature,
            ),
        )
        return response.text

    except Exception as e:
        logger.error(f"Gemini Error: {e}")
        return "⚠️ Sorry, I'm having trouble connecting to Gemini right now."


def ask_gemini_vision(image: Image.Image, prompt: str) -> str:
    """
    Sends a PIL Image object and prompt to Gemini Multimodal Vision API.
    """
    try:
        model_name = get_setting("default_model", GEMINI_MODEL)
        user_prompt = prompt.strip() if prompt else "Describe and analyze this image in detail."
        response = client.models.generate_content(
            model=model_name,
            contents=[image, user_prompt],
        )
        return response.text

    except Exception as e:
        logger.error(f"Gemini Vision Error: {e}")
        return f"⚠️ Vision AI error: {e}"


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes speech from audio file.
    """
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


def handle_gemini_error(e: Exception) -> str:
    """
    Formats user-friendly error messages for Gemini API exceptions.
    """
    message = str(e)
    if "429" in message:
        return "⚠️ Nova has reached the Gemini API quota.\n\nPlease wait a minute and try again."
    if "401" in message:
        return "⚠️ Invalid Gemini API Key."
    if "403" in message:
        return "⚠️ Permission denied."
    if "timeout" in message.lower():
        return "🌐 Network timeout."
    return "⚠️ Something went wrong."
