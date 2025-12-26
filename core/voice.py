import speech_recognition as sr
import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
import scipy.io.wavfile as wav
import os
import tempfile
import time
import queue
import asyncio
import edge_tts
import pyttsx3
import uuid
import json
import zipfile
import requests
from vosk import Model, KaldiRecognizer

class VoiceEngine:
    def __init__(self):
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.loop = asyncio.new_event_loop()
        
        # Offline TTS Fallback
        self.offline_engine = pyttsx3.init()
        self.offline_engine.setProperty('rate', 160)
        
        # Local STT (Vosk)
        self.model_path = "data/vosk-model-small-en-us-0.15"
        self._ensure_vosk_model()
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        
        threading.Thread(target=self._speech_handler, args=(self.loop,), daemon=True).start()

        self.mic_available = True
        self.current_volume = 0.0 
        self.is_listening = False
        print("[Voice] Local Independent Voice Engine Online.")

    def _ensure_vosk_model(self):
        """Auto-downloads a small Vosk model if missing."""
        if not os.path.exists(self.model_path):
            print("[Voice] Downloading local STT model (one-time setup)...")
            url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
            os.makedirs("data", exist_ok=True)
            zip_path = "data/model.zip"
            
            response = requests.get(url, stream=True)
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk: f.write(chunk)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("data")
            os.remove(zip_path)
            print("[Voice] Local model installed.")

    def _speech_handler(self, loop):
        asyncio.set_event_loop(loop)
        VOICE = "en-US-GuyNeural" 
        while True:
            text = self.speech_queue.get()
            if text is None: break
            self.is_speaking = True
            try:
                unique_filename = f"speech_{uuid.uuid4().hex}.mp3"
                tmp_file = os.path.join(tempfile.gettempdir(), unique_filename)
                loop.run_until_complete(edge_tts.Communicate(text, VOICE).save(tmp_file))
                
                data, fs = sf.read(tmp_file)
                event = threading.Event()
                def callback(outdata, frames, time, status):
                    chunk_size = len(outdata)
                    if len(data) > current_frame[0]:
                        chunk = data[current_frame[0]:current_frame[0]+chunk_size]
                        if len(chunk.shape) == 1: chunk = np.repeat(chunk[:, np.newaxis], outdata.shape[1], axis=1)
                        outdata[:] = chunk
                        current_frame[0] += chunk_size
                    else:
                        outdata.fill(0); event.set()
                current_frame = [0]
                with sd.OutputStream(samplerate=fs, channels=data.shape[1] if len(data.shape) > 1 else 1, callback=callback):
                    while not event.is_set():
                        self.current_volume = 0.5 + (np.random.rand() * 0.2); time.sleep(0.05)
                    event.wait()
                if os.path.exists(tmp_file): os.remove(tmp_file)
            except:
                self.offline_engine.say(text); self.offline_engine.runAndWait()
            finally:
                self.is_speaking = False; self.current_volume = 0.0; self.speech_queue.task_done()

    def speak(self, text):
        print(f"AI: {text}"); self.speech_queue.put(text)

    def listen(self):
        """100% Local Listening using Vosk."""
        try:
            fs = 16000
            print("Listening...")
            self.is_listening = True
            recorded_frames = []
            
            def callback(indata, frames, time, status):
                recorded_frames.append(indata.copy())
                self.current_volume = np.linalg.norm(indata) / 1000

            with sd.InputStream(samplerate=fs, channels=1, dtype='int16', callback=callback):
                # We record in chunks and check for speech locally
                start_time = time.time()
                while time.time() - start_time < 5: # 5s timeout
                    sd.sleep(100)
            
            self.is_listening = False; self.current_volume = 0.0
            if not recorded_frames: return None, None
            
            full_audio = np.concatenate(recorded_frames, axis=0)
            # Process via Vosk
            if self.recognizer.AcceptWaveform(full_audio.tobytes()):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "")
                if text: print(f"User: {text}"); return text, full_audio
            else:
                result = json.loads(self.recognizer.PartialResult())
                text = result.get("partial", "")
                if text: print(f"User (partial): {text}"); return text, full_audio
                
            return None, None
        except Exception as e:
            print(f"STT Error: {e}"); self.is_listening = False; return None, None