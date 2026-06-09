from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve, QTimer, Qt, QSize
from ui.modules.map import MapWindow
from ui.modules.search import SearchBar
from ui.modules.marker_panel import MarkerPanel
from ui.modules.button import Button
from ui.modules.label import Label
from scripts.geocoder import Geocoder
from scripts.in_out_put import ImportExport
from scripts import app_logging, utils
import requests, json

class MainWindow(QMainWindow):
    def __init__(
            self,
            title: str = "Window",
            size=(400,300),
            position=(100,100),
            background_color=(255,255,255,255),
            config: dict | None = None,
            parent=None
        ):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(size[0], size[1])
        self.move(*position)
        self.setStyleSheet(f"background-color: rgba{background_color};")
        self.setCentralWidget(QWidget())
        self.showMaximized()

        self.config = config
        self.api_key = config["map"]["api_key"] if config else None
        self.geocoder = Geocoder(self.api_key)
        self.map = MapWindow(
            title="Map",
            style=config["map"]["style"] if config else None,
            api_key=self.api_key,
            config=self.config,
            parent=self
        )

        app_logging.log_info(" > Map window initialized successfully.")

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_marker = None
        self.setCentralWidget(self.map)

        self.markers_visible = True

        TRANSPARENT = (0, 0, 0, 0)

        # Home - (30.7285, -88.1380)

        # ==================================================
        # Search Setup
        # ==================================================
        self.search_bar = SearchBar(
            placeholder_text="Search...",
            size=(400, 30),
            background_color=(255, 255, 255, 220),
            position=(10, 10),
            confirm=self.move_to_search_result,
            parent=self.centralWidget()
        )

        if self.search_bar:
            self.search_bar.raise_()
            self.search_bar.textChanged.connect(self.schedule_search)

        self.geocoder.search_finished.connect(
            self.populate_results
        )

        self.search_timer.timeout.connect(
            self.perform_search
        )

        # ==================================================
        # Marker Panel Setup
        # ==================================================
        self.marker_panel = MarkerPanel(
            size=(400, 600),
            position=(0, 175),
            background_color=TRANSPARENT,
            border_color=TRANSPARENT,
            border_width=1,
            parent=self.centralWidget()
        )
        if self.marker_panel:
            self.marker_panel.raise_()

        self.map.display_list = self.marker_panel

        # ==================================================
        # Hide Button Setup
        # ==================================================
        self.hide_button = Button(
            text="<<",
            size=(35, 35),
            position=(400, 175),
            color=(0, 0, 0, 255),
            border_color=(200, 200, 200, 100),
            border_width=1,
            background_color=(255, 255, 255, 220),
            hover_color=(200, 200, 200, 255),
            hover_border_color=(200, 200, 200, 255),
            pressed_color=(160, 160, 160, 255),
            pressed_border_color=(200, 200, 200, 255),
            font="Arial",
            font_size=18,
            padding = 1,
            parent=self
        )

        if self.hide_button:
            self.hide_button.show()
            self.hide_button.raise_()
            self.hide_button.clicked.connect(self.toggle_marker_panel)

        # ==================================================
        # Import / Export Button Setup
        # ==================================================
        self.import_export = ImportExport(self.map, self.config)
        self.export_button = Button(
            text="Export",
            size=(80, 30),
            position=(10, 785),
            color=(0, 0, 0, 255),
            border_color=(200, 200, 200, 100),
            border_width=1,
            background_color=(255, 255, 255, 220),
            hover_color=(200, 200, 200, 255),
            hover_border_color=(200, 200, 200, 255),
            pressed_color=(160, 160, 160, 255),
            pressed_border_color=(200, 200, 200, 255),
            font="Arial",
            font_size=14,
            padding = 1,
            parent=self.centralWidget()
        )

        if self.export_button:
            self.export_button.show()
            self.export_button.raise_()
            self.export_button.clicked.connect(self.export_markers)

        self.import_button = Button(
            text="Import",
            size=(80, 30),
            position=(100, 785),
            color=(0, 0, 0, 255),
            border_color=(200, 200, 200, 100),
            border_width=1,
            background_color=(255, 255, 255, 220),
            hover_color=(200, 200, 200, 255),
            hover_border_color=(200, 200, 200, 255),
            pressed_color=(160, 160, 160, 255),
            pressed_border_color=(200, 200, 200, 255),
            font="Arial",
            font_size=14,
            padding = 1,
            parent=self.centralWidget()
        )

        if self.import_button:
            self.import_button.show()
            self.import_button.raise_()
            self.import_button.clicked.connect(self.import_markers)

        app_logging.log_info(" > Main window initialized successfully.")

    # ==================================================
    # Search functionality
    # ==================================================
    def schedule_search(self):
        self.search_timer.start(300)

    def perform_search(self):
        text = self.search_bar.text()

        if len(text) < 3:
            return

        self.geocoder.search(text)

    def populate_results(self, results):
        suggestions = [feature for feature in results]
        self.search_bar.refresh_items(suggestions)
    
    def move_to_search_result(self, feature):
        try:
            app_logging.log_info(f"Search result selected: {feature['place_name']} (Lat: {feature['center'][1]}, Lon: {feature['center'][0]})")
            lon = feature["center"][0]
            lat = feature["center"][1]

            self.search_marker = (lat, lon)

            if self.map:
                if self.search_marker:
                    self.map.remove_marker("search")
                self.map.set_search(lat, lon)
                self.map.move_to(lat, lon, zoom=16)
            
        except requests.RequestException as e:
            app_logging.log_error(f"Error during search: {e}")

    # ==================================================
    # Marker Panel functionality
    # ==================================================
    def toggle_marker_panel(self):
        if self.marker_panel:
            if self.markers_visible:
                self.tween_move(
                    self.marker_panel,
                    (self.marker_panel.pos().x() - self.marker_panel.width() + 10, self.marker_panel.pos().y()),
                    duration=300
                )

                self.tween_move(
                    self.hide_button,
                    (self.hide_button.pos().x() - self.marker_panel.width() + 10, self.hide_button.pos().y()),
                    duration=300
                )
                    
                self.hide_button.setText(">>")
            else:
                self.tween_move(
                    self.marker_panel,
                    (self.marker_panel.pos().x() + self.marker_panel.width() - 10, self.marker_panel.pos().y()),
                    duration=300
                )

                self.tween_move(
                    self.hide_button,
                    (self.hide_button.pos().x() + self.marker_panel.width() - 10, self.hide_button.pos().y()),
                    duration=300
                )

                self.hide_button.setText("<<")
            
            self.markers_visible = not self.markers_visible

    def tween_move(self, target, end, duration=500):
        animation = QPropertyAnimation(target, b"pos", self)
        animation.setDuration(duration)
        animation.setStartValue(target.pos())
        animation.setEndValue(QPoint(*end))
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        target._move_animation = animation
        animation.start()

    # ==================================================
    #  Close Event and State Saving
    # ==================================================
    def save_location(self, returned_value):
        if not returned_value:
            return
        try:
            if self.config is not None:
                dict_value = json.loads(returned_value)
                lat = dict_value["lat"]
                lng = dict_value["lng"]
                zoom = dict_value["zoom"]

                self.config["map"]["last_known_location"] = {
                    "latitude": lat,
                    "longitude": lng,
                    "zoom": zoom
                }

            utils.save_config(self.config)
        except json.JSONDecodeError:
            app_logging.log_error(f"Invalid map state: {returned_value}")
            return
    
        
    
    def closeEvent(self, event):
        if self.map:
            location = self.map.get_map_center(self.save_location)
        event.accept()

    # ==================================================
    # Import Markers
    # ==================================================
    def import_markers(self):
        if self.import_export and self.map:
            markers = self.import_export.import_markers_from_csv()

            if markers:
                blocker = Label(
                    text="Importing Markers...",
                    size=QSize(250, 75),
                    position=(self.width()//2 - 125, self.height()//2 - 37),
                    color=(0, 0, 0, 255),
                    background_color=(255, 255, 255, 220),
                    border_color=(200, 200, 200, 100),
                    border_width=2,
                    font="Arial",
                    font_size=24,
                    horizontal_align=Qt.AlignmentFlag.AlignCenter,
                    vertical_align=Qt.AlignmentFlag.AlignVCenter,
                    parent=self
                )
                blocker.show()

                self.map.clear_markers()

                for marker in markers:
                    properties = marker.get("properties", {})
                    geometry = marker.get("geometry", {})
                    
                    self.map.add_marker(
                        name=properties.get("id", "Unnamed Marker"),
                        lat=geometry.get("coordinates", [0, 0])[1],
                        lng=geometry.get("coordinates", [0, 0])[0],
                        color=properties.get("color", "#ff0000")
                    )

                blocker.hide()
                blocker.deleteLater()

    def export_markers(self):
        if self.import_export and self.map:
            if self.map.marker_list != []:
                blocker = Label(
                        text="Exporting Markers...",
                        size=QSize(250, 75),
                        position=(self.width()//2 - 125, self.height()//2 - 37),
                        color=(0, 0, 0, 255),
                        background_color=(255, 255, 255, 220),
                        border_color=(200, 200, 200, 100),
                        border_width=2,
                        font="Arial",
                        font_size=24,
                        horizontal_align=Qt.AlignmentFlag.AlignCenter,
                        vertical_align=Qt.AlignmentFlag.AlignVCenter,
                        parent=self
                    )
                blocker.show()
                self.import_export.export_markers_to_csv()

                blocker.hide()
                blocker.deleteLater()

    # ==================================================
    # Overrides the key press event to handle fullscreen toggle
    # ==================================================
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showMaximized()
            else:
                self.showFullScreen()