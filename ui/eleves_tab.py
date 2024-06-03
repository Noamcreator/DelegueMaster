from PySide6.QtWidgets import QPushButton, QDialog, QMessageBox, QLabel, QHBoxLayout
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLineEdit, QTableWidgetItem

from core.eleve import Eleve
from ui.ajouter_eleve_dialog import AjouterEleveDialog

class ElevesTab(QWidget):
    def __init__(self, delegue_master):
        super().__init__()

        self.delegue_master = delegue_master

        tr = self.delegue_master.langues.tr

        layout = QVBoxLayout()

        # Ajout du champ de recherche
        ElevesTab.champ_de_recherche = QLineEdit()
        ElevesTab.champ_de_recherche.setPlaceholderText(tr('rechercher'))
        ElevesTab.champ_de_recherche.setClearButtonEnabled(True)
        ElevesTab.champ_de_recherche.textChanged.connect(self.filter_table_recherche)
        layout.addWidget(ElevesTab.champ_de_recherche)

        ElevesTab.table_eleves = QTableWidget()
        ElevesTab.table_eleves.setColumnCount(4)
        ElevesTab.table_eleves.setHorizontalHeaderLabels([tr('nom'), tr('prenom'), tr('date_de_naissance'), tr('sexe')])
        ElevesTab.table_eleves.currentItemChanged.connect(self.item_selectionne)
        ElevesTab.table_eleves.itemChanged.connect(self.renommer)
        layout.addWidget(ElevesTab.table_eleves)

        # Ajout des boutons Ajouter et Supprimer
        toolbar = QHBoxLayout()
        ElevesTab.ajouter_eleve_bouton = QPushButton(tr('ajouter_eleve'))
        ElevesTab.ajouter_eleve_bouton.clicked.connect(self.ajouter_eleve_action)
        self.delegue_master.menuBar.ajouter_eleve.triggered.connect(self.ajouter_eleve_action)
        toolbar.addWidget(ElevesTab.ajouter_eleve_bouton)

        ElevesTab.supprimer_eleve_bouton = QPushButton(tr('supprimer_eleve'))
        ElevesTab.supprimer_eleve_bouton.clicked.connect(self.supprimer_eleve_action)
        ElevesTab.supprimer_eleve_bouton.setEnabled(False)
        self.delegue_master.menuBar.supprimer_eleve.triggered.connect(self.supprimer_eleve_action)
        toolbar.addWidget(ElevesTab.supprimer_eleve_bouton)
        layout.addLayout(toolbar)

        self.setLayout(layout)

    def filter_table_recherche(self):
        # Récupère le texte de recherche en minuscules
        search_text = ElevesTab.champ_de_recherche.text().lower()

        # Parcourt les lignes de la table des élèves
        for row in range(ElevesTab.table_eleves.rowCount()):
            # Récupère le nom et le prénom de chaque élève dans la table en minuscules
            nom = ElevesTab.table_eleves.item(row, 0).text().lower()
            prenom = ElevesTab.table_eleves.item(row, 1).text().lower()

            # Cache ou montre la ligne en fonction du texte de recherche
            if search_text in nom or search_text in prenom:
                ElevesTab.table_eleves.setRowHidden(row, False)
            else:
                ElevesTab.table_eleves.setRowHidden(row, True)
    
    def vider(self):
        ElevesTab.table_eleves.setRowCount(0)
    
    def nombre_eleves(self):
        return self.table_eleves.rowCount()
    
    def ajouter_eleve_action(self):
        eleve_dialog = AjouterEleveDialog(self.delegue_master)
        
    def ajouter_eleve(self, nom, prenom, date_de_naissance, sexe):
        ElevesTab.table_eleves.setRowCount(ElevesTab.table_eleves.rowCount() + 1)
        ElevesTab.table_eleves.setItem(ElevesTab.table_eleves.rowCount() - 1, 0, QTableWidgetItem(nom))
        ElevesTab.table_eleves.setItem(ElevesTab.table_eleves.rowCount() - 1, 1, QTableWidgetItem(prenom))
        ElevesTab.table_eleves.setItem(ElevesTab.table_eleves.rowCount() - 1, 2, QTableWidgetItem(date_de_naissance))
        ElevesTab.table_eleves.setItem(ElevesTab.table_eleves.rowCount() - 1, 3, QTableWidgetItem(sexe))
        ElevesTab.table_eleves.resizeColumnsToContents()
    
    def supprimer_eleve_action(self):
        # Récupère la ligne actuellement sélectionnée
        current_row = ElevesTab.table_eleves.currentRow()
        
        eleve = self.delegue_master.getClasse().get_eleve(current_row)
        
        ElevesTab.table_eleves.setRowCount(ElevesTab.table_eleves.rowCount() - 1)
        for row in range(ElevesTab.table_eleves.rowCount()):
            if ElevesTab.table_eleves.item(row, 0).text() == eleve.get_nom() and ElevesTab.table_eleves.item(row, 1).text() == eleve.get_prenom() and ElevesTab.table_eleves.item(row, 2).text() == eleve.get_date_naissance() and ElevesTab.table_eleves.item(row, 3).text() == eleve.get_sexe():
                ElevesTab.table_eleves.removeRow(row)
                break

        self.delegue_master.getClasse().supprimer_eleve(eleve)
        
        self.delegue_master.mettre_a_jour()
        
        ElevesTab.table_eleves.setCurrentCell(-1, -1)
        
    def item_selectionne(self):
        # Vérifie si une ligne est sélectionnée dans la table des élèves
        if ElevesTab.table_eleves.currentRow() != -1:
            # Activer les options de suppression d'élève si une ligne est sélectionnée
            self.delegue_master.menuBar.supprimer_eleve.setEnabled(True)
            self.supprimer_eleve_bouton.setEnabled(True)
        else:
            # Désactiver les options de suppression si aucune ligne n'est sélectionnée
            self.delegue_master.menuBar.supprimer_eleve.setEnabled(False)
            self.supprimer_eleve_bouton.setEnabled(False)
    
    def renommer(self):
        # Récupère la ligne actuellement sélectionnée
        current_row = ElevesTab.table_eleves.currentRow()
        
        if current_row != -1:
            eleve = self.delegue_master.getClasse().get_eleve(current_row)

            nom = ElevesTab.table_eleves.item(current_row, 0).text()
            prenom = ElevesTab.table_eleves.item(current_row, 1).text()
            date_de_naissance = ElevesTab.table_eleves.item(current_row, 2).text()
            sexe = ElevesTab.table_eleves.item(current_row, 3).text()

            eleve.set_nom(nom)
            eleve.set_prenom(prenom)
            eleve.set_date_naissance(date_de_naissance)
            eleve.set_sexe(sexe)
        
            self.delegue_master.mettre_a_jour()
