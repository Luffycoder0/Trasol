import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QGroupBox, QCheckBox,
    QProgressBar, QFrame, QGridLayout, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QPixmap

import config
from utils.settings import app_settings
from utils.logger import logger
from ui.widgets import StatCard, LogViewer
from ui.dialogs import SettingsDialog
from workers.download_worker import DownloadWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{config.APP_NAME} - v{config.APP_VERSION}")
        
        # Load window geometry
        self.resize(
            app_settings.get("window_width", 1000),
            app_settings.get("window_height", 700)
        )
        
        # Set window icon
        icon_path = config.ICONS_DIR / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
            
        self.worker = None
        self._init_ui()
        self._update_status("Idle", "waiting")

    def _init_ui(self):
        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 1. Header
        header = QHBoxLayout()
        
        # Logo/Title
        title_layout = QVBoxLayout()
        title_lbl = QLabel(config.APP_NAME)
        font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        title_lbl.setFont(font)
        
        pub_lbl = QLabel(config.PUBLISHER)
        pub_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        
        title_layout.addWidget(title_lbl)
        title_layout.addWidget(pub_lbl)
        
        # Settings Button
        settings_btn = QPushButton("⚙ Settings")
        settings_btn.clicked.connect(self._open_settings)
        settings_btn.setFixedSize(90, 32)
        
        header.addLayout(title_layout)
        header.addStretch()
        header.addWidget(settings_btn)
        
        main_layout.addLayout(header)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #2d2d4e;")
        main_layout.addWidget(line)

        # 2. Main Content Split
        content_layout = QHBoxLayout()
        
        # LEFT COLUMN (Controls & Stats)
        left_col = QVBoxLayout()
        
        # Save Path
        path_group = QGroupBox("Save Directory")
        path_layout = QHBoxLayout()
        self.path_lbl = QLabel(app_settings.get("download_folder", str(config.DOWNLOADS_DIR)))
        self.path_lbl.setStyleSheet("color: #e2e8f0; font-weight: bold;")
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_folder)
        path_layout.addWidget(self.path_lbl, 1)
        path_layout.addWidget(browse_btn)
        path_group.setLayout(path_layout)
        left_col.addWidget(path_group)
        
        # Options
        opt_group = QGroupBox("Download Options")
        opt_layout = QVBoxLayout()
        self.chk_100 = QCheckBox("Process latest 100 emails")
        self.chk_unread = QCheckBox("Only process unread emails")
        self.chk_mark_read = QCheckBox("Mark read after download")
        
        self.chk_100.setChecked(app_settings.get("process_latest_100", True))
        self.chk_unread.setChecked(app_settings.get("only_unread", True))
        self.chk_mark_read.setChecked(app_settings.get("mark_read", True))
        
        self.chk_100.toggled.connect(lambda c: app_settings.set("process_latest_100", c))
        self.chk_unread.toggled.connect(lambda c: app_settings.set("only_unread", c))
        self.chk_mark_read.toggled.connect(lambda c: app_settings.set("mark_read", c))
        
        opt_layout.addWidget(self.chk_100)
        opt_layout.addWidget(self.chk_unread)
        opt_layout.addWidget(self.chk_mark_read)
        opt_group.setLayout(opt_layout)
        left_col.addWidget(opt_group)
        
        # Stats Cards
        stats_grid = QGridLayout()
        self.stat_processed = StatCard("Processed")
        self.stat_downloaded = StatCard("Downloaded")
        self.stat_skipped = StatCard("Skipped", color="#94a3b8")
        self.stat_errors = StatCard("Errors", color="#ef4444")
        
        stats_grid.addWidget(self.stat_processed, 0, 0)
        stats_grid.addWidget(self.stat_downloaded, 0, 1)
        stats_grid.addWidget(self.stat_skipped, 1, 0)
        stats_grid.addWidget(self.stat_errors, 1, 1)
        left_col.addLayout(stats_grid)
        
        left_col.addStretch()
        
        # Progress & Buttons
        self.progress_lbl = QLabel("Ready")
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Automation")
        self.start_btn.setObjectName("StartBtn")
        self.start_btn.clicked.connect(self._start_automation)
        self.start_btn.setFixedHeight(40)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setObjectName("StopBtn")
        self.stop_btn.clicked.connect(self._stop_automation)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setFixedHeight(40)
        
        btn_layout.addWidget(self.start_btn, 2)
        btn_layout.addWidget(self.stop_btn, 1)
        
        left_col.addWidget(self.progress_lbl)
        left_col.addWidget(self.progress)
        left_col.addLayout(btn_layout)
        
        content_layout.addLayout(left_col, 1) # weight 1
        
        # RIGHT COLUMN (Log View)
        right_col = QVBoxLayout()
        log_label = QLabel("Activity Log")
        log_label.setStyleSheet("color: #94a3b8; font-weight: bold;")
        self.log_viewer = LogViewer()
        right_col.addWidget(log_label)
        right_col.addWidget(self.log_viewer)
        
        content_layout.addLayout(right_col, 2) # weight 2
        
        main_layout.addLayout(content_layout)
        
        # Status Bar
        self.statusBar().setStyleSheet("background-color: #0d1117; color: #94a3b8;")
        self.statusBar().showMessage("Ready.")

    def closeEvent(self, event):
        # Save geometry
        app_settings.set("window_width", self.width())
        app_settings.set("window_height", self.height())
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(2000)
        event.accept()

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.path_lbl.text())
        if folder:
            self.path_lbl.setText(folder)
            app_settings.set("download_folder", folder)

    def _open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def _start_automation(self):
        if not os.path.exists(self.path_lbl.text()):
            QMessageBox.warning(self, "Invalid Path", "The selected download folder does not exist.")
            return
            
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress.setRange(0, 0) # Indeterminate
        
        # Disable inputs
        self.chk_100.setEnabled(False)
        self.chk_unread.setEnabled(False)
        self.chk_mark_read.setEnabled(False)
        
        self._update_status("Running", "running")
        
        self.worker = DownloadWorker()
        self.worker.progress_updated.connect(self._on_progress)
        self.worker.stats_updated.connect(self._on_stats)
        self.worker.finished.connect(self._on_worker_finished)
        self.worker.start()

    def _stop_automation(self):
        if self.worker:
            self.stop_btn.setText("Stopping...")
            self.stop_btn.setEnabled(False)
            self.worker.stop()

    def _on_progress(self, current, total, subject):
        self.progress.setRange(0, total)
        self.progress.setValue(current)
        self.progress_lbl.setText(f"Processing ({current}/{total}): {subject}")

    def _on_stats(self, stats: dict):
        self.stat_processed.set_value(stats.get("processed", 0))
        self.stat_downloaded.set_value(stats.get("downloaded", 0))
        self.stat_skipped.set_value(stats.get("skipped", 0))
        self.stat_errors.set_value(stats.get("errors", 0))

    def _on_worker_finished(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setText("Stop")
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.progress_lbl.setText("Finished.")
        
        # Re-enable inputs
        self.chk_100.setEnabled(True)
        self.chk_unread.setEnabled(True)
        self.chk_mark_read.setEnabled(True)
        
        self._update_status("Idle", "waiting")

    def _update_status(self, text: str, state: str):
        self.statusBar().showMessage(f"Status: {text}")
