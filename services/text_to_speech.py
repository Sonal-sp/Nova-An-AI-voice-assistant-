import logging
from typing import Optional
import edge_tts
from utils.settings import get_setting

logger = logging.getLogger(__name__)


async def text_to_speech(
    text: str,
    output_file: str = "temp/speech.mp3",
    voice: str = None,
) -> Optional[str]:
    """
    Convert text into speech and save it as an MP3 using dynamic settings.

    Args:
        text (str): Text to convert into speech.
        output_file (str): Path where the MP3 will be saved.
        voice (str): Optional voice override.

    Returns:
        Optional[str]: Path of the generated audio file if successful, otherwise None.
    """
    try:
        # Determine voice from settings if not explicitly provided
        if not voice:
            gender = get_setting("voice_gender", "Female")
            voice = "en-US-GuyNeural" if gender == "Male" else "en-US-AriaNeural"

        # Calculate rate adjustment from speed setting (1.0 = +0%, 1.5 = +50%, 0.8 = -20%)
        speed = float(get_setting("voice_speed", 1.0))
        pct_change = int((speed - 1.0) * 100)
        rate_str = f"+{pct_change}%" if pct_change >= 0 else f"{pct_change}%"

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate_str,
        )

        await communicate.save(output_file)

        # Attempt optional audio playback if audio drivers are present
        try:
            from playsound3 import playsound
            playsound(output_file)
        except Exception as play_err:
            logger.debug(f"Audio playback skipped: {play_err}")

        logger.info(f"TTS generated speech with voice='{voice}', rate='{rate_str}'.")
        return output_file

    except Exception as e:
        logger.error(f"Text-to-Speech Error: {e}")
        return None