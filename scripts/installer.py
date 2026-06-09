import os, json

local_path = str(os.getenv('APPDATA') or os.path.expanduser('~'))
install_path = os.path.join(local_path, "ProjectNav")
log_directory = os.path.join(install_path, "logs")
config_path = os.path.join(install_path, "config.json")

default_config = {
    "paths": {
        "install_directory": install_path,
        "log_directory": log_directory
    },
    "logging": {
        "directory": log_directory,
        "days_to_keep": 3,
        "debug": False
    },
    "import": {
        "directory": os.path.join(install_path, "data", "imports"),
        "enabled": True
    },
    "export": {
        "directory": os.path.join(install_path, "data", "exports"),
        "enabled": True
    },
    "map": {
        "maptiler_api_key": "LPHlvYyVZg3gaOCqZvM2",
        "style": "streets-v2",
        "api_key": None,
        "default_location": {
            "latitude": 30.7285,
            "longitude": -88.1380,
            "zoom": 10
        },
        "last_known_location": {
            "latitude": 30.7285,
            "longitude": -88.1380,
            "zoom": 10
        },
    }
}

# =====================================================
# Installation and Setup Functions
# =====================================================
def verify_install_directory():
    try:
        if not os.path.exists(install_path):
            os.makedirs(install_path, exist_ok=True)
            return f"Installation directory created at: {install_path}", True
        return f"Installation directory already exists at: {install_path}", True
    except Exception as e:
        return f"Error creating installation directory: {str(e)}", False

def verify_log_directory():
    try:
        if not os.path.exists(log_directory):
            os.makedirs(log_directory, exist_ok=True)
            return f"Log directory created at: {log_directory}", True
        return f"Log directory already exists at: {log_directory}", True
    except Exception as e:
        return f"Error creating log directory: {str(e)}", False

def verify_config_file():
    try:
        if not os.path.exists(config_path):
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return f"Config file created at: {config_path}", True
        return f"Config file already exists at: {config_path}", True
    except Exception as e:
        return f"Error creating config file: {str(e)}", False

def results(msg, success, data=None):
    if data is None:
        data = {"success": True, "messages": []}
    if not success:
        data["success"] = False
    data["messages"].append(msg)
    return data

def verify_all():
    data = {"success": True, "messages": []}
    results(*verify_install_directory(), data)
    results(*verify_log_directory(), data)
    results(*verify_config_file(), data)
    return data