import sys
import threading
import datetime
import keyboard
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTextEdit, QLineEdit, QPushButton, QLabel, 
                               QFrame, QProgressBar, QGraphicsDropShadowEffect, QSystemTrayIcon, QMenu)
from PySide6.QtCore import Qt, Signal, QObject, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QColor, QFont, QIcon, QAction

from gui.styles import DARK_THEME
from gui.widgets import ReactorWidget, AudioBar, SystemStatsWidget
from gui.transparency import ActionPreviewPopup, LiveExecutionPopup, ResultPopup, CriticalConfirmationPopup, Action
from gui.dashboard import MasterDashboard
from core.voice import VoiceEngine
from core.brain import Brain
from core.version import CURRENT_VERSION, check_for_updates

class WorkerSignals(QObject):
    update_log = Signal(str, str)
    status_changed = Signal(str)
    show_preview = Signal(Action)
    show_live = Signal(int, int, str, int)
    show_result = Signal(str)
    show_critical = Signal(str)
    log_tab = Signal(str, str)

class ListenThread(threading.Thread):
    def __init__(self, voice, brain, signals):
        super().__init__()
        self.voice = voice; self.brain = brain; self.signals = signals; self.running = True

    def run(self):
        while self.running:
            if self.voice.mic_available:
                self.signals.status_changed.emit("LISTENING")
                command, audio_raw = self.voice.listen()
                if command or audio_raw is not None:
                    self.signals.status_changed.emit("PROCESSING")
                    if command: self.signals.update_log.emit("User", command)
                    response = self.brain.process_command(command, audio_raw=audio_raw)
                    if response: self.signals.update_log.emit("Alex", response)
                else:
                    self.signals.status_changed.emit("IDLE")
            else:
                self.signals.status_changed.emit("TEXT_MODE")
                threading.Event().wait(1)

class MiniSphere(QWidget):
    """Tiny always-on-top version of Alex."""
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(100, 100)
        
        self.layout = QVBoxLayout(self)
        self.reactor = ReactorWidget(); self.reactor.setFixedSize(80, 80)
        self.layout.addWidget(self.reactor)
        
        self.mouse_pos = None

    def set_state(self, state):
        self.reactor.set_state(state)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton: self.mouse_pos = e.globalPosition().toPoint()
    def mouseMoveEvent(self, e):
        if self.mouse_pos:
            self.move(self.pos() + e.globalPosition().toPoint() - self.mouse_pos)
            self.mouse_pos = e.globalPosition().toPoint()
    def mouseDoubleClickEvent(self, e):
        # Open full UI on double click
        self.parent_window.restore_from_mini()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALEX // COMMAND SPHERE")
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(DARK_THEME)
        
        # Core
        self.voice = VoiceEngine()
        self.signals = WorkerSignals()
        self.brain = Brain(self.voice, ui_signals=self.signals)
        self.dashboard = MasterDashboard()
        self.signals.log_tab.connect(self.dashboard.route_log)

        # Mini Mode Setup
        self.mini_mode = MiniSphere()
        self.mini_mode.parent_window = self

        # UI
        self.main_container = QWidget(); self.main_container.setObjectName("CentralWidget")
        self.setCentralWidget(self.main_container)
        self.main_layout = QVBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(30, 20, 30, 30)

        # --- HEADER ---
        header = QHBoxLayout()
        self.logo_label = QLabel(f"ALEX AGENTIC CORE // v{CURRENT_VERSION}"); self.logo_label.setObjectName("HeaderLabel")
        header.addWidget(self.logo_label); header.addStretch()
        
        # Navigation Buttons
        self.mini_btn = QPushButton("MINI"); self.mini_btn.setFixedSize(60, 30); self.mini_btn.clicked.connect(self.switch_to_mini)
        self.hide_btn = QPushButton("_"); self.hide_btn.setFixedSize(40, 30); self.hide_btn.clicked.connect(self.showMinimized)
        close_btn = QPushButton("✕"); close_btn.setFixedSize(40, 30); close_btn.clicked.connect(self.close)
        
        header.addWidget(self.mini_btn); header.addWidget(self.hide_btn); header.addWidget(close_btn)
        self.main_layout.addLayout(header)

        # --- DASHBOARD ---
        sphere_area = QHBoxLayout()
        self.left_wing = QFrame(); self.left_wing.setObjectName("WingPanel"); self.left_wing.setFixedWidth(250)
        left_layout = QVBoxLayout(self.left_wing); left_layout.addWidget(QLabel("SYSTEM ANALYTICS")); left_layout.addWidget(SystemStatsWidget()); left_layout.addStretch()
        sphere_area.addWidget(self.left_wing)

        center_core = QVBoxLayout()
        self.reactor = ReactorWidget(); shadow = QGraphicsDropShadowEffect(); shadow.setBlurRadius(50); shadow.setColor(QColor(0, 212, 255, 150)); shadow.setOffset(0, 0); self.reactor.setGraphicsEffect(shadow)
        self.audio_bar = AudioBar()
        center_core.addStretch(); center_core.addWidget(self.reactor, 0, Qt.AlignCenter); center_core.addWidget(self.audio_bar, 0, Qt.AlignCenter); center_core.addStretch()
        sphere_area.addLayout(center_core, stretch=2)

        self.right_wing = QFrame(); self.right_wing.setObjectName("WingPanel"); self.right_wing.setFixedWidth(300)
        right_layout = QVBoxLayout(self.right_wing); right_layout.addWidget(QLabel("COMMUNICATIONS")); self.chat_area = QTextEdit(); self.chat_area.setReadOnly(True); right_layout.addWidget(self.chat_area)
        sphere_area.addWidget(self.right_wing)
        self.main_layout.addLayout(sphere_area)

        # --- FOOTER ---
        self.input_field = QLineEdit(); self.input_field.setPlaceholderText("TRANSMIT COMMAND..."); self.input_field.returnPressed.connect(self.handle_text_input)
        self.main_layout.addWidget(self.input_field)

        # Popups...
        self.popup_preview = ActionPreviewPopup(); self.popup_live = LiveExecutionPopup(); self.popup_result = ResultPopup(); self.popup_critical = CriticalConfirmationPopup()
        self.signals.show_preview.connect(self.popup_preview.show_action); self.signals.show_live.connect(self.popup_live.update); self.signals.show_result.connect(lambda m: self.popup_result.show_success(m)); self.signals.show_critical.connect(self.popup_critical.show_critical)
        self.popup_preview.authorized.connect(self.brain.set_auth_result); self.popup_critical.confirmed.connect(self.brain.set_auth_result)

        self.listen_thread = ListenThread(self.voice, self.brain, self.signals); self.listen_thread.daemon = True; self.listen_thread.start()
        self.timer = QTimer(self); self.timer.timeout.connect(self._update_loop); self.timer.start(30)

    def switch_to_mini(self):
        self.hide(); self.mini_mode.show()
    def restore_from_mini(self):
        self.mini_mode.hide(); self.show()

    def _update_loop(self):
        self.audio_bar.set_amplitude(self.voice.current_volume)
        if self.mini_mode.isVisible(): self.mini_mode.set_state(self.reactor.state)

    def handle_text_input(self):
        cmd = self.input_field.text().strip()
        if cmd:
            self.append_chat("User", cmd)
            self.input_field.clear()
            # Run in thread to not freeze UI
            threading.Thread(target=self._process_and_log, args=(cmd,), daemon=True).start()

    def _process_and_log(self, cmd):
        response = self.brain.process_command(cmd)
        if response:
            self.signals.update_log.emit("Alex", response)
    def append_chat(self, s, m):
        c = "#00d4ff" if s == "Alex" else "#fff"
        self.chat_area.append(f"<div style='margin-bottom:10px;'><b>{s.upper()}:</b> {m}</div>")
    def update_state(self, s): self.reactor.set_state(s); self.logo_label.setText(f"ALEX v{CURRENT_VERSION} // {s}")
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton: self.drag_pos = e.globalPosition().toPoint()
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton: self.move(self.pos() + e.globalPosition().toPoint() - self.drag_pos); self.drag_pos = e.globalPosition().toPoint(); e.accept()
