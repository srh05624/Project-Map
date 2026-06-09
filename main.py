from PySide6.QtWidgets import QApplication
from scripts import installer, logging, utils
from ui.modules.mainwindow import MainWindow

app = QApplication(["Navigation Application"])

def main():
    print("Starting Navigation Application...")

    print("Verifying installation...")
    install_results = installer.verify_all()
    for msg in install_results["messages"]:
        print(f" > {msg}")
    if not install_results["success"]:
        print("Installation verification failed. Please address the above issues and restart the application.")
        utils.exit(1)

    print("Installation verified. Retrieving configuration...")
    config = utils.load_config(installer.config_path)
    if config is not None:
        print(" > Configuration loaded successfully.")

    print("Setting up logging...")

    if logging.setup_logging(config["logging"]["directory"], debug=config["logging"]["debug"]):
        print(" > Logging setup complete.")
        logging.log_info("Application started.")
    else:
        print(" > Error setting up logging.\nExiting application.")
        utils.exit(1)
    
    print("Removing old log files...")
    if logging.remove_old_logs(config["logging"]["directory"], config["logging"]["days_to_keep"]):
        print(" > Old log files removed.")
        logging.log_info("Old log files removed.")
    else:
        print(" > Error removing old log files.\nPlease check the log directory and permissions.")
        logging.log_error("Error removing old log files.")

    print("Starting application...")
    logging.log_info("Application initialization complete. Starting main window.")
    window = MainWindow(title="Navigation Application", size=(800,600), position=(100,100), background_color=(10,10,10,255), config=config)
    window.show()

    print("Launching GUI...")
    logging.log_info("Launching GUI.")
    app.exec()

    print("Exiting application...")
    logging.log_info("Application exiting.")
    app.quit()

if __name__ == "__main__":
    main()