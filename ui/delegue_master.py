import sqlite3
from PySide6.QtWidgets import QMainWindow, QTabWidget, QFileDialog, QLabel
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont
from PySide6.QtCore import Qt, QTimer, QTime

from core.classe import Classe
from import_export.xlsx import importer_xlsx
from ui.classe_tab import ClasseTab
from ui.menu_bar import MenuBar

from .eleves_tab import ElevesTab
from .conseils_tab import ConseilsTab
from settings.langues import Langues
from settings.profile import Profile
from settings.themes import Themes

class DelegueMaster(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialisation des classes de paramètres
        self.profile = Profile()
        self.langues = Langues(self)
        self.themes = Themes(self)
        
        # Initialisation de la classe Classe des Elèves
        self.classe = Classe()
        
        # Création et configuration de la barre de menu
        self.menuBar = MenuBar(self)
        
        # Onglets
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        
        # Onglet Éleves
        self.eleves_tab = ElevesTab(self)
        tabs.addTab(self.eleves_tab, 'Élèves')
        
        # Onglet Classe
        self.classe_tab = ClasseTab(self)
        tabs.addTab(self.classe_tab, 'Classe')
        
        # Onglet Conseils
        self.conseils_tab = ConseilsTab(self)
        tabs.addTab(self.conseils_tab, 'Conseils')
        
        # Titre de la fenêtre
        self.setWindowTitle('DéléguéMaster')
        
        # Configuration de la fenêtre principale
        self.setGeometry(100, 100, 800, 600)
        self.move(self.screen().geometry().center() - self.rect().center())
        
        self.setAcceptDrops(True)
        
         # Label pour afficher l'heure avec les secondes à droite des onglets
        self.label_heure = QLabel()
        self.label_heure.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        tabs.setCornerWidget(self.label_heure, Qt.TopRightCorner)
        
        # Mettre le texte en gras
        font = self.label_heure.font()
        font.setWeight(QFont.Bold)
        self.label_heure.setFont(font)

        # Ajouter une marge à droite du label de l'heure pour le décaler vers la gauche
        self.label_heure.setContentsMargins(0, 0, 20, 3)
        
        # Timer pour mettre à jour l'heure toutes les secondes
        self.timer_heure = QTimer(self)
        self.timer_heure.timeout.connect(self.mettre_a_jour_heure)
        self.timer_heure.start(1000)  # Mise à jour toutes les 1000 ms (1 seconde)
        
        self.mettre_a_jour()
        
    def mettre_a_jour_heure(self):
        heure_actuelle = QTime.currentTime().toString("hh:mm:ss")
        self.label_heure.setText(heure_actuelle)

    def getLangues(self):
        return self.langues
    
    def getThemes(self):
        return self.themes

    def getProfile(self):
        return self.profile
    
    def getElevesTab(self):
        return self.eleves_tab
    
    def getConseilsTab(self):
        return self.conseils_tab
    
    def getClasse(self):
        return self.classe
    
    def setClasse(self, classe):
        self.classe = classe
        self.mettre_a_jour()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            if url.isLocalFile() and url.toLocalFile().endswith('.xlsx'):
                file_path = url.toLocalFile()
                importer_xlsx(self, file_path)
                break
            if url.isLocalFile() and url.toLocalFile().endswith('.db'):
                file_path = url.toLocalFile()
                self.menuBar.ouvrir_fichier(file_path)
                break
            if url.isLocalFile() and url.toLocalFile().endswith('.csv'):
                file_path = url.toLocalFile()
                self.menuBar.importer_csv(file_path)
                break

    def exporter_fichier_db(self):
        fichier, _ = QFileDialog.getSaveFileName(self, "Sauvegarder Fichier DB", "", "Database Files (*.db)")
        if fichier:
            conn = sqlite3.connect(fichier)
            with sqlite3.connect('deleguemaster.db') as source:
                source.backup(conn)
            conn.close()

    def importer_fichier_db(self):
        fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir Fichier DB", "", "Database Files (*.db)")
        if fichier:
            conn = sqlite3.connect('deleguemaster.db')
            with sqlite3.connect(fichier) as source:
                source.backup(conn)
            conn.close()
            self.mettre_a_jour_classes()

    def mettre_a_jour(self):
        classe = self.classe.get_eleves()
        self.conseils_tab.vider()
        self.eleves_tab.vider()
        
        for eleve in classe:
            self.eleves_tab.ajouter_eleve(eleve.nom, eleve.prenom, eleve.date_naissance, eleve.sexe)
            self.conseils_tab.combo_eleves.addItem(eleve.get_nom_complet())
            
        for i in range(self.classe.get_nb_periodes()):
            self.conseils_tab.periodes_tab.addTab('Période ' + str(i + 1))
        
        self.classe_tab.mettre_a_jour()
            
