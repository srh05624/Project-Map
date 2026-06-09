from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest,
    QNetworkReply
)
from PySide6.QtCore import QUrl
import json


class Geocoder(QObject):
    search_finished = Signal(list)

    def __init__(self, api_key):
        super().__init__()

        self.api_key = api_key
        self.network = QNetworkAccessManager()

    def search(self, query):
        url = (
            f"https://api.maptiler.com/geocoding/"
            f"{query}.json"
            f"?autocomplete=true"
            f"&limit=5"
            f"&key={self.api_key}"
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

        self.search_finished.emit(
            data.get("features", [])
        )

        reply.deleteLater()