"""QSS stylesheet for the application."""

DARK_THEME = """
/* Global */
QWidget {
    background-color: #0f0f1a;
    color: #e2e8f0;
    font-family: "Segoe UI", "Tahoma", sans-serif;
    font-size: 13px;
}

/* Main Window */
QMainWindow {
    background-color: #0f0f1a;
}

/* Cards / Containers */
QGroupBox {
    background-color: #16213e;
    border: 1px solid #2d2d4e;
    border-radius: 8px;
    margin-top: 1ex; /* leave space at the top for the title */
    padding-top: 15px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #94a3b8;
    font-weight: bold;
}

/* Stat Cards */
QWidget#StatCard {
    background-color: #1a1a2e;
    border: 1px solid #2d2d4e;
    border-radius: 6px;
}
QLabel#StatValue {
    font-size: 24px;
    font-weight: bold;
    color: #7c3aed;
}
QLabel#StatLabel {
    color: #94a3b8;
    font-size: 11px;
    text-transform: uppercase;
}

/* Buttons */
QPushButton {
    background-color: #1a1a2e;
    color: #e2e8f0;
    border: 1px solid #2d2d4e;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2d2d4e;
    border: 1px solid #7c3aed;
}
QPushButton:pressed {
    background-color: #16213e;
}
QPushButton:disabled {
    background-color: #0f0f1a;
    color: #475569;
    border: 1px solid #1e1e2e;
}

/* Primary/Action Buttons */
QPushButton#StartBtn {
    background-color: #7c3aed;
    color: white;
    border: none;
}
QPushButton#StartBtn:hover {
    background-color: #6d28d9;
}
QPushButton#StartBtn:disabled {
    background-color: #4c1d95;
    color: #94a3b8;
}

QPushButton#StopBtn {
    background-color: #ef4444;
    color: white;
    border: none;
}
QPushButton#StopBtn:hover {
    background-color: #dc2626;
}
QPushButton#StopBtn:disabled {
    background-color: #7f1d1d;
    color: #94a3b8;
}

/* Inputs */
QLineEdit {
    background-color: #0d1117;
    border: 1px solid #2d2d4e;
    border-radius: 4px;
    padding: 6px;
    color: #e2e8f0;
}
QLineEdit:focus {
    border: 1px solid #7c3aed;
}
QLineEdit:disabled {
    background-color: #1a1a2e;
    color: #475569;
}

/* Checkboxes */
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #2d2d4e;
    background-color: #0d1117;
}
QCheckBox::indicator:hover {
    border: 1px solid #7c3aed;
}
QCheckBox::indicator:checked {
    background-color: #7c3aed;
    border: 1px solid #7c3aed;
    image: url(resources/icons/check.png); /* Optional icon */
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #2d2d4e;
    border-radius: 4px;
    background-color: #0d1117;
    text-align: center;
    color: #e2e8f0;
}
QProgressBar::chunk {
    background-color: #7c3aed;
    border-radius: 3px;
}

/* Log View (QPlainTextEdit) */
QPlainTextEdit {
    background-color: #0d1117;
    color: #e2e8f0;
    border: 1px solid #2d2d4e;
    border-radius: 6px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background-color: #0d1117;
    width: 12px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background-color: #2d2d4e;
    min-height: 20px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background-color: #475569;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
