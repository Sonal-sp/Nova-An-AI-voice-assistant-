import time
import os
import logging
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

logger = logging.getLogger(__name__)


def record_audio(
    filename="temp/recording.wav",
    duration=6,
    sample_rate=16000,
    silence_threshold=500,
) -> Optional[str]:
    """
    Records audio input from system microphone and saves as 16kHz WAV audio file.

    Parameters
    ----------
    filename : str
        Output WAV file path.
    duration : int
        Maximum recording duration in seconds.
    sample_rate : int
        Audio sample rate in Hz.
    silence_threshold : int
        Amplitude threshold for detecting spoken sound vs silence.

    Returns
    -------
    Optional[str]
        Path to saved recording WAV file or None on error.
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        logger.info(f"Starting audio recording for {duration} seconds...")

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
        )

        sd.wait()

        # Check if recording captured actual speech sound above silence threshold
        max_amplitude = np.max(np.abs(recording)) if len(recording) > 0 else 0
        if max_amplitude < silence_threshold:
            logger.warning(f"Audio recording was quiet or silent (max amplitude: {max_amplitude}).")

        write(filename, sample_rate, recording)
        logger.info(f"Saved audio recording to '{filename}' ({len(recording)} frames).")
        return filename

    except Exception as e:
        logger.error(f"Recording Error: {e}")
        return None