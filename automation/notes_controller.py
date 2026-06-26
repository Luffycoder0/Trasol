import time
from typing import Callable

import config
from utils.logger import logger
from utils.settings import app_settings
from utils.helpers import write_report_csv, write_report_json
from automation.notes_window import NotesWindowManager
from automation.attachment_downloader import AttachmentDownloader

class NotesController:
    """Orchestrates the overall automation workflow."""
    
    def __init__(self):
        self.window_mgr = NotesWindowManager()
        self.downloader = None
        self.is_running = False
        self.is_paused = False
        
        # Callbacks for UI updates
        self.on_progress = None
        self.on_stats_update = None
        
        self.stats = {
            "processed": 0,
            "downloaded": 0,
            "skipped": 0,
            "errors": 0
        }

    def set_callbacks(self, progress_cb: Callable, stats_cb: Callable):
        self.on_progress = progress_cb
        self.on_stats_update = stats_cb

    def _update_stats(self, key: str, increment: int = 1):
        self.stats[key] += increment
        if self.on_stats_update:
            self.on_stats_update(self.stats)

    def _check_pause(self):
        while self.is_paused and self.is_running:
            time.sleep(0.5)

    def start(self):
        """Main automation loop."""
        self.is_running = True
        self.is_paused = False
        
        # Reset stats
        for k in self.stats:
            self.stats[k] = 0
        if self.on_stats_update:
            self.on_stats_update(self.stats)

        logger.info("Starting automation sequence...")

        if not self.window_mgr.connect():
            self.is_running = False
            return

        self.downloader = AttachmentDownloader(self.window_mgr.main_window)

        if not self.window_mgr.ensure_inbox_visible():
            logger.warning("Inbox might not be visible. Attempting to proceed anyway.")

        email_list = self.window_mgr.get_email_list()
        if not email_list:
            logger.error("Could not locate the email list in Notes. Stopping.")
            self.is_running = False
            return

        max_emails = config.MAX_EMAILS if app_settings.get("process_latest_100") else 1000
        logger.info(f"Scanning up to {max_emails} newest emails...")

        try:
            # We assume the newest emails are at the top (index 0, 1, 2...)
            for i in range(max_emails):
                if not self.is_running:
                    break
                    
                self._check_pause()

                try:
                    # In pywinauto, getting items from a list/grid can be tricky depending on implementation.
                    # As a general strategy, we can send the HOME key to jump to top, 
                    # process the email, and then DOWN arrow to the next.
                    
                    if i == 0:
                        email_list.type_keys("{HOME}")
                    else:
                        email_list.type_keys("{DOWN}")
                        
                    time.sleep(config.ACTION_DELAY)

                    # Check if unread (this often requires looking at an icon column or state)
                    # We will just open it and try to figure it out, or assume it's unread if the setting is off.
                    # For a robust non-COM solution without a clear "Unread" property exposed to UIA,
                    # we often just process it.
                    
                    # Open the email
                    email_list.type_keys("{ENTER}")
                    time.sleep(2.0) # wait for email to open
                    
                    result = self.downloader.process_open_email()
                    
                    # Update stats based on result
                    self._update_stats("processed")
                    
                    if result["status"] == "success":
                        self._update_stats("downloaded", len(result["files"]))
                    elif result["status"] == "skipped":
                        self._update_stats("skipped")
                    elif result["status"] == "failed":
                        self._update_stats("errors")
                        
                    # Write reports
                    write_report_csv(result)
                    write_report_json(result)
                    
                    if self.on_progress:
                        self.on_progress(i + 1, max_emails, result.get("subject", "Unknown"))
                        
                except Exception as row_e:
                    logger.error(f"Failed to process email at index {i}: {row_e}")
                    self._update_stats("errors")
                    # Try to close any stuck window
                    import pyautogui
                    pyautogui.press('esc')
                    time.sleep(0.5)

        except Exception as e:
            logger.error(f"Automation loop error: {e}")
            if config.SCREENSHOT_ON_ERROR:
                from utils.helpers import take_screenshot
                take_screenshot("loop_error")

        logger.success("Automation finished.")
        self.is_running = False
        app_settings.update_last_run()

    def stop(self):
        self.is_running = False
        logger.info("Stop requested by user.")

    def pause(self):
        self.is_paused = True
        logger.info("Automation paused.")

    def resume(self):
        self.is_paused = False
        logger.info("Automation resumed.")
