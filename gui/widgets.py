from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QConicalGradient, QRadialGradient
import math
import random

class ReactorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 220)
        
        # Animation State
        self.angle_outer = 0
        self.angle_inner = 0
        self.pulse = 0
        self.pulse_dir = 1
        
        self.color_main = QColor("#00d4ff") # Cyan
        self.color_accent = QColor("#00d4ff") 

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16) # ~60 FPS
        
        self.state = "IDLE"

    def set_state(self, state):
        self.state = state
        if state == "IDLE":
            self.color_main = QColor("#00d4ff") # Cyan
            self.color_accent = QColor("#007acc")
        elif state == "LISTENING":
            self.color_main = QColor("#ff3333") # Red
            self.color_accent = QColor("#ff0000")
        elif state == "PROCESSING":
            self.color_main = QColor("#00ff00") # Green
            self.color_accent = QColor("#33cc33")
        self.update()

    def animate(self):
        # Rotation speeds
        speed_outer = 1 if self.state == "IDLE" else 4
        speed_inner = -2 if self.state == "IDLE" else -8
        
        self.angle_outer = (self.angle_outer + speed_outer) % 360
        self.angle_inner = (self.angle_inner + speed_inner) % 360

        # Pulse logic
        if self.state == "LISTENING":
            if self.pulse >= 20: self.pulse_dir = -1
            elif self.pulse <= 0: self.pulse_dir = 1
            self.pulse += 2 * self.pulse_dir
        else:
            self.pulse = 0 # Steady when not listening
            
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        
        # --- 1. Background Glow (Radial) ---
        radial = QRadialGradient(cx, cy, w/2)
        radial.setColorAt(0, QColor(self.color_main.red(), self.color_main.green(), self.color_main.blue(), 50))
        radial.setColorAt(0.8, Qt.transparent)
        radial.setColorAt(1, Qt.transparent)
        painter.setBrush(QBrush(radial))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, w, h)

        # --- 2. Outer Tech Ring ( segmented ) ---
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle_outer)
        
        pen_outer = QPen(self.color_main, 3)
        pen_outer.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_outer)
        
        radius_outer = 80 + (self.pulse * 0.2)
        for i in range(3):
            painter.rotate(120)
            painter.drawArc(QRectF(-radius_outer, -radius_outer, radius_outer*2, radius_outer*2), 0, 60 * 16)
        
        painter.restore()

        # --- 3. Inner Data Ring (Fast Spinner) ---
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle_inner)
        
        pen_inner = QPen(self.color_accent, 1.5)
        pen_inner.setStyle(Qt.DotLine)
        painter.setPen(pen_inner)
        
        radius_inner = 60 + (self.pulse * 0.5)
        painter.drawEllipse(QRectF(-radius_inner, -radius_inner, radius_inner*2, radius_inner*2))
        
        painter.restore()

        # --- 4. The Core (Nucleus) ---
        painter.save()
        painter.translate(cx, cy)
        core_size = 30 + self.pulse
        core_grad = QRadialGradient(0, 0, core_size)
        core_grad.setColorAt(0, Qt.white)
        core_grad.setColorAt(0.5, self.color_main)
        core_grad.setColorAt(1, Qt.transparent)
        painter.setBrush(QBrush(core_grad))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-core_size, -core_size, core_size*2, core_size*2))
        painter.restore()

class SystemStatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_bar = QProgressBar()
        self.ram_label = QLabel("RAM: 0%")
        self.ram_bar = QProgressBar()
        
        for widget in [self.cpu_label, self.cpu_bar, self.ram_label, self.ram_bar]:
            self.layout.addWidget(widget)
            
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)

    def update_stats(self):
        import psutil
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.cpu_label.setText(f"CPU: {cpu}%")
        self.cpu_bar.setValue(int(cpu))
        self.ram_label.setText(f"RAM: {ram}%")
        self.ram_bar.setValue(int(ram))

class AudioBar(QWidget):
    def __init__(self, color="#00d4ff", parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 40)
        self.amplitude = 0
        self.target_amplitude = 0
        self.color = QColor(color)
        
        # Smooth animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(20)

    def set_amplitude(self, value):
        self.target_amplitude = value

    def animate(self):
        diff = self.target_amplitude - self.amplitude
        self.amplitude += diff * 0.2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        bar_count = 30
        bar_width = (w / bar_count) - 2
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        
        for i in range(bar_count):
            dist_norm = abs(i - (bar_count/2)) / (bar_count/2)
            shape_factor = 1.0 - (dist_norm * dist_norm)
            jitter = 0
            if self.amplitude > 0.05:
                jitter = math.sin(i * 0.5 + self.amplitude * 10) * 0.2
            
            bar_h = h * self.amplitude * shape_factor * (1.0 + jitter)
            bar_h = min(h, max(2, bar_h))

            x = i * (bar_width + 2)
            y = (h - bar_h) / 2
            painter.drawRoundedRect(QRectF(x, y, bar_width, bar_h), 2, 2)