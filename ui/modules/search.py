from PySide6.QtWidgets import QLineEdit, QPushButton
from ui.modules.button import Button

class SearchBar(QLineEdit):
    def __init__(
            self,
            text="",
            placeholder_text="",
            size=(100,25),
            position=(0,0),
            color=(0,0,0,255),
            background_color=(255,255,255,255),
            hover_color=(187,187,187,255),
            focus_color=(119,119,119,255),
            font="Arial",
            padding=5,
            confirm=None,
            parent=None
        ):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        self.setText(text)
        self.setStyleSheet(f"""
            QLineEdit {{
                color: rgba{color};
                background-color: rgba{background_color};
                font-family: {font};
                padding: {padding}px;
                border-radius: 5px;
            }}
            QLineEdit:hover {{
                background-color: rgba{hover_color};
            }}
            QLineEdit:focus {{
                background-color: rgba{focus_color};
            }}
        """)

        self.resize(size[0], size[1])
        self.move(position[0], position[1])

        self.items = []
        self.position = position
        self.confirm = confirm

    def refresh_items(self, new_items):
        self.clear_items()

        for i, feature in enumerate(new_items):
            name = feature["place_name"]
                                                                                                     
            new_item = Button(
                text=name,
                size=(self.width(), 25),
                position=(self.position[0], self.position[1] + self.height() + i*25),
                padding=0,
                parent=self.parent()
            )
            
            if new_item:
                self.items.append(new_item)
                if self.confirm:
                    new_item.clicked.connect(lambda confirm, feature=feature: self.confirm(feature))
                new_item.show()

    def clear_items(self):
        for item in self.items:
            item.deleteLater()
        self.items = []