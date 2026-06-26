from PyQt6.QtCore import QThread, pyqtSignal
from automation.notes_controller import NotesController

class DownloadWorker(QThread):
    """
    Background worker thread to run the Notes automation
    so it doesn't freeze the PyQt UI.
    """
    
    # Signals for UI updates
    progress_updated = pyqtSignal(int, int, str) # current, total, subject
    stats_updated = pyqtSignal(dict)
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.controller = NotesController()
        self.controller.set_callbacks(self._on_progress, self._on_stats)
        
    def _on_progress(self, current: int, total: int, subject: str):
        self.progress_updated.emit(current, total, subject)
        
    def _on_stats(self, stats: dict):
        self.stats_updated.emit(stats)
        
    def run(self):
        """Entry point for the thread."""
        self.controller.start()
        self.finished.emit()
        
    def stop(self):
        self.controller.stop()
        
    def pause(self):
        self.controller.pause()
        
    def resume(self):
        self.controller.resume()
