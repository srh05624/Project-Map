import requests
from scripts import logging

def download_osm_data(bbox, output_file):
    """
    Download OpenStreetMap data for a given bounding box and save it to a file.
    
    Parameters:
    - bbox: A tuple of (min_lon, min_lat, max_lon, max_lat) defining the bounding box.
    - output_file: The path to the file where the OSM data will be saved.
    
    Returns:
    - True if the download was successful, False otherwise.
    """
    
    try:
        min_lon, min_lat, max_lon, max_lat = bbox
        url = f"https://api.openstreetmap.org/api/0.6/map?bbox={min_lon},{min_lat},{max_lon},{max_lat}"
        
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        logging.log_info(f"OSM data downloaded successfully and saved to {output_file}")
        return True
    except Exception as e:
        logging.log_error(f"Error downloading OSM data: {e}")
        return False