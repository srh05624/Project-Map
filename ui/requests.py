from PySide6.QtWidgets import QFileDialog, QApplication
from PySide6.QtCore import QCoreApplication

Image = "Images (*.png *.xpm *.jpg *.jpeg *.bmp)"
Document = "Documents (*.pdf *.docx *.txt)"

class RequestManager():
    def __init__(self, message):
        self.app = QCoreApplication.instance() or QApplication([])
        self.message = message
        
    # ===============================================================
    # File dialog functions
    # ===============================================================
    def request_dir(self, message=None):
        try:
            directory = QFileDialog.getExistingDirectory(
                None, 
                message or self.message,
                ""
            )
            return directory
        except Exception as e:
            return None
        
    def request_file(self, message=None, filter="All Files (*)"):
        try:
            file_dialog = QFileDialog()
            file_dialog.setWindowTitle(message or self.message)
            file_dialog.setNameFilter(filter)
            if file_dialog.exec():
                file_path = file_dialog.selectedFiles()[0]
                return file_path
            else:
                return None
        except Exception as e:
            return None
        
    def request_image_file(self, message=None):
        try:
            file_dialog = QFileDialog()
            file_dialog.setWindowTitle(message or self.message)
            file_dialog.setNameFilter(Image)
            if file_dialog.exec():
                file_path = file_dialog.selectedFiles()[0]
                return file_path
            else:
                return None
        except Exception as e:
            return None
        
    def request_document_file(self, message=None):
        try:
            file_dialog = QFileDialog()
            file_dialog.setWindowTitle(message or self.message)
            file_dialog.setNameFilter(Document)
            if file_dialog.exec():
                file_path = file_dialog.selectedFiles()[0]
                return file_path
            else:
                return None
        except Exception as e:
            return None