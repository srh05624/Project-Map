import csv, os
from scripts import app_logging
from ui.requests import RequestManager

class ImportExport():
    def __init__(self, map, config):
        self.map = map
        self.config = config

    # ===============================================================
    # Import / Export functions
    # ===============================================================
    def export_markers_to_csv(self):
        if self.map is None:
            app_logging.log_warning("Map not set up. Cannot export markers.")
            return
        
        try:
            markers = self.map.marker_list
            request_manager = RequestManager("Select a file to save the markers")
            file_path = request_manager.request_file(filter="CSV Files (*.csv)")

            if file_path is None:
                app_logging.log_info("No file selected. Export cancelled.")
                return
            
            with open(file_path, 'w', newline='') as csvfile:
                fieldnames = ['id', 'color', 'type', 'lat', 'lon']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for marker in markers:
                    properties = marker.get("properties", {})
                    geometry = marker.get("geometry", {})

                    writer.writerow({
                        'id': properties.get('id', 'Unnamed Marker'),
                        'color': properties.get('color', '#000000'),
                        'type': marker.get("type", "Point"),
                        'lat': geometry.get('coordinates', [0, 0])[1],
                        'lon': geometry.get('coordinates', [0, 0])[0]
                    })
        except Exception as e:
            app_logging.log_error(f"Error exporting markers to CSV: {e}")
            app_logging.log_error(f"Error exporting markers to CSV: {e}")

    def import_markers_from_csv(self, file_path = None):
        if file_path is None:
            request_manager = RequestManager("Select a file to import markers from")
            file_path = request_manager.request_file(filter="CSV Files (*.csv)")
            if file_path is None:
                app_logging.log_info("No file selected. Import cancelled.")
                return None

        try:
            with open(file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                markers = []
                for row in reader:
                    markers.append({
                        "type": "Feature",
                        "properties": {
                            'id': row['id'],
                            'color': row.get('color', '#000000'),
                            'type': row.get('type', 'Point')
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(row['lon']), float(row['lat'])]
                        }
                    })
                
                return markers
        except Exception as e:
            app_logging.log_error(f"Error importing markers: {e}")
            app_logging.log_error(f"Error importing markers: {e}")
            return None
