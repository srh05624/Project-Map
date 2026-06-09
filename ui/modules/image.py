from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class Image(QLabel):
    def __init__(self,
            image: str | QPixmap,
            size=(100, 100),
            position=(0, 0),
            parent=None
        ):
        super().__init__(parent)
        self.setGeometry(position[0], position[1], size[0], size[1])
        self.setStyleSheet("background-color: transparent;")

        if isinstance(image, QPixmap):
            self.setPixmap(image.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.setPixmap(QPixmap(image).scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation))