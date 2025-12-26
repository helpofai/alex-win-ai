import pyautogui
import time
import os
import base64
from io import BytesIO

ASSETS_DIR = "assets"

class Automation:
    def __init__(self):
        pyautogui.FAILSAFE = True 
        pyautogui.PAUSE = 0.2

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

    def move_mouse(self, x, y):
        pyautogui.moveTo(x, y, duration=0.3)
        return f"Moved to {x}, {y}"

    def move_relative(self, dx, dy):
        pyautogui.moveRel(dx, dy, duration=0.3)
        return f"Moved by {dx}, {dy}"

    def click_coordinates(self, x, y):
        pyautogui.click(x, y)
        return f"Clicked {x}, {y}"

    def right_click(self):
        pyautogui.rightClick()
        return "Right clicked"

    def drag_and_drop(self, x1, y1, x2, y2):
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, duration=1.0, button='left')
        return f"Dragged from {x1},{y1} to {x2},{y2}"

    def type_text(self, text):
        pyautogui.write(text, interval=0.02)
        return "Typed"

    def press_key(self, key):
        pyautogui.press(key)
        return f"Pressed {key}"

    def hotkey(self, keys):
        if isinstance(keys, str):
            keys = [k.strip() for k in keys.split("+")]
        pyautogui.hotkey(*keys)
        return f"Hotkey {keys}"

    def scroll(self, clicks):
        pyautogui.scroll(clicks)
        return f"Scrolled {clicks}"
