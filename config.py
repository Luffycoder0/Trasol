"""
Application-wide constants, paths, and configuration.
Publisher: Djed Tech.ink
"""
from __future__ import annotations

import sys
from pathlib import Path

# ─── Identity ─────────────────────────────────────────────────────────────────
APP_NAME: str = "HCL Notes Attachment Downloader"
APP_VERSION: str = "3.0.0"
PUBLISHER: str = "Djed Tech.ink"

# ─── Automation limits ────────────────────────────────────────────────────────
MAX_EMAILS: int = 100
MAX_RETRIES: int = 3
RETRY_DELAY_SEC: float = 1.5
SCREENSHOT_ON_ERROR: bool = True
ACTION_DELAY: float = 0.4   # seconds between UI actions
DIALOG_TIMEOUT: float = 8.0  # seconds to wait for dialogs

# ─── HCL Notes 11.x process / window identifiers ─────────────────────────────
NOTES_PROCESS_NAMES: list[str] = [
    "nlnotes.exe",
    "notes.exe",
    "notes2.exe",
    "Notes2.exe",
    "NLNotes.exe",
]

# Window title patterns (regex) — Notes 11 uses "HCL Notes" prefix
NOTES_WINDOW_TITLE_RE: str = r".*(?:HCL Notes|IBM Notes|Lotus Notes).*"

# Inbox folder labels (English + Arabic, Notes may show either)
INBOX_LABELS: list[str] = [
    "Inbox",
    "البريد الوارد",
    "صندوق الوارد",
    "Boîte de réception",
]

# Context-menu item labels for "Save As" (Notes 11, English + Arabic)
SAVE_AS_LABELS: list[str] = [
    "Save As",
    "Save as",
    "Detach",
    "Save Attachment",
    "حفظ باسم",
    "حفظ المرفق",
    "فصل",
]

# Mark-as-read keyboard shortcut (Notes default)
MARK_READ_HOTKEY: str = "ctrl+q"

# Close email window shortcut
CLOSE_EMAIL_HOTKEY: str = "escape"

# ─── Skip / filter rules ──────────────────────────────────────────────────────
SKIP_SUBJECTS: list[str] = [
    "Delivery Time Out",
    "رفض استلام",
    "رفض الفاكس",
]

SKIP_SENDERS: list[str] = [
    "ادارة نظم المعلومات",
    "نظم المعلومات",
]

# ─── Base paths ───────────────────────────────────────────────────────────────
if getattr(sys, "frozen", False):
    # Running as PyInstaller bundle
    BASE_DIR: Path = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

RESOURCES_DIR: Path = BASE_DIR / "resources"
ICONS_DIR: Path = RESOURCES_DIR / "icons"
TRANSLATIONS_DIR: Path = RESOURCES_DIR / "translations"
STYLES_DIR: Path = RESOURCES_DIR / "styles"
LOGS_DIR: Path = BASE_DIR / "logs"
DOWNLOADS_DIR: Path = BASE_DIR / "downloads"
SCREENSHOTS_DIR: Path = BASE_DIR / "screenshots"
SETTINGS_FILE: Path = BASE_DIR / "settings.json"
REPORT_CSV: Path = BASE_DIR / "report.csv"
REPORT_JSON: Path = BASE_DIR / "report.json"

# ─── Ensure directories exist ─────────────────────────────────────────────────
for _d in [
    LOGS_DIR, DOWNLOADS_DIR, SCREENSHOTS_DIR,
    RESOURCES_DIR, ICONS_DIR, TRANSLATIONS_DIR, STYLES_DIR,
]:
    _d.mkdir(parents=True, exist_ok=True)
