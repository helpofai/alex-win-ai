from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTextEdit, QLabel, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor

class DashboardTab(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 100);
                color: #00ffaa;
                border: none;
                font-family: 'Consolas';
                font-size: 13px;
                padding: 10px;
            }
        """)

class MasterDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(800, 500)
        
        self.layout = QVBoxLayout(self)
        self.container = QFrame()
        self.container.setStyleSheet("""
            background-color: rgba(10, 15, 25, 240);
            border: 1px solid #00d4ff;
            border-radius: 15px;
        """)
        self.container_layout = QVBoxLayout(self.container)
        
        # Header
        self.header = QLabel("ALEX AGENTIC DATA CENTER // v4.0")
        self.header.setStyleSheet("color: #00d4ff; font-weight: bold; font-size: 10px; letter-spacing: 3px; padding: 5px;")
        self.container_layout.addWidget(self.header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #333; background: transparent; }
            QTabBar::tab { background: #1a1a1a; color: #666; padding: 12px 20px; font-weight: bold; }
            QTabBar::tab:selected { background: #00d4ff; color: #000; }
        """)
        
        # Specialist Tabs
        self.tab_activity = DashboardTab()
        self.tab_files = DashboardTab()
        self.tab_browser = DashboardTab()
        self.tab_debugger = DashboardTab()
        self.tab_network = DashboardTab()
        self.tab_learning = DashboardTab()
        
        self.tabs.addTab(self.tab_activity, "ACTIVITY")
        self.tabs.addTab(self.tab_files, "FILES")
        self.tabs.addTab(self.tab_browser, "BROWSER")
        self.tabs.addTab(self.tab_debugger, "DEBUGGER")
        self.tabs.addTab(self.tab_network, "NETWORK")
        self.tabs.addTab(self.tab_learning, "MEMORY")
        
        self.container_layout.addWidget(self.tabs)
        self.layout.addWidget(self.container)
        
        # Auto-Close Timer
        self.close_timer = QTimer()
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(self._fade_out)

    def route_log(self, category, text):
        tab_map = {
            "activity": self.tab_activity,
            "files": self.tab_files,
            "browser": self.tab_browser,
            "debugger": self.tab_debugger,
            "network": self.tab_network,
            "learning": self.tab_learning
        }
        
        target_tab = tab_map.get(category, self.tab_activity)
        target_tab.append(f"<span style='color:#00ffaa'>></span> {text}")
        
        # Switch to the active tab
        index = self.tabs.indexOf(target_tab)
        self.tabs.setCurrentIndex(index)
        
        self._fade_in()
        self.close_timer.start(10000) # 10 seconds

    def _fade_in(self):
        if not self.isVisible():
            self.show()
            self.setWindowOpacity(0.0)
            self.anim = QPropertyAnimation(self, b"windowOpacity")
            self.anim.setDuration(300)
            self.anim.setStartValue(0.0)
            self.anim.setEndValue(1.0)
            self.anim.start()

    def _fade_out(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.hide)
        self.anim.start()