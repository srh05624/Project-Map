import os, json
from scripts import app_logging, installer
from datetime import datetime

# ===============================================================
# Utility functions
# ===============================================================
def exit(code=0):
    app_logging.log_info(f"Exiting application with code {code}.")
    os._exit(code)

# ===============================================================
# Config functions
# ===============================================================
def load_config(config_path=installer.config_path):
    try:
        if not os.path.exists(config_path):
            app_logging.log_warning(f"Config file {config_path} not found. Using default configuration.")
            return installer.default_config
        
        with open(config_path, 'r') as f:
            config = json.load(f)
            return {**installer.default_config, **config}
    except Exception as e:
        app_logging.log_error(f"Error loading config: {e}")
        return installer.default_config
    
def save_config(config, config_path=installer.config_path):
    try:
        app_logging.log_info(f"Saving config to {config_path}...")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        app_logging.log_error(f"Error saving config: {e}")

# ===============================================================
# Time and date functions
# ===============================================================
def current_time():
    return datetime.now().strftime("%H:%M:%S")

def current_date():
    return datetime.now().strftime("%Y-%m-%d")

def current_datetime():
    return datetime.now()

def format_datetime(date=current_date(), time=current_time()):
    try:
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%m-%d-%Y %I:%M:%S %p")
    except Exception as e:
        app_logging.log_error(f"Error formatting datetime: {e}")
        return "unknown_datetime"

def formated_time():
    try:
        time_now = datetime.now()
        time_final = time_now.strftime("%m-%d-%Y@")
        if time_now.hour > 12:
            time_final += f"{time_now.hour - 12:02d}-{time_now.minute:02d}-{time_now.second:02d}PM"
        else:
            time_final += f"{time_now.hour:02d}-{time_now.minute:02d}-{time_now.second:02d}AM"
        
        return time_final
    except Exception as e:
        app_logging.log_error(f"Error formatting time: {e}")
        return "unknown_time"
    
# ===============================================================
# File functions
# ===============================================================
def file_modification_time(file_path):
    try:
        return datetime.fromtimestamp(os.path.getmtime(file_path))
    except Exception as e:
        app_logging.log_error(f"Error getting file modification time: {e}")
        return datetime.min