DARK_THEME = """
QMainWindow {
    background-color: transparent;
}

#CentralWidget {
    background-color: rgba(10, 15, 20, 230);
    border: 1px solid rgba(0, 212, 255, 50);
    border-radius: 20px;
}

/* Glass Panels */
#SidePanel {
    background-color: rgba(30, 30, 30, 100);
    border-right: 1px solid rgba(0, 212, 255, 30);
    border-radius: 10px;
}

QLabel {
    color: #e0e0e0;
    font-family: 'Consolas', 'Segoe UI';
}

#StatusLabel {
    color: #00d4ff;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 12px;
}

QTextEdit {
    background-color: rgba(0, 0, 0, 150);
    color: #00ffaa;
    border: none;
    border-radius: 10px;
    font-family: 'Consolas';
    font-size: 13px;
}

QLineEdit {
    background-color: rgba(20, 20, 20, 200);
    color: #00d4ff;
    border: 1px solid #333;
    border-radius: 15px;
    padding: 10px 20px;
    font-size: 14px;
}

QLineEdit:focus {
    border: 1px solid #00d4ff;
}

QPushButton {
    background-color: #00d4ff;
    color: #000;
    border-radius: 15px;
    padding: 8px 20px;
    font-weight: bold;
    text-transform: uppercase;
}

QPushButton:hover {
    background-color: #00ffff;
}

QProgressBar {
    border: 1px solid #333;
    border-radius: 5px;
    background: #111;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #00d4ff;
}
"""
