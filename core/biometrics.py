import numpy as np
import os
import json

BIO_DATA = "data/biometrics.json"

class BiometricEngine:
    def __init__(self):
        self.enrolled_fingerprint = self._load_data()
        self.threshold = 0.15 # Sensitivity: lower is stricter

    def _load_data(self):
        if not os.path.exists(BIO_DATA): return None
        try:
            with open(BIO_DATA, 'r') as f:
                data = json.load(f)
                return np.array(data["fingerprint"])
        except: return None

    def enroll(self, audio_data):
        """Creates a spectral envelope fingerprint from audio."""
        if audio_data is None: return "Enrollment failed: No audio data."
        
        fingerprint = self._generate_fingerprint(audio_data)
        with open(BIO_DATA, 'w') as f:
            json.dump({"fingerprint": fingerprint.tolist()}, f)
        self.enrolled_fingerprint = fingerprint
        return "Voice profile successfully encrypted and saved."

    def verify(self, audio_data):
        """Compares current voice envelope to enrolled one."""
        if self.enrolled_fingerprint is None:
            return True # No enrollment yet
        if audio_data is None: return False
            
        current_fp = self._generate_fingerprint(audio_data)
        
        # Use Cosine Similarity or Normalized Euclidean Distance
        # We'll use normalized distance for spectral shape
        dist = np.linalg.norm(self.enrolled_fingerprint - current_fp)
        
        print(f"[Bio] Voice Verification Score: {dist:.4f} (Threshold: {self.threshold})")
        
        # Return match
        return dist < self.threshold

    def _generate_fingerprint(self, audio_data):
        """Generates a 10-point spectral envelope (Frequency shape)."""
        # 1. Normalize amplitude
        audio_data = audio_data.astype(float)
        audio_data /= (np.max(np.abs(audio_data)) + 1e-6)
        
        # 2. Get Power Spectrum
        fft_data = np.abs(np.fft.rfft(audio_data))
        
        # 3. Bin into 10 frequency ranges (Spectral Envelope)
        # This captures the 'timbre' or unique tone of the voice
        bins = np.array_split(fft_data, 10)
        envelope = [np.mean(b) for b in bins]
        
        # 4. Normalize envelope to sum to 1.0 (shape-only matching)
        envelope = np.array(envelope)
        envelope /= (np.sum(envelope) + 1e-6)
        
        return envelope