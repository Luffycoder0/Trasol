from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPlainTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCharFormat, QColor, QFont

from utils.logger import logger

class StatCard(QWidget):
    """A card widget to display a single statistic."""
    def __init__(self, label: str, value: str = "0", color: str = "#7c3aed"):
        super().__init__()
        self.setObjectName("StatCard")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
        
        self.val_label = QLabel(value)
        self.val_label.setObjectName("StatValue")
        self.val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.val_label.setStyleSheet(f"color: {color};")
        
        self.desc_label = QLabel(label)
        self.desc_label.setObjectName("StatLabel")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.val_label)
        layout.addWidget(self.desc_label)
        
    def set_value(self, value: str):
        self.val_label.setText(str(value))

class LogViewer(QPlainTextEdit):
    """Custom read-only text area for displaying colored logs."""
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumBlockCount(1000)
        
        # Connect to the global logger signals
        logger.signals.new_log.connect(self.append_log)
        
    def append_log(self, message: str, level: str):
        """Appends a colored log message."""
        fmt = QTextCharFormat()
        
        if level == "info":
            fmt.setForeground(QColor("#60a5fa")) # blue
        elif level == "warning":
            fmt.setForeground(QColor("#fbbf24")) # yellow
        elif level == "error":
            fmt.setForeground(QColor("#ef4444")) # red
        elif level == "success":
            fmt.setForeground(QColor("#22c55e")) # green
        else:
            fmt.setForeground(QColor("#e2e8f0")) # default
            
        self.setCurrentCharFormat(fmt)
        self.appendPlainText(message)
        
        # Reset format
        self.setCurrentCharFormat(QTextCharFormat())
        
        # Scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
