from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize as Qsize

class Button(QPushButton):
    def __init__(
            self,
            text="Button",
            size=(100,25),
            position=(0,0),
            color=(0,0,0,255),
            background_color=(255,255,255,255),
            hover_color=(187,187,187,255),
            hover_border_color=(0,0,0,255),
            pressed_color=(119,119,119,255),
            pressed_border_color=(0,0,0,255),
            checked_color=(16,185,129,255),
            checked_border_color=(5,150,105,255),
            disabled_color=(156,163,175,255),
            disabled_background_color=(229,231,235,255),
            disabled_border_color=(209,213,219,255),
            font="Arial",
            font_size=10,
            padding=10,
            border_radius=5,
            border_color=(0,0,0,255),
            border_width=1,
            parent=None
        ):
        super().__init__(parent)

        # ==================================================
        #             -=- Button Properties -=-
        # ==================================================
        self.padding = padding
        self.button_size = Qsize(*size)
        self.position = position
        
        self.button_parent = parent

        # ==================================================
        #              -=- Text Properties -=-
        # ==================================================
        self.button_text = text
        self.text_font = font
        self.text_size = font_size

        # ==================================================
        #             -=- Border Properties -=-
        # ==================================================
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width
        
        # ==================================================
        #               -=- Color Palette -=-
        # ==================================================
        self.color = color
        self.background_color = background_color

        self.hover_color = hover_color
        self.hover_border_color = hover_border_color

        self.pressed_color = pressed_color
        self.pressed_border_color = pressed_border_color

        self.checked_color = checked_color
        self.checked_border_color = checked_border_color

        self.disabled_color = disabled_color
        self.disabled_background_color = disabled_background_color
        self.disabled_border_color = disabled_border_color

        self.setText(text)
        self.resize(self.button_size)
        self.move(*position)

        self.setStyleSheet(f"""
            QPushButton {{
                color: rgba{color};
                background-color: rgba{background_color};
                border-color: rgba{border_color};
                border-radius: {border_radius}px;
                border-width: {border_width}px;
                border-style: outset;
                font-family: {font};
                font-size: {font_size}px;
                padding: {padding}px;
            }}

            QPushButton:hover {{
                background-color: rgba{hover_color};
                border-color: rgba{hover_border_color};
            }}

            QPushButton:pressed {{
                background-color: rgba{pressed_color};
                border-color: rgba{pressed_border_color};
            }}

            QPushButton:checked {{
                background-color: rgba{checked_color};
                border-color: rgba{checked_border_color};
            }}

            QPushButton:disabled {{
                color: rgba{disabled_color};
                background-color: rgba{disabled_background_color};
                border-color: rgba{disabled_border_color};
            }}
        """)