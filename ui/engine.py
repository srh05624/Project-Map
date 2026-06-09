from PIL import Image, ImageQt, ImageDraw
from PySide6.QtGui import QPixmap

class Engine:
    window = None

    @classmethod
    def draw_circle(cls, radius, color=(0, 0, 0, 0), background_color=(0, 0, 0, 0), outline_color=(0, 0, 0, 0), outline_width=0):
        img = Image.new("RGBA", (radius*2, radius*2), background_color)

        draw = ImageDraw.Draw(img, "RGBA")
        draw.ellipse((0, 0, radius*2 - outline_width, radius*2 - outline_width), fill=color, outline=outline_color, width=outline_width)

        qt_img = ImageQt.ImageQt(img)
        return QPixmap.fromImage(qt_img)