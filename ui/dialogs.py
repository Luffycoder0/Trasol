from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QCheckBox, QComboBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

import config
from utils.settings import app_settings

class SettingsDialog(QDialog):
    """Dialog for configuring application settings."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)
        
        self._init_ui()
        self._load_settings()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # General Settings Group
        general_group = QGroupBox("General")
        form_layout = QFormLayout(general_group)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Arabic"])
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setEnabled(False) # Light theme not implemented yet
        
        form_layout.addRow("Language:", self.lang_combo)
        form_layout.addRow("Theme:", self.theme_combo)
        
        layout.addWidget(general_group)
        
        # Behavior Settings Group
        behavior_group = QGroupBox("Behavior")
        v_layout = QVBoxLayout(behavior_group)
        
        self.skip_dupes_cb = QCheckBox("Skip duplicate files")
        self.create_folders_cb = QCheckBox("Create folder per email")
        
        v_layout.addWidget(self.skip_dupes_cb)
        v_layout.addWidget(self.create_folders_cb)
        
        layout.addWidget(behavior_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._save_and_close)
        save_btn.setObjectName("StartBtn")
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
    def _load_settings(self):
        # Set UI elements based on current settings
        lang = app_settings.get("language")
        idx = self.lang_combo.findText(lang)
        if idx >= 0:
            self.lang_combo.setCurrentIndex(idx)
            
        self.skip_dupes_cb.setChecked(app_settings.get("skip_duplicates", True))
        self.create_folders_cb.setChecked(app_settings.get("create_folder_per_email", True))
        
    def _save_and_close(self):
        # Save settings
        app_settings.set("language", self.lang_combo.currentText())
        app_settings.set("skip_duplicates", self.skip_dupes_cb.isChecked())
        app_settings.set("create_folder_per_email", self.create_folders_cb.isChecked())
        
        self.accept()
