import sys, ctypes
from PySide6.QtWidgets import QApplication
from scripts import app_logging, installer, utils
from ui.modules.mainwindow import MainWindow

app = QApplication(["Navigation Application"])

def hide_console():
    if sys.platform == "win32":
        console = ctypes.windll.kernel32.GetConsoleWindow()
        if console:
            ctypes.windll.user32.ShowWindow(console, 0)  # 0 = hide

def main():
    install_results = installer.verify_all()
    if not install_results["success"]:
        utils.exit(1)

    config = utils.load_config(installer.config_path)

    if app_logging.setup_logging(config["logging"]["directory"]):
        app_logging.log_info("Application started.")
        for msg in install_results["messages"]:
            app_logging.log_info(msg)
    else:
        utils.exit(1)
    
    if app_logging.remove_old_logs(config["logging"]["directory"], config["logging"]["days_to_keep"]):
        app_logging.log_info("Old log files removed.")
    else:
        app_logging.log_error("Error removing old log files.")

    app_logging.log_info("Application initialization complete. Starting main window.")
    window = MainWindow(title="Navigation Application", size=(800,600), position=(100,100), background_color=(10,10,10,255), config=config)
    window.show()

    app_logging.log_info("Launching GUI.")
    app.exec()

    app_logging.log_info("Application exiting.")
    app.quit()

if __name__ == "__main__":
    hide_console()
    main()