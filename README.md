"""
HCL Notes Attachment Downloader
===============================

A production-ready Windows desktop application built with PyQt6 and pywinauto 
to automate downloading attachments from HCL Notes without using COM APIs.

Features
--------
- Modern dark theme UI
- Real-time logging and progress tracking
- Skips duplicate files and specific senders/subjects
- No COM or NotesSession dependencies (uses UI Automation)
- OCR fallback for difficult-to-locate controls

Requirements
------------
- Python 3.12+
- Windows 10/11
- HCL Notes client installed and running

Installation
------------
1. Install Python 3.12 or newer.
2. Clone or download this repository.
3. Open a terminal in the project directory.
4. Run: `pip install -r requirements.txt`

Usage
-----
1. Start HCL Notes and ensure it is unlocked and visible.
2. Run the application: `python main.py`
3. Configure the save folder and options in the UI.
4. Click "Start" to begin downloading attachments.

Building EXE
------------
Run the following command to build a standalone folder with PyInstaller:
`pyinstaller --noconfirm --onedir --windowed --icon "resources/icons/icon.ico" --name "HCL Notes Downloader" "main.py"`

Troubleshooting
---------------
- Ensure HCL Notes is the active window during automation.
- If UI Automation fails, the app will fallback to OCR (requires easyocr).
- Check the `logs/` directory for detailed error messages.
