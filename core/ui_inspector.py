import uiautomation as auto
import time

class UIInspector:
    def __init__(self):
        # Prevent automation from moving the mouse during scans
        auto.SetGlobalSearchTimeout(2) 

    def get_active_window_text(self):
        """Scrapes text elements from the currently focused window."""
        try:
            window = auto.GetForegroundControl()
            if not window: return "No active window detected."
            
            # Recursive search for all text-bearing elements
            # We filter for common text types to avoid huge dumps
            text_elements = []
            
            def walk(control, depth):
                if depth > 5: return # Limit depth for performance
                
                name = control.Name
                val = getattr(control, 'Value', "")
                
                if name and len(name.strip()) > 1:
                    text_elements.append(name.strip())
                if val and len(val.strip()) > 1:
                    text_elements.append(val.strip())
                
                for child in control.GetChildren():
                    walk(child, depth + 1)

            walk(window, 0)
            
            # De-duplicate and join
            unique_text = list(dict.fromkeys(text_elements))
            return "\n".join(unique_text[:50]) # Top 50 elements for context
        except Exception as e:
            return f"UI Scrape Error: {e}"

    def get_browser_tabs(self):
        """Specialized logic to try and find browser tab titles."""
        try:
            # Look for common browser window patterns
            for proc in ["chrome.exe", "msedge.exe", "firefox.exe"]:
                # This is a simplified version; uiautomation can find the TabBar control
                pass
            return self.get_active_window_text()
        except:
            return ""
