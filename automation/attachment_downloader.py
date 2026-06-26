import time
import os
from pathlib import Path
import pyautogui
import pyperclip
from pywinauto.findwindows import ElementNotFoundError

import config
from utils.logger import logger
from utils.settings import app_settings
from utils.helpers import generate_folder_path
from automation.ocr import ocr

class AttachmentDownloader:
    """Handles parsing an open email window and downloading its attachments."""
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def _read_field(self, field_name: str) -> str:
        """Attempts to read a field (Sender, Subject) via UI Automation or OCR."""
        # This is highly dependent on the specific UI structure.
        # In a generic UIA approach, we might look for text controls near labels.
        # Since Notes UIA trees are notoriously complex, we will try to copy all text 
        # or use hotkeys if possible, otherwise rely on OCR or assume empty if not critical.
        
        # A common trick in Notes is to select all (Ctrl+A) and Copy (Ctrl+C), 
        # then parse the clipboard. Let's try that if it's the whole email.
        return "" # We'll implement clipboard parsing in process_email instead for reliability
        
    def _save_attachments_via_right_click(self, save_path: Path) -> list[str]:
        """
        Attempts to find attachments, right click them, and use 'Save As'.
        Returns a list of downloaded filenames.
        """
        downloaded = []
        
        # 1. Attempt to find the attachment list control
        try:
            # Attachments are often in a List or Tree within the email view
            # Let's search for controls that might contain attachments
            attachment_controls = self.main_window.descendants(control_type="ListItem")
            
            # Filter ones that look like files (have extensions or sizes)
            # This is a heuristic.
            file_items = []
            for ctrl in attachment_controls:
                name = ctrl.window_text()
                if name and ("." in name or " KB" in name or " MB" in name):
                    file_items.append(ctrl)
                    
            if not file_items:
                logger.debug("No obvious attachment list items found via UIA.", to_ui=False)
                # Fallback to OCR to find the attachment region and right click it
                # We'll skip OCR for this specific step unless necessary to keep it fast
                return []
                
            for item in file_items:
                filename = item.window_text().split('\n')[0].strip() # rough guess
                if not filename:
                    filename = f"attachment_{int(time.time())}"
                    
                # Right click the item
                item.click_input(button='right')
                time.sleep(config.ACTION_DELAY)
                
                # Navigate context menu
                # PyAutoGUI is reliable for sending down-arrows or typing the shortcut key
                # We will try to click the "Save As" text via OCR on the context menu
                clicked = False
                for label in config.SAVE_AS_LABELS:
                    if ocr.click_text(label):
                        clicked = True
                        break
                        
                if not clicked:
                    # Fallback: send hotkey 'v' or 'a' depending on locale, or just arrow down
                    # This is brittle, so OCR is preferred.
                    logger.warning("Could not click 'Save As' on context menu.")
                    # Dismiss menu
                    pyautogui.press('esc')
                    continue
                    
                # Now wait for the "Save" dialog
                time.sleep(1.0)
                if self._handle_save_dialog(save_path, filename):
                    downloaded.append(filename)
                    
        except Exception as e:
            logger.error(f"Error during right-click save: {e}", to_ui=False)
            
        return downloaded
        
    def _handle_save_dialog(self, save_path: Path, expected_filename: str) -> bool:
        """Handles the standard Windows 'Save As' dialog."""
        try:
            # Wait for dialog
            dialog = self.main_window.child_window(title_re=".*Save.*", control_type="Window")
            if not dialog.exists(timeout=config.DIALOG_TIMEOUT):
                logger.error("Save dialog did not appear.")
                return False
                
            # Type the full path
            full_path = str(save_path / expected_filename)
            
            # Find the File Name edit control
            file_name_edit = dialog.child_window(control_type="Edit", found_index=0)
            file_name_edit.type_keys(full_path, with_spaces=True, set_foreground=False)
            time.sleep(config.ACTION_DELAY)
            
            # Click Save (usually default button, can just press Enter)
            dialog.type_keys("{ENTER}")
            time.sleep(config.ACTION_DELAY)
            
            # Handle "File already exists" overwrite prompt if it appears
            try:
                overwrite_dialog = dialog.child_window(title_re=".*Confirm.*", control_type="Window")
                if overwrite_dialog.exists(timeout=1):
                    overwrite_dialog.type_keys("{Y}") # Press Yes
            except:
                pass
                
            return True
        except Exception as e:
            logger.error(f"Failed to handle Save dialog: {e}", to_ui=False)
            # Try to escape out to not block the app
            pyautogui.press('esc')
            return False

    def extract_email_data_via_clipboard(self) -> dict:
        """
        Selects all, copies to clipboard, and parses basic info.
        Returns dict with 'sender', 'subject'.
        """
        # Save current clipboard
        old_cb = pyperclip.paste()
        pyperclip.copy("")
        
        # Select All, Copy
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.3)
        
        # Deselect
        pyautogui.press('esc')
        
        content = pyperclip.paste()
        
        # Restore old
        pyperclip.copy(old_cb)
        
        data = {"sender": "Unknown Sender", "subject": "No Subject"}
        
        if not content:
            return data
            
        lines = content.split('\n')
        # Crude parsing heuristic based on common email headers
        for i, line in enumerate(lines[:20]): # Check first 20 lines
            line_lower = line.lower()
            if "from:" in line_lower or "من:" in line_lower:
                data["sender"] = line.split(":", 1)[-1].strip()
            elif "subject:" in line_lower or "الموضوع:" in line_lower:
                data["subject"] = line.split(":", 1)[-1].strip()
                
        return data

    def process_open_email(self) -> dict:
        """
        Coordinates parsing the open email, checking filters, saving files, and closing.
        """
        result = {
            "sender": "Unknown",
            "subject": "Unknown",
            "status": "failed",
            "files": [],
            "error": ""
        }
        
        # Wait for email window to be active
        time.sleep(1)
        
        try:
            # 1. Extract data
            email_data = self.extract_email_data_via_clipboard()
            result["sender"] = email_data["sender"]
            result["subject"] = email_data["subject"]
            
            logger.info(f"Processing email from: {result['sender']}")
            
            # 2. Check filters
            from automation.email_filters import should_skip_email
            skip, reason = should_skip_email(result["sender"], result["subject"])
            if skip:
                result["status"] = "skipped"
                result["error"] = reason
                return result
                
            # 3. Determine save folder
            base_dir = app_settings.get("download_folder", str(config.DOWNLOADS_DIR))
            
            if app_settings.get("create_folder_per_email", True):
                save_path = generate_folder_path(base_dir, result["sender"], result["subject"])
            else:
                save_path = Path(base_dir) / "Attachments"
                
            save_path.mkdir(parents=True, exist_ok=True)
            
            # 4. Save attachments
            downloaded_files = self._save_attachments_via_right_click(save_path)
            result["files"] = downloaded_files
            
            if downloaded_files:
                result["status"] = "success"
                logger.success(f"Saved {len(downloaded_files)} attachments to {save_path.name}")
            else:
                result["status"] = "no_attachments"
                logger.info("No attachments found or saved.", to_ui=False)
                
            return result
            
        except Exception as e:
            logger.error(f"Error processing email: {e}")
            result["error"] = str(e)
            return result
        finally:
            # Always try to mark read and close
            if app_settings.get("mark_read", True):
                pyautogui.hotkey(*config.MARK_READ_HOTKEY.split('+'))
                time.sleep(config.ACTION_DELAY)
                
            # Close window
            pyautogui.hotkey(*config.CLOSE_EMAIL_HOTKEY.split('+'))
            time.sleep(config.ACTION_DELAY)
