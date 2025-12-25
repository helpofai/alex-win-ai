import cv2
import os
import numpy as np

FACE_DATA = "data/face_model.yml"
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

class FaceEngine:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
        self.is_enrolled = os.path.exists(FACE_DATA)
        if self.is_enrolled:
            self.recognizer.read(FACE_DATA)

    def enroll(self):
        """Captures 30 samples from webcam to train the model."""
        cam = cv2.VideoCapture(0)
        count = 0
        samples = []
        ids = []
        
        print("[Face] Enrollment started. Look at the camera...")
        
        while count < 30:
            ret, img = cam.read()
            if not ret: break
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                samples.append(gray[y:y+h, x:x+w])
                ids.append(1) # User ID 1
                count += 1
                # Show feedback (optional, but good for user)
                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
                cv2.imshow('Face Enrollment - Look at Camera', img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'): break
            
        cam.release()
        cv2.destroyAllWindows()
        
        if samples:
            self.recognizer.train(samples, np.array(ids))
            self.recognizer.write(FACE_DATA)
            self.is_enrolled = True
            return "Face enrollment complete."
        return "Enrollment failed."

    def verify(self):
        """Captures one frame and checks if it matches user 1."""
        if not self.is_enrolled: return True # Fallback if not set
        
        cam = cv2.VideoCapture(0)
        ret, img = cam.read()
        cam.release()
        
        if not ret: return False
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
            # Lower confidence score is better in LBPH (distance)
            print(f"[Face] match score: {confidence}")
            if id == 1 and confidence < 60: # Threshold 60 is usually good
                return True
        return False
