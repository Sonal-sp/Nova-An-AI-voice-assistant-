import time
import sounddevice as sd
from scipy.io.wavfile import write


def record_audio(
    filename="temp/recording.wav",
    duration=8,
    sample_rate=16000,
):
    try:
        print("🎤 Recording starts in seconds...")
        time.sleep(0)

        print("🎤 Speak now!")

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
        )

        sd.wait()

        write(filename, sample_rate, recording)

        print("✅ Recording complete!")

        return filename

    except Exception as e:
        print(f"Recording Error: {e}")
        return None