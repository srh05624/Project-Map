from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize, Qt

class Label(QLabel):
    def __init__(self,
            text="",
            size: QSize = QSize(100, 30),
            position=(0, 0),
            color=(255, 255, 255, 255),
            background_color=(0, 0, 0, 0),
            border_color=(0, 0, 0, 0),
            border_width=0,
            horizontal_align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
            vertical_align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignVCenter,
            font="Arial",
            font_size=12,
            parent=None
        ):
        super().__init__(text, parent)
        self.setGeometry(position[0], position[1], size.width(), size.height())
        r, g, b, a = color
        br, bg, bb, ba = background_color
        bdr, bdg, bdb, bda = border_color
        
        self.setStyleSheet(f"""
            QLabel {{
                color: rgba({r}, {g}, {b}, {a});
                background-color: rgba({br}, {bg}, {bb}, {ba});
                border: {border_width}px solid rgba({bdr}, {bdg}, {bdb}, {bda});
                font-family: {font};
                font-size: {font_size}px;
            }}
        """)

        self.setAlignment(horizontal_align | vertical_align)