import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path

import config
from utils.logger import logger

def sanitize_filename(name: str) -> str:
    """Removes invalid characters from a string to make it a valid filename."""
    if not name:
        return "Unknown"
    # Replace invalid chars with underscore
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remove control characters
    name = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', name)
    # Strip leading/trailing spaces and dots
    name = name.strip('. ')
    return name[:150] if name else "Unknown"

def generate_folder_path(base_dir: str, sender: str, subject: str) -> Path:
    """Generates the nested folder path: YYYY-MM-DD/Sender_Subject/"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    clean_sender = sanitize_filename(sender)
    clean_subject = sanitize_filename(subject)
    
    # Create Sender_Subject string, truncate if too long
    folder_name = f"{clean_sender}_{clean_subject}"[:200]
    
    path = Path(base_dir) / date_str / folder_name
    return path

def write_report_csv(data: dict):
    """Appends a record to the CSV report."""
    fieldnames = ['Time', 'Sender', 'Subject', 'DownloadedFiles', 'Status', 'Error']
    file_exists = config.REPORT_CSV.exists()
    
    try:
        with open(config.REPORT_CSV, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            
            row = {
                'Time': datetime.now().isoformat(),
                'Sender': data.get('sender', ''),
                'Subject': data.get('subject', ''),
                'DownloadedFiles': ';'.join(data.get('files', [])),
                'Status': data.get('status', ''),
                'Error': data.get('error', '')
            }
            writer.writerow(row)
    except Exception as e:
        logger.error(f"Failed to write CSV report: {e}", to_ui=False)

def write_report_json(data: dict):
    """Appends a record to the JSON lines report."""
    row = {
        'timestamp': datetime.now().isoformat(),
        'sender': data.get('sender', ''),
        'subject': data.get('subject', ''),
        'downloaded_files': data.get('files', []),
        'status': data.get('status', ''),
        'error': data.get('error', '')
    }
    
    try:
        with open(config.REPORT_JSON, 'a', encoding='utf-8') as f:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
    except Exception as e:
        logger.error(f"Failed to write JSON report: {e}", to_ui=False)

def take_screenshot(prefix="error") -> str:
    """Takes a screenshot of the main screen and saves it."""
    import pyautogui
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"
    filepath = config.SCREENSHOTS_DIR / filename
    
    try:
        pyautogui.screenshot(str(filepath))
        return str(filepath)
    except Exception as e:
        logger.error(f"Failed to take screenshot: {e}", to_ui=False)
        return ""
