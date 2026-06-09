from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize as Qsize
from scripts import app_logging

class Window(QWidget):
    def __init__(
            self,
            title="Window",
            size=(400,300),
            position=(100,100),
            background_color=(255,255,255,255),
            parent=None
        ):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setFixedSize(Qsize(*size))
        self.move(*position)
        self.setStyleSheet(f"background-color: rgba{background_color};")
        
        if parent:
            self.parent = parent
            app_logging.log_info(f"Window '{title}' created with parent '{parent.windowTitle()}'.")
        else:
            app_logging.log_warning("No parent specified for Window. This may lead to unexpected behavior.")
