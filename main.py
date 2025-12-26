import sys
import os
import ctypes

# 1. Force the highest level of DPI awareness via Windows API immediately
# This must happen before ANY other imports.
try:
    # Set Per Monitor V2 (Context-based)
    # -4 is the handle for DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
    ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)
except Exception:
    try:
        # Fallback to older Per Monitor Awareness
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            # Final fallback to System Awareness
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# 2. Prevent Qt from throwing warnings when it finds the awareness already set
os.environ["QT_LOGGING_RULES"] = "qt.qpa.window=false"

# 3. Standard Qt Environment Variables
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PySide6.QtWidgets import QApplication

def main():
    # 4. Initialize QApplication BEFORE importing the rest of the project
    # This locks in the DPI awareness for all subsequent imports (like pyautogui)
    app = QApplication(sys.argv)
    
    # Delayed import of MainWindow to ensure it uses the established app context
    from gui.main_window import MainWindow
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()