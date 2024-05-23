from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QDialog
from PySide6.QtGui import QDragEnterEvent, QDropEvent

from import_export.xlsx import importer_xlsx

class ImportElevesDialog(QDialog):
    def __init__(self, delegue_master):
        super().__init__(delegue_master)
        self.delegue_master = delegue_master

        self.setWindowTitle("Importation de Fichier")
        self.setGeometry(100, 100, 400, 200)
        self.move(self.screen().geometry().center() - self.rect().center())

        # Activer le drag and drop
        self.setAcceptDrops(True)

        # Initialisation des composants et configuration de la fenêtre
        self.initUI()

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout()

        # Bouton pour importer un fichier Excel
        self.import_button = QPushButton("Importer un fichier Excel (.xlsx)")
        self.import_button.clicked.connect(lambda: self.import_excel())
        layout.addWidget(self.import_button)

        # Définir le layout de la frame
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            if url.isLocalFile() and url.toLocalFile().endswith('.xlsx'):
                file_path = url.toLocalFile()
                importer_xlsx(self.delegue_master, file_path)
                break

    def import_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Importer un fichier Excel", "", "Fichiers Excel (*.xlsx)")
        if file_path:
            importer_xlsx(self.delegue_master, file_path)