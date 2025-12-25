import sys
import threading
import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTextEdit, QLineEdit, QPushButton, QLabel, 
                               QFrame, QProgressBar)
from PySide6.QtCore import Qt, Signal, QObject, QTimer
from PySide6.QtGui import QColor, QFont

from gui.styles import DARK_THEME
from gui.widgets import ReactorWidget, AudioBar, SystemStatsWidget
from gui.transparency import ActionPreviewPopup, LiveExecutionPopup, ResultPopup, CriticalConfirmationPopup, Action
from core.voice import VoiceEngine
from core.brain import Brain

class WorkerSignals(QObject):
    update_log = Signal(str, str)
    status_changed = Signal(str)
    # Transparency Signals
    show_preview = Signal(Action)
    show_live = Signal(int, int, str, int) # step, total, desc, progress
    show_result = Signal(str)
    show_critical = Signal(str)

class ListenThread(threading.Thread):
    def __init__(self, voice, brain, signals):
        super().__init__()
        self.voice = voice
        self.brain = brain
        self.signals = signals
        self.running = True

    def run(self):
        while self.running:
            if self.voice.mic_available:
                self.signals.status_changed.emit("LISTENING")
                command, audio_raw = self.voice.listen()
                
                if command or audio_raw is not None:
                    self.signals.status_changed.emit("PROCESSING")
                    if command: self.signals.update_log.emit("User", command)
                    response = self.brain.process_command(command, audio_raw=audio_raw)
                    if response:
                        self.signals.update_log.emit("Alex", response)
                else:
                    self.signals.status_changed.emit("IDLE")
            else:
                self.signals.status_changed.emit("TEXT_MODE")
                threading.Event().wait(1)

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALEX | CORE COMMAND")
        self.resize(1100, 750)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(DARK_THEME)
        
        # 1. Signals & Core
        self.voice = VoiceEngine()
        self.signals = WorkerSignals()
        self.brain = Brain(self.voice, ui_signals=self.signals, task_callback=self.show_live_single)
        self.signals.update_log.connect(self.append_chat)
        self.signals.status_changed.connect(self.update_state)

        # 2. Popups
        self.popup_preview = ActionPreviewPopup()
        self.popup_live = LiveExecutionPopup()
        self.popup_result = ResultPopup()
        self.popup_critical = CriticalConfirmationPopup()
        
        # Connections
        self.signals.show_preview.connect(self.popup_preview.show_action)
        self.signals.show_live.connect(self.popup_live.update)
        self.signals.show_result.connect(self._handle_result)
        self.signals.show_critical.connect(self.popup_critical.show_critical)
        
        self.popup_preview.authorized.connect(self._handle_auth)
        self.popup_critical.confirmed.connect(self._handle_auth)

        # UI Setup (The Cockpit)
        self.main_container = QWidget(); self.main_container.setObjectName("CentralWidget")
        self.setCentralWidget(self.main_container)
        self.main_layout = QVBoxLayout(self.main_container)

        # --- Dashboard ---
        header = QHBoxLayout()
        self.logo_label = QLabel("ALEX v4.0 // AGENTIC CORE"); self.logo_label.setObjectName("StatusLabel")
        header.addWidget(self.logo_label); header.addStretch(); 
        close_btn = QPushButton("✕"); close_btn.setFixedSize(30, 30); close_btn.clicked.connect(self.close); header.addWidget(close_btn)
        self.main_layout.addLayout(header)

        dashboard = QHBoxLayout()
        # Left Vitals
        side = QVBoxLayout(); side.addWidget(QLabel("SYSTEM VITALS")); side.addWidget(SystemStatsWidget()); side.addStretch()
        dashboard.addLayout(side)
        # Center Core
        center = QVBoxLayout(); self.reactor = ReactorWidget(); self.audio_bar = AudioBar(); center.addWidget(self.reactor, 0, Qt.AlignCenter); center.addWidget(self.audio_bar, 0, Qt.AlignCenter)
        dashboard.addLayout(center, stretch=2)
        # Right Chat
        self.chat_area = QTextEdit(); self.chat_area.setReadOnly(True); dashboard.addWidget(self.chat_area, stretch=1)
        self.main_layout.addLayout(dashboard)

        # Footer
        footer = QHBoxLayout(); self.input_field = QLineEdit(); self.input_field.setPlaceholderText("ENTER COMMAND..."); self.input_field.returnPressed.connect(self.handle_text_input)
        footer.addWidget(self.input_field); self.main_layout.addLayout(footer)

        # AI Thread
        self.listen_thread = ListenThread(self.voice, self.brain, self.signals); self.listen_thread.daemon = True; self.listen_thread.start()
        
        self.audio_timer = QTimer(self); self.audio_timer.timeout.connect(self.update_audio); self.audio_timer.start(30)

    def _handle_auth(self, val):
        self.popup_preview.hide(); self.popup_critical.hide()
        self.brain.set_auth_result(val)

    def _handle_result(self, msg):
        self.popup_live.hide(); self.popup_result.show_success(msg)

    def show_live_single(self, text):
        self.popup_live.update(1, 1, text, 100)

    def update_audio(self):
        self.audio_bar.set_amplitude(self.voice.current_volume)

    def handle_text_input(self):
        cmd = self.input_field.text().strip()
        if cmd: self.append_chat("User", cmd); self.input_field.clear(); threading.Thread(target=self.brain.process_command, args=(cmd,), daemon=True).start()

    def append_chat(self, sender, message):
        color = "#00d4ff" if sender == "Alex" else "#fff"
        self.chat_area.append(f"<b style='color:{color}'>{sender}:</b> {message}")

    def update_state(self, status):
        self.reactor.set_state(status)
        self.logo_label.setText(f"ALEX // {status}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: self.drag_pos = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton: self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos); self.drag_pos = event.globalPosition().toPoint(); event.accept()