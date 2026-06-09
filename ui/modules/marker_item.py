from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize
from ui.modules.label import Label
from ui.modules.image import Image
from ui.engine import Engine
import json

class MarkerItem(QWidget):
    def __init__(self,
            marker_data,
            size=(200, 30),
            parent=None
        ):
        super().__init__(parent)
        self.marker_data = marker_data
        self.id = self.marker_data.get("properties", {}).get("id", "Unnamed Marker")
        self.size_hint = size
        self.long = self.marker_data.get("geometry", {}).get("coordinates", [0, 0])[0]
        self.lat = self.marker_data.get("geometry", {}).get("coordinates", [0, 0])[1]

        TEXT_COLOR = (0, 0, 0, 255)
        TRANSPARENT = (0, 0, 0, 0)

        self.icon = Image(
            image=Engine.draw_circle(
                10,
                color=self.hex_to_rgba(self.marker_data.get("properties", {}).get("color", "#FF0000")),
                background_color=TRANSPARENT,
                outline_color=(255, 255, 255, 255),
                outline_width=2
                ),
            size=(20, 20),
            position=(5, 10),
            parent=self
        )

        self.label = Label(
            text=self.id,
            color=TEXT_COLOR,
            background_color=TRANSPARENT,
            font_size=16,
            parent=self
        )
        self.label.setGeometry(35, 10, self.size_hint[0] - 10, self.size_hint[1] - 10)

    def hex_to_rgba(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (255,)

    def sizeHint(self):
        return QSize(self.size_hint[0], self.size_hint[1] + 10)