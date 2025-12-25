import pyautogui
import time
import os
import base64
from io import BytesIO

ASSETS_DIR = "assets"

class Automation:
    def __init__(self):
        pyautogui.FAILSAFE = True 
        pyautogui.PAUSE = 0.3

    def capture_screen_base64(self):
        try:
            screenshot = pyautogui.screenshot()
            width, height = screenshot.size
            if width > 1024:
                ratio = 1024 / width
                new_height = int(height * ratio)
                screenshot = screenshot.resize((1024, new_height))
            buffered = BytesIO()
            screenshot.save(buffered, format="JPEG", quality=80)
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{img_str}"
        except: return None

    def click_icon(self, icon_name):
        icon_path = os.path.join(ASSETS_DIR, f"{icon_name}.png")
        if not os.path.exists(icon_path):
            return f"Error: No image for '{icon_name}'."
        try:
            location = pyautogui.locateOnScreen(icon_path, confidence=0.8)
            if location:
                center = pyautogui.center(location)
                pyautogui.click(center)
                return f"Clicked {icon_name}."
            return f"Could not see {icon_name}."
        except Exception as e: return str(e)

    def click_coordinates(self, x, y):
        pyautogui.click(x, y)
        return f"Clicked {x}, {y}"

    def right_click(self):
        pyautogui.rightClick()
        return "Right clicked."

    def drag_to(self, x, y):
        pyautogui.dragTo(x, y, duration=1.0)
        return f"Dragged to {x}, {y}"

    def type_text(self, text):
        pyautogui.write(text, interval=0.02)
        return "Typed."

    def press_key(self, key):
        pyautogui.press(key)
        return f"Pressed {key}"

    def hotkey(self, keys):
        """Supports 'ctrl', 'c' or ['ctrl', 'alt', 'del']"""
        if isinstance(keys, str):
            keys = [k.strip() for k in keys.split("+")]
        pyautogui.hotkey(*keys)
        return f"Executed hotkey: {'+'.join(keys)}"