import os, logging
from scripts import utils

# ===============================================================
# Logging functions
# ===============================================================
def setup_logging(log_dir, debug=False):
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, f"ServiceManager_{utils.formated_time()}.log")
        
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG if debug else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        log_info("Logging setup complete.")
        return True
    except Exception as e:
        print(f"Error setting up logging: {e}")
        return False

def log_debug(message):
    logging.debug(message)

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)

# ===============================================================
# Log file management
# ===============================================================
def remove_old_logs(log_dir, days_to_keep=7):
    try:
        if not os.path.exists(log_dir):
            return
        now = utils.current_datetime()
        for filename in os.listdir(log_dir):
            file_path = os.path.join(log_dir, filename)
            if os.path.isfile(file_path):
                file_age = (now - utils.file_modification_time(file_path)).days
                if file_age > days_to_keep:
                    os.remove(file_path)
                    log_info(f"Removed old log file: {filename}")
        return True
    except Exception as e:
        log_error(f"Error removing old log files: {e}")
        return False