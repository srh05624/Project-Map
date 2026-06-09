# ProjectMap

A desktop mapping application built with Python, PySide6, and MapLibre.

ProjectMap provides an interactive map interface with support for custom markers, geolocation, and import/export functionality. The application uses a local HTTP server to host MapLibre assets and communicates between Python and JavaScript for real-time map interaction.

## Features

* Interactive MapLibre-based map
* Vector tile rendering
* Current location detection
* Add markers with double-click
* Remove markers with right-click
* Cycle marker colors with left-click
* Import marker data from JSON
* Export marker data to JSON
* Save and restore last viewed map location
* Standalone Windows executable support
* Python ↔ JavaScript communication using QWebChannel

## Technologies Used

* Python 3
* PySide6
* Qt WebEngine
* Qt WebChannel
* MapLibre GL JS
* MapTiler Vector Tiles
* JSON

## Controls

| Action             | Result             |
| ------------------ | ------------------ |
| Double Click       | Add Marker         |
| Left Click Marker  | Cycle Marker Color |
| Right Click Marker | Remove Marker      |
| Mouse Wheel        | Zoom               |
| Left Click + Drag  | Move Map           |

## Installation

### From Source

```bash
pip install -r requirements.txt
python main.py
```

### Build Executable

```bash
python -m PyInstaller --onefile --icon="assets/icon.ico" main.py
```

## Project Structure

```text
ProjectMap/
├── assets/
│   ├── map.html
│   ├── icon.ico
│   └── maplibre/
│       ├── maplibre-gl.js
│       └── maplibre-gl.css
├── scripts/
├── main.py
└── README.md
```

## Future Plans

* Address search and geocoding
* Route generation
* Marker categories
* Marker clustering
* Map image export
* Offline map support

## License

This project is licensed under the MIT License.
