import sys
from PySide6.QtWidgets import QApplication
from ui.delegue_master import DelegueMaster

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DelegueMaster()
    window.show()
        
    sys.exit(app.exec())
