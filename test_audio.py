from services.speech_to_text import record_audio
from services.gemini_service import transcribe_audio

audio_path = record_audio()

print("Uploading to Gemini...")

text = transcribe_audio(audio_path)

print()
print("Transcript:")
print(text)