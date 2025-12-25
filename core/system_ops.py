import ctypes
import pygetwindow as gw
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import pyperclip
import pyautogui
import os

class SystemController:
    def __init__(self):
        pass

    def set_volume(self, level):
        """Sets system volume (0 to 100)."""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            return f"Volume set to {level}%"
        except: return "Failed to set volume."

    def set_brightness(self, level):
        """Sets screen brightness (0 to 100)."""
        try:
            sbc.set_brightness(level)
            return f"Brightness set to {level}%"
        except: return "Failed to set brightness."

    def manage_window(self, app_name, action):
        """action: minimize, maximize, close, focus"""
        try:
            windows = gw.getWindowsWithTitle(app_name)
            if not windows: return f"Window '{app_name}' not found."
            win = windows[0]
            if action == "minimize": win.minimize()
            elif action == "maximize": win.maximize()
            elif action == "close": win.close()
            elif action == "focus": win.activate()
            return f"Performed {action} on {app_name}."
        except: return "Window operation failed."

    def clipboard_copy(self, text):
        pyperclip.copy(text)
        return "Copied to clipboard."

    def clipboard_paste(self):
        return pyperclip.paste()

    def take_screenshot(self, name="screenshot"):
        path = f"data/{name}.png"
        pyautogui.screenshot(path)
        return f"Screenshot saved to {path}."

    def lock_pc(self):
        ctypes.windll.user32.LockWorkStation()
        return "PC Locked."

    def media_control(self, action):
        """action: playpause, nexttrack, prevtrack"""
        try:
            pyautogui.press(action)
            return f"Executed media {action}."
        except: return "Media control failed."

    def open_url(self, url):
        import webbrowser
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opening {url}..."

    def close_app(self, app_name):
        import psutil
        try:
            for proc in psutil.process_iter(['name']):
                if app_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    return f"Terminated {proc.info['name']}."
            return f"No process found matching '{app_name}'."
        except: return "Failed to close app."
