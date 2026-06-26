import time
import psutil
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError

import config
from utils.logger import logger

class NotesWindowError(Exception):
    pass

class NotesWindowManager:
    """Manages the main HCL Notes application window via UI Automation."""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        
    def is_notes_running(self) -> bool:
        """Check if any Notes process is running."""
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] in config.NOTES_PROCESS_NAMES:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
        
    def connect(self) -> bool:
        """Connects to the running HCL Notes instance."""
        if not self.is_notes_running():
            logger.error("HCL Notes process not found. Please start HCL Notes.")
            return False
            
        try:
            # Connect using the UIA backend which is better for modern desktop apps
            self.app = Application(backend="uia").connect(title_re=config.NOTES_WINDOW_TITLE_RE, timeout=5)
            self.main_window = self.app.window(title_re=config.NOTES_WINDOW_TITLE_RE)
            
            # Ensure window is ready and visible
            if not self.main_window.exists(timeout=3):
                logger.error("Could not find the Notes main window.")
                return False
                
            logger.success("Successfully connected to HCL Notes window.")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Notes window: {e}")
            return False
            
    def bring_to_front(self):
        """Brings the Notes window to the foreground."""
        if self.main_window:
            try:
                self.main_window.set_focus()
                time.sleep(config.ACTION_DELAY)
            except Exception as e:
                logger.warning(f"Could not bring Notes to front: {e}", to_ui=False)
                
    def ensure_inbox_visible(self) -> bool:
        """
        Navigates to the Inbox if not already there.
        This is a complex UIA operation and might need OCR fallback
        if the tree structure is too deeply nested.
        """
        if not self.main_window:
            return False
            
        logger.info("Verifying Inbox is visible...")
        self.bring_to_front()
        
        try:
            # Try to find the Inbox tab or tree item
            # In Notes 11, there's usually a tab or a navigator pane
            
            # First, check if there's a visible control with the Inbox label
            for label in config.INBOX_LABELS:
                try:
                    # Look for a tab item or tree item containing the inbox text
                    inbox_item = self.main_window.child_window(title_re=f".*{label}.*", control_type="TabItem", found_index=0)
                    if inbox_item.exists(timeout=1):
                        inbox_item.click_input()
                        time.sleep(config.ACTION_DELAY)
                        logger.debug(f"Found and clicked Inbox tab: {label}", to_ui=False)
                        return True
                except ElementNotFoundError:
                    pass
                    
            # If not found via tab, look in the navigator tree
            for label in config.INBOX_LABELS:
                try:
                    inbox_item = self.main_window.child_window(title=label, control_type="TreeItem", found_index=0)
                    if inbox_item.exists(timeout=1):
                        inbox_item.click_input()
                        time.sleep(config.ACTION_DELAY)
                        logger.debug(f"Found and clicked Inbox tree item: {label}", to_ui=False)
                        return True
                except ElementNotFoundError:
                    pass
                    
            logger.warning("Could not definitively verify Inbox via UIA. Assuming it is open or needs manual selection.")
            # We return True anyway to let the email processor try to find the list
            return True
            
        except Exception as e:
            logger.error(f"Error while ensuring Inbox is visible: {e}", to_ui=False)
            return False
            
    def get_email_list(self):
        """
        Attempts to locate the DataGrid/List control containing the emails.
        Returns the UIA wrapper object if found.
        """
        if not self.main_window:
            return None
            
        try:
            # In Notes, the email list is usually a DataGrid or a custom Table control
            list_control = self.main_window.child_window(control_type="DataGrid", found_index=0)
            if list_control.exists(timeout=2):
                return list_control
                
            # Try List control
            list_control = self.main_window.child_window(control_type="List", found_index=0)
            if list_control.exists(timeout=2):
                return list_control
                
        except Exception as e:
            logger.debug(f"Could not find email list control: {e}", to_ui=False)
            
        return None
