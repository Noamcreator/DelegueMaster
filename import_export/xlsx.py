import pandas as pd
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QLabel, QDialog, QComboBox, QSpinBox, QMessageBox

from core.classe import Classe
from core.eleve import Eleve

def importer_xlsx(delegue_master, file_path):
    # Charger le fichier Excel dans un DataFrame pandas
    df = pd.read_excel(file_path)

    # Extraire les classes disponibles
    classes_disponibles = df['Classe'].dropna().unique()

    # Créer une boîte de dialogue pour sélectionner la classe
    dialog = QDialog(delegue_master)
    dialog.setWindowTitle("Sélectionner une classe et le nombre de périodes")
    dialog.setGeometry(100, 100, 300, 100)
    dialog.move(delegue_master.screen().geometry().center() - delegue_master.rect().center())
    dialog_layout = QVBoxLayout()

    # Créer un combo box avec les classes disponibles
    classes_dispo = QComboBox()
    classes_dispo.setEditable(True)  # Permettre la recherche
    classes_dispo.addItems(classes_disponibles)
    classes_dispo.lineEdit().setPlaceholderText("Rechercher une classe...")
    dialog_layout.addWidget(classes_dispo)
        
    nb_periodes = QSpinBox()
    nb_periodes.setMinimum(1)
    nb_periodes.setValue(2) # Semestre par defaut
    dialog_layout.addWidget(nb_periodes)

    # Bouton OK pour valider la sélection
    ok_button = QPushButton("OK")
    ok_button.clicked.connect(dialog.accept)
    dialog_layout.addWidget(ok_button)

    dialog.setLayout(dialog_layout)
        
    # On demande à l'utilisateur s'il souhaite supprimer les données actuelles
    if delegue_master.getElevesTab().nombre_eleves() > 0:
        # Affichage d'une boîte de dialogue de confirmation
        resultat = QMessageBox.question(delegue_master, delegue_master.langues.tr('confirmer'),
                                        delegue_master.langues.tr('message_confirmation_suppression'),
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if resultat == QMessageBox.StandardButton.Yes:  # Si l'utilisateur confirme
            ok_pour_vider = True
        elif resultat == QMessageBox.StandardButton.No:  # Si l'utilisateur annule
            ok_pour_vider = False
    else:
        ok_pour_vider = True

    if dialog.exec() == QDialog.Accepted and ok_pour_vider:
        nom_classe = classes_dispo.currentText()
        nombres_periodes = nb_periodes.value()
            
        classe = Classe()
        classe.set_nom(nom_classe)
        classe.set_nb_periodes(nombres_periodes)

        # Filtrer les élèves par classe
        eleves = df[df['Classe'] == nom_classe]

        for _, row in eleves.iterrows():
            date_naissance = row['Né(e) le'].strftime('%Y-%m-%d')
            eleve = Eleve(row['Nom'], row['Prénom'])
            eleve.set_date_naissance(date_naissance)
            eleve.set_sexe(row['Sexe'])
            eleve.set_nb_periodes(nombres_periodes)
            classe.ajouter_eleve(eleve)

        delegue_master.setClasse(classe)
        dialog.close()
