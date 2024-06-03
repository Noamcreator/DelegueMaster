# Importation des modules nécessaires
import os  # Module pour les opérations sur le système d'exploitation

# Importations PyQt6 pour l'interface graphique
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMessageBox, QFileDialog, QTextEdit, QPushButton, QVBoxLayout, QDialog, QCheckBox, QLabel
# Importation de la fonction pour appliquer un thème à l'interface
from qt_material import apply_stylesheet

from core.classe import Classe
from database.db_handler import ouvrir_db, sauvegarder_db
from import_export.csv import exporter_csv, importer_csv
from import_export.pdf import exporter_pdf
<<<<<<< HEAD
from import_export.txt import exporter_txt, importer_txt
=======
>>>>>>> dc682bbcb658d6e2427319f7e6d1c93c16bddda1
from import_export.xlsx import importer_xlsx

from .settings_dialog import SettingsDialog

# Classe de la barre de menu
class MenuBar:
    # Initialisation de la barre de menu
    def __init__(self, delegue_master):
        # Référence à la fenêtre principale
        self.delegue_master = delegue_master

        # Récupération de la barre de menu de la fenêtre principale
        menubar = delegue_master.menuBar()

        # Récupération de la fonction de traduction
        tr = self.delegue_master.langues.tr

        # MENU FICHIER
        MenuBar.menu_fichier = menubar.addMenu(tr('fichier'))

        # Nouveau projet (on supprime les données actuelles)
        MenuBar.nouveau = QAction(tr('nouveau'), delegue_master)
        MenuBar.nouveau.setShortcut('Ctrl+N')
        MenuBar.nouveau.triggered.connect(self.nouveau_action)
        MenuBar.menu_fichier.addAction(MenuBar.nouveau)

        # Ouvrir un projet (en db)
        MenuBar.ouvrir = QAction(tr('ouvrir'), delegue_master)
        MenuBar.ouvrir.setShortcut('Ctrl+O')
        MenuBar.ouvrir.triggered.connect(self.ouvrir_action)
        self.db_file_open = None
        MenuBar.menu_fichier.addAction(MenuBar.ouvrir)

        # Enregistrer
        MenuBar.enregistrer = QAction(tr('enregistrer'), delegue_master)
        MenuBar.enregistrer.setShortcut('Ctrl+S')
        MenuBar.enregistrer.triggered.connect(self.enregistrer_action)
        MenuBar.menu_fichier.addAction(MenuBar.enregistrer)

        # Enregistrer sous
        MenuBar.enregistrer_sous = QAction(tr('enregistrer_sous'), delegue_master)
        MenuBar.enregistrer_sous.setShortcut('Ctrl+Shift+S')
        MenuBar.enregistrer_sous.triggered.connect(self.enregistrer_sous_action)
        MenuBar.menu_fichier.addAction(MenuBar.enregistrer_sous)

        MenuBar.menu_fichier.addSeparator()

        # Sous-menu Importer
        MenuBar.menu_importer = MenuBar.menu_fichier.addMenu(tr('importer'))
        MenuBar.menu_fichier.addMenu(MenuBar.menu_importer)

        # Importer CSV
        MenuBar.importer_xlsx = QAction(tr('importer') + ' XLSX', delegue_master)
        MenuBar.importer_xlsx.triggered.connect(self.importer_xlsx_action)
        MenuBar.menu_importer.addAction(MenuBar.importer_xlsx)

        # Importer CSV
        MenuBar.importer_csv = QAction(tr('importer') + ' CSV', delegue_master)
        MenuBar.importer_csv.triggered.connect(self.importer_csv_action)
        MenuBar.menu_importer.addAction(MenuBar.importer_csv)

        # Importer TXT
        MenuBar.importer_txt = QAction(tr('importer') + ' TXT', delegue_master)
        MenuBar.importer_txt.triggered.connect(self.importer_txt_action)
        MenuBar.menu_importer.addAction(MenuBar.importer_txt)

        MenuBar.menu_importer.addSeparator()

        # Importer du texte qui est soit un fichier CSV, soit un fichier TXT
        MenuBar.importer_texte = QAction(tr('importer_texte'), delegue_master)
        MenuBar.importer_texte.triggered.connect(self.importer_texte_action)
        MenuBar.menu_importer.addAction(MenuBar.importer_texte)

        # Sous-menu Exporter
        MenuBar.menu_exporter = MenuBar.menu_fichier.addMenu(tr('exporter'))
        MenuBar.menu_fichier.addMenu(MenuBar.menu_exporter)

        # Exporter CSV
        MenuBar.exporter_csv = QAction(tr('exporter') + ' CSV', delegue_master)
        MenuBar.exporter_csv.triggered.connect(self.exporter_csv_action)
        MenuBar.menu_exporter.addAction(MenuBar.exporter_csv)

        # Exporter TXT
        MenuBar.exporter_txt = QAction(tr('exporter') + ' TXT', delegue_master)
        MenuBar.exporter_txt.triggered.connect(self.exporter_txt_action)
        MenuBar.menu_exporter.addAction(MenuBar.exporter_txt)

        MenuBar.menu_fichier.addSeparator()

        # Exporter PDF
        MenuBar.exporter_pdf = QAction(tr('exporter') + ' PDF', delegue_master)
        MenuBar.exporter_pdf.triggered.connect(self.exporter_pdf_action)
        MenuBar.menu_exporter.addAction(MenuBar.exporter_pdf)

        # Action Paramètres
        MenuBar.parametres = QAction(tr('parametres'), delegue_master)
        MenuBar.parametres.setShortcut('Ctrl+P')
        MenuBar.parametres.triggered.connect(self.afficher_parametres_action)
        MenuBar.menu_fichier.addAction(MenuBar.parametres)

        MenuBar.menu_fichier.addSeparator()

        # Action Quitter
        MenuBar.quitter = QAction(tr('quitter'), delegue_master)
        MenuBar.quitter.setShortcut('Alt+F4')
        MenuBar.quitter.triggered.connect(delegue_master.close)
        MenuBar.menu_fichier.addAction(MenuBar.quitter)

        # MENU EDITION
        MenuBar.menu_edition = menubar.addMenu(tr('edition'))

        # MENU ELEVES
        MenuBar.menu_eleves = menubar.addMenu(tr('eleves'))

        # Action Ajouter Élève
        self.ajouter_eleve = QAction(tr('ajouter_eleve'), delegue_master)
        self.ajouter_eleve.setShortcut('Ctrl+E')
        MenuBar.menu_eleves.addAction(self.ajouter_eleve)

        # Action Supprimer Élève
        self.supprimer_eleve = QAction(tr('supprimer_eleve'), delegue_master)
        self.supprimer_eleve.setShortcut('Del')
        self.supprimer_eleve.setEnabled(False)
        MenuBar.menu_eleves.addAction(self.supprimer_eleve)

    # Méthode appelée lors de l'action Nouveau
    def nouveau_action(self):
        # On demande à l'utilisateur s'il souhaite supprimer les données actuelles
        if self.delegue_master.getElevesTab().nombre_eleves() > 0:
            # Affichage d'une boîte de dialogue de confirmation
            resultat = QMessageBox.question(self.delegue_master, self.delegue_master.langues.tr('confirmer'), self.delegue_master.langues.tr('message_confirmation_suppression'),QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if resultat == QMessageBox.StandardButton.Yes:  # Si l'utilisateur confirme
                self.delegue_master.setClasse(Classe())
            elif resultat == QMessageBox.StandardButton.No:  # Si l'utilisateur annule
                return False
        else:
            self.delegue_master.setClasse(Classe())

        self.db_file_open = None

        self.delegue_master.profile.emplacement_fichier_db = ""
        self.delegue_master.profile.enregistrer_fichier()
        return True

    def ouvrir_action(self):
        # Ouvrir une boîte de dialogue pour sélectionner un fichier de base de données SQLite
        self.db_file_open, _ = QFileDialog.getOpenFileName(self.delegue_master,
                                                           self.delegue_master.langues.tr('ouvrir') + ' .db',
                                                           self.delegue_master.profile.emplacement_ouvrir,
                                                           'SQLite Database (*.db)')
        if self.db_file_open:
            if self.ouvrir_fichier(self.db_file_open):
                # Afficher un message de confirmation
                QMessageBox.information(self.delegue_master, self.delegue_master.langues.tr('succes'),
                                        self.delegue_master.langues.tr('donnes_importees') + self.db_file_open)

    def ouvrir_fichier(self, db_file_open):
        try:
            classe = ouvrir_db(db_file_open)

            # Mettre à jour la classe dans le profil de l'utilisateur
            self.delegue_master.setClasse(classe)

            # Mettre à jour l'emplacement de la dernière ouverture dans le profil de l'utilisateur
            self.delegue_master.profile.emplacement_ouvrir = os.path.dirname(db_file_open)
            self.delegue_master.profile.emplacement_fichier_db = db_file_open
            self.delegue_master.profile.enregistrer_fichier()

            return True

        except Exception as e:
            # En cas d'erreur, afficher un message d'erreur
            QMessageBox.critical(self.delegue_master, self.delegue_master.langues.tr('erreur'),
                                 self.delegue_master.langues.tr('message_erreur') + str(e))

    def enregistrer_action(self):
        # Vérifier si un fichier de base de données est déjà ouvert
        if self.db_file_open:
            # Si oui, copier le fichier temporaire vers le fichier ouvert
            sauvegarder_db(self.db_file_open, self.delegue_master.getClasse())
            
            self.delegue_master.profile.emplacement_fichier_db = self.db_file_open
            self.delegue_master.profile.enregistrer_fichier()
        else:  # Si non, appeler la fonction pour enregistrer sous
            self.enregistrer_sous_action()

    def enregistrer_sous_action(self):
        # Ouvrir une boîte de dialogue pour choisir l'emplacement de sauvegarde et le nom du fichier
        file_dialog = QFileDialog()
        # mettre le nomd u 
        #file_dialog.set
        dossier_enregistrement, _ = file_dialog.getSaveFileName(self.delegue_master,
                                                                self.delegue_master.langues.tr('enregistrer_sous'),
                                                                self.delegue_master.profile.emplacement_enregistrer_sous + '/' + self.delegue_master.getClasse().get_nom() + '.db',
                                                                'SQLite Files (*.db)')
        if dossier_enregistrement:
            # Si un emplacement de sauvegarde est sélectionné
            self.db_file_open = dossier_enregistrement
            
            # créer db
            sauvegarder_db(self.db_file_open, self.delegue_master.getClasse())
            
            # Mettre à jour l'emplacement de sauvegarde dans le profil de l'utilisateur
            self.delegue_master.profile.emplacement_enregistrer_sous = os.path.dirname(self.db_file_open)
            self.delegue_master.profile.emplacement_fichier_db = self.db_file_open
            self.delegue_master.profile.enregistrer_fichier()

    def exporter_action(self):
        # Obtient la traduction pour la langue sélectionnée
        tr = self.delegue_master.langues.tr

<<<<<<< HEAD
        # Crée une boîte de dialogue pour choisir les semestres à exporter en PDF
        dialog = QDialog(self.delegue_master)
        dialog.setWindowIcon(QIcon("logo.png"))  # Définit une icône pour la boîte de dialogue
        dialog.setWindowTitle('Exporter')  # Définit le titre de la boîte de dialogue
        layout = QVBoxLayout(dialog)  # Crée un layout vertical pour la boîte de dialogue
        
        # Ajoute un label pour indiquer à l'utilisateur de sélectionner les semestres à exporter
        layout.addWidget(QLabel('Exporter par Éleve et/ou Classe'))
        
        par_eleve_checkbox = QCheckBox('Exporter par Éleve', self.delegue_master)
        par_classe_checkbox = QCheckBox('Exporter par Classe', self.delegue_master)
        eleves_checkboxs = [par_eleve_checkbox, par_classe_checkbox]
        layout.addWidget(par_eleve_checkbox)
        layout.addWidget(par_classe_checkbox)

        # Ajoute un label pour indiquer à l'utilisateur de sélectionner les semestres à exporter
        layout.addWidget(QLabel('Selectionner les fichiers à exporter'))
        
        txt_checkbox = QCheckBox('Exporter TXT', self.delegue_master)
        csv_checkbox = QCheckBox('Exporter CSV', self.delegue_master)
        pdf_checkbox = QCheckBox('Exporter PDF', self.delegue_master)
        fichiers_checkboxs = [txt_checkbox, csv_checkbox, pdf_checkbox]
        layout.addWidget(txt_checkbox)
        layout.addWidget(csv_checkbox)
        layout.addWidget(pdf_checkbox)
        
        periodes_checkboxs = []
        nb_periodes = self.delegue_master.getClasse().get_nb_periodes()
        for i in range(nb_periodes):
            checkbox_periode = QCheckBox('Période ' + str(i+1), self.delegue_master)
            periodes_checkboxs.append(checkbox_periode)
            layout.addWidget(checkbox_periode)
    
        
        # Ajoute un bouton pour valider l'exportation du PDF
        bouton_valider = QPushButton(tr('exporter'), self.delegue_master)
        # Connecte le clic du bouton à la fonction d'exportation du PDF en utilisant les paramètres choisis
        bouton_valider.clicked.connect(lambda: self.exporter(self.delegue_master, eleves_checkboxs, fichiers_checkboxs, periodes_checkboxs, dialog))
        layout.addWidget(bouton_valider)

        dialog.setLayout(layout)  # Applique le layout à la boîte de dialogue
        dialog.exec()  # Affiche la boîte de dialogue et attend que l'utilisateur interagisse avec
        
    def exporter(self, delegue_master, eleves_checkboxs, fichiers_checkboxs, periodes_checkboxs, dialog):
        # on choisit le dossier ou on enregistre le fichier
        dossier = QFileDialog.getExistingDirectory(self.delegue_master, 'Exporter')
        dossier_classe = os.path.join(dossier, self.delegue_master.getClasse().get_nom())
        os.makedirs(dossier_classe)
            
        for eleve_checkbox in eleves_checkboxs:
            if eleve_checkbox.isChecked():
                for fichier_checkbox in fichiers_checkboxs:
                    if fichier_checkbox.isChecked():
                        if fichier_checkbox.text() == 'Exporter TXT':
                            exporter_txt(delegue_master, dossier_classe, periodes_checkboxs, True)
                        elif fichier_checkbox.text() == 'Exporter CSV':
                            exporter_csv(delegue_master, dossier_classe)
                        elif fichier_checkbox.text() == 'Exporter PDF':
                            exporter_pdf(delegue_master, dossier_classe, periodes_checkboxs, dialog)
                            
    def exporter_pdf_action(self):
        # Obtient la traduction pour la langue sélectionnée
        tr = self.delegue_master.langues.tr

=======
>>>>>>> dc682bbcb658d6e2427319f7e6d1c93c16bddda1
        # Crée une boîte de dialogue pour choisir les semestres à exporter en PDF
        dialog = QDialog(self.delegue_master)
        dialog.setWindowIcon(QIcon("logo.png"))  # Définit une icône pour la boîte de dialogue
        dialog.setWindowTitle(tr('choisir_semestre'))  # Définit le titre de la boîte de dialogue
        layout = QVBoxLayout(dialog)  # Crée un layout vertical pour la boîte de dialogue

        # Ajoute un label pour indiquer à l'utilisateur de sélectionner les semestres à exporter
        layout.addWidget(QLabel(tr('selectionner_semestre_exporter')))
        
        checkboxs = []
        nb_periodes = self.delegue_master.getClasse().get_nb_periodes()
        for i in range(nb_periodes):
            checkbox_periode = QCheckBox('Période ' + str(i+1), self.delegue_master)
            checkboxs.append(checkbox_periode)
            layout.addWidget(checkbox_periode)

        # Ajoute un bouton pour valider l'exportation du PDF
        bouton_valider = QPushButton(tr('exporter'), self.delegue_master)
        # Connecte le clic du bouton à la fonction d'exportation du PDF en utilisant les paramètres choisis
<<<<<<< HEAD
    
=======
>>>>>>> dc682bbcb658d6e2427319f7e6d1c93c16bddda1
        bouton_valider.clicked.connect(lambda: exporter_pdf(self.delegue_master, tr, checkboxs, dialog))
        layout.addWidget(bouton_valider)

        dialog.setLayout(layout)  # Applique le layout à la boîte de dialogue
        dialog.exec()  # Affiche la boîte de dialogue et attend que l'utilisateur interagisse avec
        
    def importer_texte_action(self):
        # Ouvre une fenêtre de dialogue avec un QTextEdit et un bouton d'importation
        dialog = QDialog()
        dialog.setWindowTitle(self.delegue_master.langues.tr('importer_texte_titre'))

        text_edit = QTextEdit(dialog)
        importer_button = QPushButton(self.delegue_master.langues.tr('importer_texte_bouton'), dialog)
        # Connecte le clic du bouton à la fonction de conversion de texte en CSV ou TXT
        importer_button.clicked.connect(lambda: self.convertir_texte_csv_ou_txt(text_edit.toPlainText()))
        importer_button.clicked.connect(dialog.close)

        layout = QVBoxLayout(dialog)
        layout.addWidget(text_edit)
        layout.addWidget(importer_button)

        dialog.setLayout(layout)
        dialog.setWindowIcon(QIcon("logo.png"))
        dialog.exec()

        apply_stylesheet(dialog, theme=self.delegue_master.themes.convertir_theme_int_en_str())

    def convertir_texte_csv_ou_txt_action(self, texte):
        # Efface la table des élèves
        self.delegue_master.recup_onglet_eleves().effacer_table()

        # Divise le texte en lignes
        lignes = texte.split('\n')

        # Convertit le texte en CSV ou TXT en fonction du délimiteur
        if ';' in texte:
            for line in lignes:
                data = line.strip().split(';')
                self.delegue_master.recup_onglet_eleves().ajouter_eleve(data[0], data[1])
        else:
            for line in lignes:
                data = line.strip().split(' ')
                self.delegue_master.recup_onglet_eleves().ajouter_eleve(data[0], data[1])

    def importer_xlsx_action(self):
        #self.nouveau_action()
        file_path, _ = QFileDialog.getOpenFileName(self.delegue_master, "Importer un fichier Excel", "", "Fichiers Excel (*.xlsx)")
        if file_path:
            importer_xlsx(self.delegue_master, file_path)

    def importer_csv_action(self):
        file_dialog = QFileDialog()
        tr = self.delegue_master.langues.tr
        nom_fichier, _ = file_dialog.getOpenFileName(self.delegue_master, tr('importer_csv'), '', 'CSV Files (*.csv)')
        importer_csv(nom_fichier)
    
    def exporter_csv_action(self):
        fichier = QFileDialog()
        tr = self.delegue_master.langues.tr
        nom_fichier, _ = fichier.getSaveFileName(self.delegue_master, tr('exporter_csv'), '', 'CSV Files (*.csv)')
        exporter_csv(nom_fichier)
        
    def importer_txt_action(self):
        fichier = QFileDialog()
        tr = self.delegue_master.langues.tr
        nom_fichier, _ = fichier.getOpenFileName(self.delegue_master, tr('importer_txt'), '', 'TXT Files (*.txt)')
        importer_txt(self.delegue_master, nom_fichier)

    def exporter_txt_action(self):
        fichier = QFileDialog()
        tr = self.delegue_master.langues.tr
        nom_fichier, _ = fichier.getSaveFileName(self.delegue_master, tr('exporter_txt'), '', 'TXT Files (*.txt)')
        exporter_txt(self.delegue_master, nom_fichier, True)

    def afficher_parametres_action(self):
        parametres_dialog = SettingsDialog(self.delegue_master)
        parametres_dialog.exec()

    def changer_langue(self):
        # On actualise dynamiquement les textes dans les menus
        tr = self.delegue_master.langues.tr

        MenuBar.menu_fichier.setTitle(tr('fichier'))
        MenuBar.nouveau.setText(tr('nouveau'))
        MenuBar.ouvrir.setText(tr('ouvrir'))
        MenuBar.enregistrer.setText(tr('enregistrer'))
        MenuBar.enregistrer_sous.setText(tr('enregistrer_sous'))

        MenuBar.menu_importer.setTitle(tr('importer'))
        MenuBar.importer_csv.setText(tr('importer') + ' CSV')
        MenuBar.importer_txt.setText(tr('importer') + ' TXT')
        MenuBar.importer_texte.setText(tr('importer_texte'))

        MenuBar.menu_exporter.setTitle(tr('exporter'))
        MenuBar.exporter_csv.setText(tr('exporter') + ' CSV')
        MenuBar.exporter_txt.setText(tr('exporter') + ' TXT')
        MenuBar.exporter_pdf.setText(tr('exporter') + ' PDF')

        MenuBar.parametres.setText(tr('parametres'))

        MenuBar.quitter.setText(tr('quitter'))

        MenuBar.menu_edition.setTitle(tr('edition'))

        MenuBar.menu_eleves.setTitle(tr('eleves'))
        MenuBar.ajouter_eleve.setText(tr('ajouter_eleve'))
        self.supprimer_eleve.setText(tr('supprimer_eleve'))

