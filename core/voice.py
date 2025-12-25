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

class VoiceEngine:
    def __init__(self):
        # Initialize TTS with a queue for thread safety
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.loop = asyncio.new_event_loop()
        
        # Initialize Offline Engine (Fallback)
        self.offline_engine = pyttsx3.init()
        self.offline_engine.setProperty('rate', 160)
        self.offline_engine.setProperty('volume', 1.0)
        
        # Initialize TTS Engine in its own thread
        threading.Thread(target=self._speech_handler, args=(self.loop,), daemon=True).start()

        self.recognizer = sr.Recognizer()
        # Improve Listening
        self.recognizer.energy_threshold = 300 
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.6 
        
        self.mic_available = True
        self.current_volume = 0.0 
        self.is_listening = False
        print("[Voice] Voice System Initialized (Edge TTS + Offline Fallback).")

    def _speech_handler(self, loop):
        """Worker thread to handle speech and non-verbal tags using Edge TTS."""
        asyncio.set_event_loop(loop)
        VOICE = "en-US-GuyNeural" 
        
        REACTION_TAGS = [
            "(laughs)", "(clears throat)", "(sighs)", "(gasps)", "(coughs)",
            "(singing)", "(sings)", "(mumbles)", "(beep)", "(groans)",
            "(sniffs)", "(claps)", "(screams)", "(inhales)", "(exhales)",
            "(applause)", "(burps)", "(humming)", "(sneezes)", "(chuckle)", "(whistles)"
        ]

        while True:
            full_text = self.speech_queue.get()
            if full_text is None: break
            
            self.is_speaking = True
            import re
            # Split by tags but keep the tags in the list
            parts = re.split(r'(\(.*?\))', full_text)
            
            for part in parts:
                if not part: continue
                
                if part in REACTION_TAGS:
                    # 1. Play Sound Effect if exists
                    tag_name = part.strip("()")
                    sound_path = f"assets/sounds/{tag_name}.wav"
                    if os.path.exists(sound_path):
                        self._play_wav(sound_path)
                    else:
                        print(f"[Voice] Tag detected but no sound file at: {sound_path}")
                else:
                    # 2. Speak the text part
                    clean_text = self._clean_text_for_speech(part)
                    if clean_text:
                        self._speak_online_or_offline(clean_text, VOICE, loop)

            self.is_speaking = False
            self.current_volume = 0.0
            self.speech_queue.task_done()

    def _speak_online_or_offline(self, clean_text, VOICE, loop):
        """Handles the actual audio generation and playback."""
        try:
            # Attempt Edge TTS (Online)
            unique_filename = f"speech_{uuid.uuid4().hex}.mp3"
            tmp_file = os.path.join(tempfile.gettempdir(), unique_filename)
            
            loop.run_until_complete(self._generate_audio(clean_text, VOICE, tmp_file))
            
            data, fs = sf.read(tmp_file)
            event = threading.Event()
            
            def callback(outdata, frames, time, status):
                chunk_size = len(outdata)
                channels = outdata.shape[1] if len(outdata.shape) > 1 else 1
                
                if len(data) > current_frame[0]:
                    chunk = data[current_frame[0]:current_frame[0]+chunk_size]
                    
                    # Ensure chunk has same number of dimensions as outdata
                    if channels > 1 and len(chunk.shape) == 1:
                        chunk = np.repeat(chunk[:, np.newaxis], channels, axis=1)
                    elif channels == 1 and len(chunk.shape) > 1:
                        chunk = chunk[:, 0] # Take first channel
                    
                    if len(chunk) < chunk_size:
                        outdata[:len(chunk)] = chunk.reshape(outdata[:len(chunk)].shape)
                        outdata[len(chunk):] = 0
                        event.set()
                    else:
                        outdata[:] = chunk.reshape(outdata.shape)
                    current_frame[0] += chunk_size
                else:
                    outdata.fill(0)
                    event.set()

            current_frame = [0]
            with sd.OutputStream(samplerate=fs, channels=data.shape[1] if len(data.shape) > 1 else 1, callback=callback):
                while not event.is_set():
                    self.current_volume = 0.5 + (np.random.rand() * 0.3)
                    time.sleep(0.05)
                event.wait()
            
            time.sleep(0.1)
            if os.path.exists(tmp_file): os.remove(tmp_file)

        except Exception as e:
            # Fallback to pyttsx3 (Offline)
            print(f"[Voice] Edge TTS failed ({e}). Using Offline Fallback.")
            try:
                self.current_volume = 0.6
                self.offline_engine.say(clean_text)
                self.offline_engine.runAndWait()
            except Exception as offline_e:
                print(f"[Voice] All TTS systems failed: {offline_e}")
            finally:
                self.current_volume = 0.0

    async def _generate_audio(self, text, voice, output_file):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    def _play_wav(self, file_path):
        """Plays a WAV sound effect."""
        try:
            data, fs = sf.read(file_path)
            sd.play(data, fs)
            self.current_volume = 0.7
            sd.wait()
            self.current_volume = 0.0
        except Exception as e:
            print(f"Error playing reaction sound: {e}")

    def _clean_text_for_speech(self, text):
        import re
        text = text.replace("*", "").replace("#", "")
        text = re.sub(r'```.*?```', 'code block skipped', text, flags=re.DOTALL)
        # Remove tags that might have leaked into text parts
        text = re.sub(r'\(.*?\)', '', text)
        return text.strip()

    def speak(self, text):
        """Adds text to the speech queue."""
        print(f"AI: {text}")
        self.speech_queue.put(text)

    def listen(self):
        try:
            fs = 16000
            duration = 5 
            print("Listening...")
            self.is_listening = True
            recorded_frames = []
            
            def callback(indata, frames, time, status):
                recorded_frames.append(indata.copy())
                vol = np.linalg.norm(indata) / 1000
                self.current_volume = min(1.0, vol)

            with sd.InputStream(samplerate=fs, channels=1, dtype='int16', callback=callback):
                sd.sleep(int(duration * 1000))
            
            self.is_listening = False
            self.current_volume = 0.0
            
            if not recorded_frames: return None
            recording = np.concatenate(recorded_frames, axis=0)

            tmp_path = None
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                tmp_path = tmp_wav.name
                wav.write(tmp_path, fs, recording)

            command = None
            if os.path.exists(tmp_path):
                with sr.AudioFile(tmp_path) as source:
                    audio_data = self.recognizer.record(source)
                    try:
                        command = self.recognizer.recognize_google(audio_data)
                        print(f"User: {command}")
                    except: pass
                
                try: os.remove(tmp_path)
                except: pass
            
            return command.lower() if command else None, recording

        except Exception as e:
            print(f"Listen Error: {e}")
            self.is_listening = False
        return None, None
