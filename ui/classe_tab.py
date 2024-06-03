from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QTextEdit, QLineEdit, QTabWidget, QLabel, QTabBar, QDoubleSpinBox, QSpinBox

class ClasseTab(QWidget):
    def __init__(self, delegue_master):
        super().__init__()
        
        self.delegue_master = delegue_master
        tr = self.delegue_master.langues.tr
        
        # Création du layout principal
        layout = QVBoxLayout()
        
        # Ajout du label "Nom"
        self.nom_label = QLabel("Nom")
        layout.addWidget(self.nom_label)
        
        # Ajout du champ de texte pour écrire le nom
        self.nom_field = QLineEdit()
        self.nom_field.textChanged.connect(self.mettre_a_jour_classe)
        layout.addWidget(self.nom_field)
        
        # Ajout du label "Nombre de période"
        self.nbr_periode_label = QLabel("Nombre de périodes")
        layout.addWidget(self.nbr_periode_label)
        
        # Ajout du spin box pour sélectionner le nombre de périodes
        self.nbr_periode_spin = QSpinBox()
        self.nbr_periode_spin.setValue(2)
        self.nbr_periode_spin.setMinimum(1)  # Définit la valeur minimale
        self.nbr_periode_spin.setMaximum(10)  # Définit la valeur maximale
        self.nbr_periode_spin.valueChanged.connect(self.mettre_a_jour_classe)
        layout.addWidget(self.nbr_periode_spin)
        
        # Applique le layout au widget
        self.setLayout(layout)
    
    def mettre_a_jour(self):
        classe = self.delegue_master.getClasse()

        self.nom_field.setText(classe.get_nom())
        self.nbr_periode_spin.setValue(classe.get_nb_periodes())

    def mettre_a_jour_classe(self):
        self.delegue_master.getClasse().set_nom(self.nom_field.text())
        self.delegue_master.getClasse().set_nb_periodes(self.nbr_periode_spin.value())
        
        for eleve in self.delegue_master.getClasse().get_eleves():
            eleve.set_nb_periodes(self.nbr_periode_spin.value())
        
        self.delegue_master.mettre_a_jour()