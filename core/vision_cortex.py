import pyautogui
import pygetwindow as gw
import easyocr
import numpy as np
from PIL import Image
import os

class VisionCortex:
    def __init__(self):
        # Initialize EasyOCR reader (English by default)
        # Note: This will download models on first run (~100MB)
        print("[Vision] Initializing Local OCR Engine...")
        self.reader = easyocr.Reader(['en'], gpu=False) # Set gpu=True if user has CUDA
        print("[Vision] OCR Engine Ready.")

    def get_screen_context(self):
        """Returns a summary of what's currently on screen."""
        try:
            active_win = gw.getActiveWindow()
            cursor_pos = pyautogui.position()
            
            context = {
                "active_window": active_win.title if active_win else "Desktop",
                "window_geometry": {
                    "left": active_win.left, "top": active_win.top,
                    "width": active_win.width, "height": active_win.height
                } if active_win else None,
                "cursor_pos": {"x": cursor_pos.x, "y": cursor_pos.y}
            }
            return context
        except:
            return {"active_window": "Unknown", "cursor_pos": {"x": 0, "y": 0}}

    def ocr_screen(self):
        """Performs OCR on the entire screen and returns a list of text blocks."""
        try:
            screenshot = pyautogui.screenshot()
            # Convert PIL image to numpy array for EasyOCR
            img_np = np.array(screenshot)
            
            # Read text
            results = self.reader.readtext(img_np)
            
            # Format: [{"text": "...", "box": [[x,y], ...], "confidence": 0.9}]
            text_blocks = []
            for (bbox, text, prob) in results:
                text_blocks.append({
                    "text": text,
                    "box": bbox,
                    "confidence": prob
                })
            return text_blocks
        except Exception as e:
            print(f"[Vision] OCR Error: {e}")
            return []

    def find_text_coordinates(self, target_text):
        """Searches for a specific text on screen and returns its center coordinates."""
        blocks = self.ocr_screen()
        if not blocks: return None
        
        target_text = target_text.lower()
        for block in blocks:
            if target_text in block["text"].lower():
                bbox = block["box"]
                x_center = (bbox[0][0] + bbox[1][0]) / 2
                y_center = (bbox[0][1] + bbox[2][1]) / 2
                return [int(x_center), int(y_center)]
        return None

    def verify_text_on_screen(self, target_text):
        """Checks if a specific text is currently visible."""
        blocks = self.ocr_screen()
        target_text = target_text.lower()
        return any(target_text in b["text"].lower() for b in blocks)

    def get_context_string(self):
        ctx = self.get_screen_context()
        labels = self.get_all_ui_labels()
        labels_str = ", ".join(labels[:15]) # Top 15 labels
        return f"Currently focus is on '{ctx['active_window']}'. Visible elements: [{labels_str}]. Cursor at {ctx['cursor_pos']['x']}, {ctx['cursor_pos']['y']}."

    def get_all_ui_labels(self):
        """Returns a list of all text strings currently visible on screen."""
        blocks = self.ocr_screen()
        return [b["text"] for b in blocks if b["confidence"] > 0.5]
