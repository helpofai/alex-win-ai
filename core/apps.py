import os
import difflib
import subprocess

class AppManager:
    def __init__(self):
        self.apps = {}
        self.refresh_apps()

    def refresh_apps(self):
        """Scans Start Menu folders for shortcuts."""
        print("[Apps] Indexing installed applications...")
        paths = [
            os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs")
        ]

        self.apps = {}
        # Hardcoded common fallbacks
        self.apps["vlc"] = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
        self.apps["chrome"] = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        
        for path in paths:
            if not os.path.exists(path): continue
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith(".lnk"):
                        name = file.lower().replace(".lnk", "").strip()
                        self.apps[name] = os.path.join(root, file)
        
        print(f"[Apps] Found {len(self.apps)} applications.")

    def open_app(self, app_name):
        app_name = app_name.lower().strip()
        
        # Check if it's a known path already
        if app_name in self.apps and os.path.exists(self.apps[app_name]):
            return self._launch(app_name, self.apps[app_name])
        
        # Fuzzy match
        matches = difflib.get_close_matches(app_name, self.apps.keys(), n=1, cutoff=0.4)
        if matches:
            best_match = matches[0]
            return self._launch(best_match, self.apps[best_match])
            
        return f"I couldn't find an application named '{app_name}'."

    def _launch(self, name, path):
        try:
            os.startfile(path)
            return f"Opening {name}..."
        except Exception as e:
            return f"Failed to open {name}: {e}"

    def get_app_list(self):
        return list(self.apps.keys())
