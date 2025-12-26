DARK_THEME = """
QMainWindow {
    background-color: transparent;
}

#CentralWidget {
    background-color: rgba(5, 10, 15, 200);
    border: 2px solid rgba(0, 212, 255, 80);
    border-radius: 30px;
}

/* Glass Panels */
#WingPanel {
    background-color: rgba(20, 25, 35, 150);
    border: 1px solid rgba(0, 212, 255, 40);
    border-radius: 20px;
}

QLabel {
    color: #00d4ff;
    font-family: 'Consolas', 'Segoe UI';
    text-transform: uppercase;
}

#HeaderLabel {
    font-weight: bold;
    letter-spacing: 5px;
    font-size: 14px;
    color: #00d4ff;
}

QTextEdit {
    background-color: transparent;
    color: #e0e0e0;
    border: none;
    font-family: 'Segoe UI';
    font-size: 13px;
}

QLineEdit {
    background-color: rgba(0, 0, 0, 180);
    color: #00ffaa;
    border: 1px solid #00d4ff;
    border-radius: 20px;
    padding: 12px 25px;
    font-size: 14px;
    font-family: 'Consolas';
}

QPushButton {
    background-color: rgba(0, 212, 255, 20);
    color: #00d4ff;
    border: 1px solid #00d4ff;
    border-radius: 15px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #00d4ff;
    color: #000;
}

QProgressBar {
    border: 1px solid rgba(0, 212, 255, 50);
    border-radius: 5px;
    background: rgba(0,0,0,100);
    text-align: center;
}
QProgressBar::chunk {
    background-color: #00ffaa;
}
"""