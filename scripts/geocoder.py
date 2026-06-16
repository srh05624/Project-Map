from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest
)
from PySide6.QtCore import QUrl
import json


class Geocoder(QObject):
    search_finished = Signal(list)

    def __init__(self, maptiler_api, google_api):
        super().__init__()

        self.maptiler_api_key = maptiler_api
        self.google_api_key = google_api
        self.network = QNetworkAccessManager()
        self.provider = "maptiler"

    def search(self, query):
        url = ""

        if self.provider == "google":
            url = (
                f"https://maps.googleapis.com/maps/api/geocode/json"
                f"?address={query}"
                f"&key={self.google_api_key}"
            )
        else:
            url = (
                f"https://api.maptiler.com/geocoding/"
                f"{query}.json"
                f"?autocomplete=true"
                f"&limit=5"
                f"&key={self.maptiler_api_key}"
            )

        request = QNetworkRequest(QUrl(url))

        reply = self.network.get(request)
        reply.finished.connect(
            lambda: self._handle_reply(reply)
        )

    def _handle_reply(self, reply):
        data = json.loads(
            bytes(reply.readAll()).decode()
        )
        
        if self.provider == "google":
            results = data.get("results", [])
        else:
            results = data.get("features", [])
        
        self.search_finished.emit(
            results
        )

        reply.deleteLater()