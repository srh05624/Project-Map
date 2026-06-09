from pathlib import Path
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Slot, QUrl, Qt
from scripts.map_server import LocalMapServer
from scripts import app_logging
import json, sys

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(relative_path).resolve()

map_folder = resource_path("assets")

app_logging.log_info("Map module loaded.")
app_logging.log_info(f"Map assets path: {map_folder}")

styles = [
    "streets-v2",
    "basic-v2",
    "bright-v2",
    "outdoor-v2",
    "satellite",
    "hybrid",
    "topo-v2"
]

class MapBridge(QObject):
    def __init__(self,
            load_callback=None,
            refresh=None,
            parent=None
        ):
        super().__init__(parent)
        self.refresh = refresh
        self.load_callback = load_callback

    @Slot(str)
    def loadCompleted(self, message):
        if message == "Map loaded and ready":
            if self.load_callback:
                self.load_callback()
            app_logging.log_info("Map loaded successfully and ready for interaction.")
        else:
            app_logging.log_error(f"Map failed to load. Message from JS: {message}")

    @Slot(str)
    def markersEdited(self, markers_json):
        markers = json.loads(markers_json)["features"]
        
        if self.refresh:
            self.refresh(markers=markers)
            app_logging.log_info(f"Markers updated from JS. Total markers: {len(markers)}")

class MapWindow(QWebEngineView):
    def __init__(
            self,
            html_path: Path = map_folder,
            title : str = "Map",
            style: str | None = styles[0],
            api_key: str | None = None,
            display_list = None,
            config: dict | None = None,
            parent = None
        ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.marker_list = []
        self.display_list = display_list if display_list else None
        self.map_style = style
        self.api_key = api_key
        self.config = config

        self.channel = QWebChannel()
        self.bridge = MapBridge(load_callback=self.map_setup, refresh=self.refresh_markers, parent=self)
        self.channel.registerObject("pyBridge", self.bridge)
        self.page().setWebChannel(self.channel)

        from PySide6.QtWebEngineCore import QWebEngineSettings

        self.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
            True
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            False
        )

        self.page().featurePermissionRequested.connect(
            self.handle_permission_request
        )

        if html_path and html_path != "":
            self.map_server = LocalMapServer(str(html_path), port=8765)
            self.map_server.start()

            self.setUrl(QUrl("http://127.0.0.1:8765/map.html"))

        self.loadFinished.connect(lambda ok: self.load_style() if ok else None)

    # ==================================================
    # Utility functions
    # ==================================================
    def run_js(self, script, callback=None):
        if callback is None:
            callback = print 
        self.page().runJavaScript(script, callback)

    def handle_permission_request(self, security_origin, feature):
        try:
            if feature == QWebEnginePage.Feature.Geolocation:
                self.page().setFeaturePermission(
                    security_origin,
                    feature,
                    QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
                )
        except Exception as e:
            app_logging.log_error(f"Error handling permission request: {e}")

    def load_style(self):
        style_url = f"https://api.maptiler.com/maps/{self.map_style}/style.json?key={self.api_key}"

        if self.map_style is not None:
            app_logging.log_info(f"Loading map style: {self.map_style}")
            self.run_js(f"setMapStyle('{style_url}');")

    def map_setup(self):
         try:
            self.load_style()

            if self.config:
                app_logging.log_info("Loading map details from configuration...")
                last_known_location = self.config.get("map", {}).get("last_known_location", None)
                default_location = self.config["map"]["default_location"]

                if last_known_location:
                    self.move_to(last_known_location["latitude"], last_known_location["longitude"], last_known_location["zoom"])
                elif default_location:
                    self.move_to(default_location["latitude"], default_location["longitude"], default_location["zoom"])

         except Exception as e:
            app_logging.log_warning(f"Error loading map details: {e}")

    def load_markers(self, markers):
        app_logging.log_info(f"Loading {len(markers)} markers onto the map...")

        for marker in markers:
            try:
                name = marker.get("properties", {}).get("id", "Unnamed Marker")
                color = marker.get("properties", {}).get("color", "#ff0000")
                coordinates = marker.get("geometry", {}).get("coordinates", [0, 0])
                lng, lat = coordinates[0], coordinates[1]
                self.add_marker(name, lat, lng, color=color)
            except Exception as e:
                app_logging.log_warning(f"Error loading marker '{marker}': {e}")

    # ==================================================
    # Marker functions
    # ==================================================
    def refresh_markers(self, markers=None):
        if self.display_list is not None:
            self.marker_list = markers if markers is not None else []
            self.display_list.populate(markers=markers)
    
    def add_marker(self, name, lat, lng, color="#ff0000"):
        self.run_js(f"addMarker('{name}', {lat}, {lng}, '{color}');")
    
    def remove_marker(self, name):
        self.run_js(f"removeMarker('{name}');")

    def update_marker(self, name, lat="null", lng="null", color="null"):
        self.run_js(f"updateMarker('{name}', {lat}, {lng}, '{color}');")

    def clear_markers(self):
        self.run_js("clearMarkers();")

    def set_search(self, lat, lng):
        self.run_js(f"setSearch({lat}, {lng});")

    # ==================================================
    # Map functions
    # ==================================================
    def get_map_center(self, callback=None):
        return self.run_js("getMapState();", callback)

    def jump_to(self, lat, lng):
        self.run_js(f"jumpTo({lat}, {lng});")

    def move_to(self, lat, lng, zoom = 16):
        self.run_js(f"easeTo({lat}, {lng}, {zoom});")

    def set_home(self, lat, lng):
        self.run_js(f"setHome({lat}, {lng});")

    def snap_to_position(self):
        current_position = self.get_map_center()
        if current_position is not None and current_position != "":
            self.add_marker("_currentPosition", current_position["lat"], current_position["lng"], color="#0000ff")
    
    def is_map_loaded(self):
        return self.page().url() != QUrl("about:blank")
