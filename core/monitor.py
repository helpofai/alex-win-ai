import psutil
import time
import threading
import socket
import pygetwindow as gw

class HealthMonitor(threading.Thread):
    def __init__(self, brain_callback):
        super().__init__()
        self.brain_callback = brain_callback
        self.daemon = True
        self.running = True
        
        # Thresholds
        self.battery_low = 20
        self.cpu_high = 90
        
        # Focus settings
        self.focus_apps = ["visual studio", "vscode", "intellij", "blender", "unity", "game"]
        self.is_focus_mode = False
        
        # State
        self.last_battery_alert = 0
        self.last_internet_status = True

    def run(self):
        print("[Monitor] Background Health Check Active.")
        while self.running:
            try:
                # 0. Focus Check
                active_win = gw.getActiveWindow()
                title = active_win.title.lower() if active_win else ""
                self.is_focus_mode = any(app in title for app in self.focus_apps)

                # 1. Battery Check (Only if not in focus mode)
                battery = psutil.sensors_battery()
                if not self.is_focus_mode:
                    if battery and battery.percent < self.battery_low and not battery.power_plugged:
                        if time.time() - self.last_battery_alert > 1800: # Every 30 mins
                            self.brain_callback(f"ALERT: Battery is low at {battery.percent}%. Please plug in.")
                            self.last_battery_alert = time.time()

                # 2. Internet Check
                internet = self._check_internet()
                if internet != self.last_internet_status:
                    if not internet:
                        self.brain_callback("ALERT: Internet connection lost. Switching to offline mode.")
                    else:
                        self.brain_callback("ALERT: Internet connection restored.")
                    self.last_internet_status = internet

                # 3. CPU Check
                cpu = psutil.cpu_percent()
                if cpu > self.cpu_high:
                    self.brain_callback(f"ALERT: CPU usage is very high at {cpu}%. I'm slowing down.")

            except Exception as e:
                print(f"[Monitor] Error: {e}")
            
            time.sleep(60) # Check every minute

    def _check_internet(self):
        try:
            with socket.create_connection(("8.8.8.8", 53), timeout=3) as sock:
                return True
        except:
            return False

    def stop(self):
        self.running = False