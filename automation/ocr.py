import time
from typing import Optional, Tuple

import pyautogui

import config
from utils.logger import logger

class OCREngine:
    """Fallback OCR engine using easyocr to locate UI elements."""
    
    _instance = None
    _reader = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCREngine, cls).__new__(cls)
        return cls._instance
        
    def _init_reader(self):
        if self._reader is None:
            try:
                import easyocr
                logger.info("Initializing EasyOCR (this may take a moment)...")
                # Load English and Arabic models
                self._reader = easyocr.Reader(['en', 'ar'], gpu=False)
                logger.info("EasyOCR initialized successfully.", to_ui=False)
            except Exception as e:
                logger.error(f"Failed to initialize EasyOCR: {e}")
                
    def find_text_on_screen(self, target_text: str, region: Optional[Tuple[int, int, int, int]] = None, threshold: float = 0.6) -> Optional[Tuple[int, int]]:
        """
        Takes a screenshot and searches for target_text using OCR.
        Returns the (x, y) center coordinates of the found text, or None.
        region is (left, top, width, height)
        """
        self._init_reader()
        if not self._reader:
            return None
            
        try:
            # Capture screen
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
                
            import numpy as np
            # Convert to numpy array for OpenCV
            img_np = np.array(screenshot)
            # Convert RGB to BGR for OpenCV processing if needed, but EasyOCR handles RGB fine
            
            # Run OCR
            # detail=1 returns [(bounding_box, text, confidence), ...]
            results = self._reader.readtext(img_np, detail=1)
            
            target_lower = target_text.lower()
            
            for (bbox, text, conf) in results:
                if conf < threshold:
                    continue
                    
                if target_lower in text.lower():
                    # bbox is [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
                    x1, y1 = bbox[0]
                    x2, y2 = bbox[2]
                    
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    
                    # Adjust for region offset if provided
                    if region:
                        center_x += region[0]
                        center_y += region[1]
                        
                    logger.debug(f"OCR found '{text}' (conf: {conf:.2f}) at ({center_x}, {center_y})")
                    return (center_x, center_y)
                    
            logger.debug(f"OCR could not find text: '{target_text}'", to_ui=False)
            return None
            
        except Exception as e:
            logger.error(f"OCR error during search for '{target_text}': {e}", to_ui=False)
            return None
            
    def click_text(self, target_text: str, region: Optional[Tuple[int, int, int, int]] = None, 
                   button: str = 'left', clicks: int = 1) -> bool:
        """Finds text on screen and clicks it."""
        coords = self.find_text_on_screen(target_text, region)
        if coords:
            x, y = coords
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
            time.sleep(config.ACTION_DELAY)
            return True
        return False

# Global instance
ocr = OCREngine()
