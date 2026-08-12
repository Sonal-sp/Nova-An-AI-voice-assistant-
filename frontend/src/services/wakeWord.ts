// Continuous Web Speech API Wake-Word Engine ("Hey Nova")

export type WakeWordCallback = (transcript: string, wakeWordDetected: boolean) => void;

class WakeWordEngine {
  private recognition: any = null;
  private isListening = false;
  private onResultCallback: WakeWordCallback | null = null;
  private wakeWords = ["hey nova", "listen nova", "ok nova", "hello nova", "hi nova", "nova"];

  constructor() {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = false;
      this.recognition.lang = "en-US";

      this.recognition.onresult = (event: any) => {
        const lastResultIndex = event.results.length - 1;
        const transcript = event.results[lastResultIndex][0].transcript.trim();
        this.processTranscript(transcript);
      };

      this.recognition.onerror = (event: any) => {
        console.warn("Web Speech Recognition Error:", event.error);
        if (this.isListening && event.error !== "aborted") {
          setTimeout(() => this.restart(), 1000);
        }
      };

      this.recognition.onend = () => {
        if (this.isListening) {
          this.restart();
        }
      };
    } else {
      console.warn("Web Speech API is not supported in this browser.");
    }
  }

  private processTranscript(transcript: string) {
    if (!transcript) return;
    const lower = transcript.toLowerCase();
    let wakeWordDetected = false;
    let cleanPrompt = transcript;

    for (const trigger of this.wakeWords) {
      const idx = lower.indexOf(trigger);
      if (idx !== -1) {
        wakeWordDetected = true;
        cleanPrompt = transcript.substring(idx + trigger.length).trim();
        if (!cleanPrompt) cleanPrompt = "Hello Nova";
        break;
      }
    }

    if (this.onResultCallback) {
      this.onResultCallback(cleanPrompt, wakeWordDetected);
    }
  }

  public start(callback: WakeWordCallback) {
    this.onResultCallback = callback;
    this.isListening = true;
    if (this.recognition) {
      try {
        this.recognition.start();
      } catch (e) {
        // Recognition already active
      }
    }
  }

  public stop() {
    this.isListening = false;
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {}
    }
  }

  private restart() {
    if (this.recognition && this.isListening) {
      try {
        this.recognition.start();
      } catch (e) {}
    }
  }

  public getIsSupported(): boolean {
    return !!this.recognition;
  }
}

export const wakeWordEngine = new WakeWordEngine();
