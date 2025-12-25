from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QColor, QFont

class ActionHUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # UI
        self.layout = QVBoxLayout(self)
        self.container = QWidget()
        self.container.setStyleSheet("""
            background-color: rgba(20, 20, 20, 230);
            border: 2px solid #00d4ff;
            border-radius: 15px;
        """)
        self.container_layout = QVBoxLayout(self.container)
        
        self.label = QLabel("SYSTEM INITIALIZING...")
        self.label.setStyleSheet("color: #00d4ff; font-weight: bold; font-size: 14px; padding: 10px;")
        self.container_layout.addWidget(self.label)
        
        self.layout.addWidget(self.container)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 212, 255, 150))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

        self.resize(300, 80)
        
        # Hide Timer
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.fade_out)

    def show_task(self, text):
        self.label.setText(f"TASK: {text.upper()}")
        self.show()
        # Move to bottom right
        screen = self.screen().availableGeometry()
        self.move(screen.width() - self.width() - 20, screen.height() - self.height() - 50)
        
        self.setWindowOpacity(1.0)
        self.hide_timer.start(3000) # Show for 3 seconds

    def fade_out(self):
        self.hide_timer.stop()
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.hide)
        self.anim.start()
