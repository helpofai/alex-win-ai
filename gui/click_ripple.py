from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QPainter, QColor, QPen

class ClickRipple(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(100, 100)
        
        self.radius = 0
        self.opacity = 255
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)

    def trigger(self, x, y):
        self.move(x - 50, y - 50)
        self.radius = 5
        self.opacity = 255
        self.show()
        self.timer.start(16)

    def _animate(self):
        self.radius += 2
        self.opacity -= 10
        if self.opacity <= 0:
            self.timer.stop()
            self.hide()
        self.update()

    def paintEvent(self, event):
        if self.opacity <= 0: return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(0, 212, 255, self.opacity), 3)
        painter.setPen(pen)
        painter.drawEllipse(QPoint(50, 50), self.radius, self.radius)
