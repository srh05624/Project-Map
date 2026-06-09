import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class LocalMapServer:
    def __init__(self, folder: str, port: int = 8765):
        self.folder = Path(folder).resolve()
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        folder = str(self.folder)

        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=folder, **kwargs)

        self.server = ThreadingHTTPServer(("127.0.0.1", self.port), Handler)

        self.thread = threading.Thread(
            target=self.server.serve_forever,
            daemon=True
        )
        self.thread.start()

    def url(self, filename="map.html"):
        return f"http://127.0.0.1:{self.port}/{filename}"