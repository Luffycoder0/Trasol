import sys
import ctypes
from PyQt6.QtWidgets import QApplication

import config
from ui.main_window import MainWindow
from ui.styles import DARK_THEME
from utils.logger import logger

def main():
    # Set App ID so Windows taskbar groups the icon correctly
    myappid = f'{config.PUBLISHER}.{config.APP_NAME}.{config.APP_VERSION}'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass
        
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    
    logger.info("Application starting...")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
