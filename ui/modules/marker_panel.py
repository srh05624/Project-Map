from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from ui.modules.marker_item import MarkerItem
from ui.modules.button import Button

class MarkerList(QListWidget):
    def __init__(self,
            items=[],
            size=(100,25),
            position=(0,0),
            color=(0,0,0,0),
            background_color=(255,255,255,255),
            hover_color=(187,187,187,255),
            click_color=(119,119,119,255),
            border_color=(0,0,0,255),
            border_width=0,
            font="Arial",
            parent=None
        ):
        super().__init__(parent)

        self.setStyleSheet(f"""
            QListWidget {{
                color: rgba{color};
                background-color: rgba{background_color};
                font-family: {font};
                border: {border_width}px solid rgba{border_color};
            }}
            QListWidget::item {{
                outline: none;
                margin: 0px;
                padding: 0px;
            }}
            QListWidget::item:hover {{
                background-color: rgba{hover_color};
                color: rgba{color};
                }}
            QListWidget::item:selected {{
                background-color: rgba{click_color};
                color: rgba{color};
                }}
        """)

        self.setGeometry(position[0], position[1], size[0], size[1])

class MarkerPanel(QWidget):
    def __init__(self,
            markers: list | None = None,
            size=(200, 300),
            background_color=(255,255,255,255),
            border_color=(0,0,0,255),
            border_width=1,
            position=(0,0),
            parent=None
        ):
        super().__init__(parent)
        self.position = position
        self.markers = markers if markers else []

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setGeometry(position[0], position[1], size[0], size[1])

        r, g, b, a = background_color
        self.setStyleSheet(
            f"""
            MarkerPanel {{
                background-color: rgba({r}, {g}, {b}, {a});
                border: {border_width}px solid rgba{border_color};
            }}
            """
        )

        self.raise_()
        self.show()

        self.marker_list = MarkerList(
            items=self.markers,
            size=size,
            background_color=(255, 255, 255, 200),
            border_color=(255, 255, 255, 100),
            border_width=1,
            position=(0,0),
            parent=self
        )
        
        if self.marker_list:
            self.marker_list.raise_()
            self.marker_list.itemDoubleClicked.connect(self.focus_marker)
        

    def populate(self, markers: list[dict] | None = None):
        if markers is None or markers == []:
            return
        
        self.marker_list.clear()
        self.markers = markers

        for marker in self.markers:
            item = QListWidgetItem(self.marker_list)
            row = MarkerItem(marker, parent=self.marker_list)
            
            item.setSizeHint(row.sizeHint())
            self.marker_list.setItemWidget(item, row)


    def focus_marker(self, item):
        marker_obj = self.marker_list.itemWidget(item)
        
        if self.parent() and marker_obj:
            self.parent().move_to(marker_obj.lat, marker_obj.long)