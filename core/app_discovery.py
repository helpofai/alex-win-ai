import os
import json
import subprocess
import threading

class AppDiscovery:
    def __init__(self, registry_path="data/app_registry.json"):
        self.registry_path = registry_path
        self.apps = {}
        self.load_registry()

    def load_registry(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                self.apps = json.load(f)

    def save_registry(self):
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.apps, f, indent=2)

    def full_scan(self):
        """Orchestrates all scan methods."""
        print("[AppDiscovery] Deep scan initiated...")
        self._scan_start_menu()
        self._scan_uwp_apps()
        self.save_registry()
        print(f"[AppDiscovery] Scan complete. Found {len(self.apps)} unique entry points.")

    def _scan_start_menu(self):
        """Scans .lnk files from global and user start menus."""
        paths = [
            os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs")
        ]
        
        for p in paths:
            if not os.path.exists(p): continue
            for root, _, files in os.walk(p):
                for f in files:
                    if f.lower().endswith(".lnk"):
                        name = f[:-4].lower()
                        full_path = os.path.join(root, f)
                        self.apps[name] = {
                            "name": f[:-4],
                            "type": "shortcut",
                            "path": full_path,
                            "category": self._guess_category(name)
                        }

    def _scan_uwp_apps(self):
        """Uses PowerShell to get Microsoft Store / UWP apps."""
        try:
            # Command to get PackageFamilyName and DisplayName
            cmd = 'PowerShell "Get-AppxPackage | Select Name, PackageFamilyName"'
            res = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
            
            lines = res.split('\r\n')
            for line in lines:
                if "  " in line:
                    parts = [p.strip() for p in line.split("  ") if p.strip()]
                    if len(parts) >= 2:
                        name = parts[0].lower()
                        family_name = parts[1]
                        # We don't have the exact AppUserModelID here without deeper lookup,
                        # but we can often launch via family name or explorer shell:AppsFolder
                        self.apps[name] = {
                            "name": parts[0],
                            "type": "uwp",
                            "identity": family_name,
                            "path": rf"shell:AppsFolder\{family_name}!App", # Approximate
                            "category": self._guess_category(name)
                        }
        except Exception as e:
            print(f"[AppDiscovery] UWP Scan Error: {e}")

    def _guess_category(self, name):
        name = name.lower()
        if any(x in name for x in ["music", "player", "spotify", "vlc", "groove"]): return "music"
        if any(x in name for x in ["chrome", "edge", "firefox", "browser"]): return "browser"
        if any(x in name for x in ["code", "notep", "studio", "sublime"]): return "editor"
        return "general"

    def find_app(self, query):
        """Intelligent lookup: by name, category, or type."""
        query = query.lower().strip()
        
        # 1. Direct Name Match
        if query in self.apps: return self.apps[query]
        
        # 2. Category Match (e.g. "open music player")
        if "player" in query or "music" in query:
            for app in self.apps.values():
                if app["category"] == "music": return app
                
        # 3. Fuzzy search
        import difflib
        matches = difflib.get_close_matches(query, self.apps.keys(), n=1, cutoff=0.5)
        if matches: return self.apps[matches[0]]
        
        return None

    def get_app_summary(self):
        """Returns a concise string of available apps for AI context."""
        summary = {}
        for app in self.apps.values():
            cat = app.get("category", "general")
            if cat not in summary: summary[cat] = []
            if len(summary[cat]) < 10: # Cap at 10 per category to save tokens
                summary[cat].append(app["name"])
        
        lines = []
        for cat, names in summary.items():
            lines.append(f"- {cat.upper()}: {', '.join(names)}")
        return "\n".join(lines)
