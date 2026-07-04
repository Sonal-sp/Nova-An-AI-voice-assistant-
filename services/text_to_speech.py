import edge_tts
from playsound3 import playsound

async def text_to_speech(
    text: str,
    output_file: str = "temp/speech.mp3",
    voice: str = "en-US-AriaNeural",
):
    """
    Convert text into speech and save it as an MP3.

    Args:
        text (str): Text to convert into speech.
        output_file (str): Path where the MP3 will be saved.
        voice (str): Microsoft Edge TTS voice.

    Returns:
        str | None: Path of the generated audio file if successful,
        otherwise None.
    """

    try:
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
        )

        await communicate.save(output_file)
        playsound(output_file)
        return output_file

    except Exception as e:
        print(f"Text-to-Speech Error: {e}")
        return None