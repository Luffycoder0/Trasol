import json
import os
from datetime import datetime

import config
from utils.logger import logger

class SettingsManager:
    """Manages application settings stored in settings.json."""
    
    def __init__(self):
        self.settings_file = config.SETTINGS_FILE
        self.default_settings = {
            "language": "English",
            "theme": "dark",
            "window_width": 1000,
            "window_height": 700,
            "download_folder": str(config.DOWNLOADS_DIR),
            "process_latest_100": True,
            "only_unread": True,
            "mark_read": True,
            "skip_duplicates": True,
            "create_folder_per_email": True,
            "save_sender_metadata": True,
            "save_subject_metadata": True,
            "skip_existing_emails": True,
            "last_run": None
        }
        self.settings = self._load()

    def _load(self) -> dict:
        """Load settings from JSON file or return defaults."""
        if not self.settings_file.exists():
            return self.default_settings.copy()
            
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Merge loaded data with defaults to ensure all keys exist
            merged = self.default_settings.copy()
            merged.update(data)
            return merged
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            return self.default_settings.copy()

    def save(self):
        """Save current settings to JSON file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def get(self, key: str, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)

    def set(self, key: str, value):
        """Set a setting value and save."""
        self.settings[key] = value
        self.save()
        
    def update_last_run(self):
        """Update the last_run timestamp."""
        self.set("last_run", datetime.now().isoformat())

# Global instance
app_settings = SettingsManager()
