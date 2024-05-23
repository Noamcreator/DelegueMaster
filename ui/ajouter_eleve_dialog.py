import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QComboBox, QTabWidget, QVBoxLayout, QWidget, QHBoxLayout, \
    QCheckBox, QDoubleSpinBox, QPushButton, QLineEdit, QInputDialog

from core.eleve import Eleve


class AjouterEleveDialog(QDialog):
    def __init__(self, delegue_master):
        super().__init__(delegue_master)
        self.delegue_master = delegue_master

        # Module de traduction pour les langues
        tr = delegue_master.langues.tr

        self.setWindowTitle(tr('ajouter_eleve'))
        self.setGeometry(100, 100, 400, 200)
        self.move(self.screen().geometry().center() - self.rect().center())

        layout = QVBoxLayout()

        label_nom = QLabel(tr("nom")+":")
        edit_nom = QLineEdit()
        layout.addWidget(label_nom)
        layout.addWidget(edit_nom)

        label_prenom = QLabel(tr('prenom') +":")
        edit_prenom = QLineEdit()
        layout.addWidget(label_prenom)
        layout.addWidget(edit_prenom)
        
        label_date_de_naissance = QLabel(tr("date_de_naissance")+":")
        edit_date_de_naissance = QLineEdit()
        layout.addWidget(label_date_de_naissance)
        layout.addWidget(edit_date_de_naissance)

        label_sexe = QLabel(tr('sexe') +":")
        choose_sexe = QComboBox()
        choose_sexe.addItems(['Masculin', 'Féminin'])
        layout.addWidget(label_sexe)
        layout.addWidget(choose_sexe)

        button_ok = QPushButton(tr('ok'))
        button_ok.clicked.connect(self.accept)
        layout.addWidget(button_ok)

        self.setLayout(layout)

        if self.exec() == QDialog.DialogCode.Accepted:
            # enlever la selection d'une table
            nom = edit_nom.text()
            nom = nom.upper()  # mettre le nom en majuscule
            
            prenom = edit_prenom.text()
            # mettre la premier lettre de chaque mot en majuscule
            prenom = ' '.join([word.capitalize() for word in prenom.split()])
            
            date_de_naissance = edit_date_de_naissance.text()
            sexe = choose_sexe.currentText()
            
            eleve = Eleve(nom, prenom)
            eleve.set_date_naissance(date_de_naissance)
            eleve.set_sexe(sexe)
            eleve.set_nb_periodes(self.delegue_master.getClasse().get_nb_periodes())
            
            self.delegue_master.getClasse().ajouter_eleve(eleve)
            self.delegue_master.mettre_a_jour()

