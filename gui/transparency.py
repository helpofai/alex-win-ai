from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QFrame, QLineEdit
from PySide6.QtCore import Qt, Signal, QTimer, QPoint
from PySide6.QtGui import QColor, QFont, QScreen, QGuiApplication, QCursor

class Action:
    """The internal contract for every AI action."""
    def __init__(self, title, desc, tool, risk_score=0, steps=None):
        self.id = id(self)
        self.title = title
        self.description = desc
        self.tool = tool
        self.risk_score = risk_score # 0-100
        self.steps = steps or []
        self.estimated_time = "2 sec"
        self.reversible = True

class GlassPopup(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout(self)
        self.frame = QFrame()
        self.frame.setObjectName("GlassFrame")
        self.layout.addWidget(self.frame)
        self.content = QVBoxLayout(self.frame)
        
        title_label = QLabel(f"🤖 {title.upper()}")
        title_label.setStyleSheet("color: #00d4ff; font-weight: bold; font-size: 10px; letter-spacing: 1px;")
        self.content.addWidget(title_label)
        
        self.setStyleSheet("""
            #GlassFrame {
                background-color: rgba(10, 15, 20, 245);
                border: 1px solid #00d4ff;
                border-radius: 8px;
            }
            QLabel { color: #e0e0e0; font-family: 'Segoe UI'; font-size: 12px; }
            QPushButton { background: #1a1a1a; border: 1px solid #333; color: white; padding: 5px; border-radius: 4px; }
            QPushButton:hover { border: 1px solid #00d4ff; }
        """)

    def position_near_tray(self):
        # Detect which screen the cursor is on
        cursor_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(cursor_pos)
        if not screen:
            screen = QGuiApplication.primaryScreen()
        
        geo = screen.availableGeometry()
        
        # Position at bottom-right of the detected screen
        x = geo.x() + geo.width() - self.width() - 20
        y = geo.y() + geo.height() - self.height() - 20
        self.move(x, y)
        
        # Ensure it's on top and active
        self.raise_()
        self.activateWindow()

# --- A. PREVIEW POPUP ---
class ActionPreviewPopup(GlassPopup):
    authorized = Signal(bool)
    def __init__(self):
        super().__init__("AI Action Preview")
        self.setFixedWidth(300)
        self.info = QLabel("")
        self.content.addWidget(self.info)
        
        btns = QHBoxLayout()
        self.allow_btn = QPushButton("Allow")
        self.deny_btn = QPushButton("Deny")
        self.always_btn = QPushButton("Always")
        btns.addWidget(self.deny_btn); btns.addWidget(self.allow_btn); btns.addWidget(self.always_btn)
        self.content.addLayout(btns)
        
        self.allow_btn.clicked.connect(lambda: self.authorized.emit(True))
        self.deny_btn.clicked.connect(lambda: self.authorized.emit(False))

    def show_action(self, action: Action):
        risk_color = "🟢 Low" if action.risk_score < 25 else "🟡 Medium" if action.risk_score < 60 else "🔴 High"
        text = f"<b>Intent:</b> {action.title}<br><b>Tool:</b> {action.tool}<br><b>Risk:</b> {risk_color}<br><b>Time:</b> {action.estimated_time}"
        self.info.setText(text)
        self.show()
        self.position_near_tray()

# --- B. LIVE POPUP ---
class LiveExecutionPopup(GlassPopup):
    def __init__(self):
        super().__init__("Executing Action")
        self.setFixedWidth(280)
        self.step_label = QLabel("Step 1/1")
        self.desc_label = QLabel("Processing...")
        self.bar = QProgressBar()
        self.bar.setFixedHeight(4); self.bar.setTextVisible(False)
        self.content.addWidget(self.step_label)
        self.content.addWidget(self.desc_label)
        self.content.addWidget(self.bar)
        
        stop_btn = QPushButton("STOP NOW")
        stop_btn.setStyleSheet("color: #ff3333; font-weight: bold;")
        self.content.addWidget(stop_btn)

    def update(self, step, total, desc, progress):
        self.step_label.setText(f"Step {step} of {total}")
        self.desc_label.setText(desc)
        self.bar.setValue(progress)
        self.show()
        self.position_near_tray()

# --- C. RESULT POPUP ---
class ResultPopup(GlassPopup):
    def __init__(self):
        super().__init__("Action Completed")
        self.setFixedWidth(250)
        self.res_label = QLabel("")
        self.content.addWidget(self.res_label)
        self.timer = QTimer(); self.timer.timeout.connect(self.hide)

    def show_success(self, msg):
        self.res_label.setText(f"✅ {msg}")
        self.show(); self.position_near_tray(); self.timer.start(3000)

# --- D. CRITICAL POPUP ---
class CriticalConfirmationPopup(GlassPopup):
    confirmed = Signal(bool)
    def __init__(self):
        super().__init__("CRITICAL ACTION")
        self.setFixedWidth(320)
        self.frame.setStyleSheet("#GlassFrame { border: 2px solid #ff3333; background: rgba(30,0,0,240); }")
        
        self.desc_label = QLabel("")
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("color: #ffaaaa; font-size: 11px; margin-bottom: 10px;")
        self.content.addWidget(self.desc_label)
        
        self.content.addWidget(QLabel("⚠️ This action is dangerous.<br>Type <b>CONFIRM</b> to proceed:"))
        self.input = QLineEdit()
        self.input.setStyleSheet("background: #000; color: #ff3333; border: 1px solid #ff3333; padding: 5px;")
        self.content.addWidget(self.input)
        
        btn_layout = QHBoxLayout()
        self.yes_btn = QPushButton("Confirm")
        self.no_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.no_btn); btn_layout.addWidget(self.yes_btn)
        self.content.addLayout(btn_layout)
        
        self.yes_btn.clicked.connect(self.check_confirm)
        self.no_btn.clicked.connect(lambda: self.confirmed.emit(False))

    def check_confirm(self):
        if self.input.text().upper() == "CONFIRM":
            self.confirmed.emit(True)
        else:
            self.input.clear(); self.input.setPlaceholderText("INVALID")

    def show_critical(self, desc):
        self.desc_label.setText(desc)
        self.input.clear()
        self.show(); self.position_near_tray()
