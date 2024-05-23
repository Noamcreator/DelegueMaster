# Importation des modules nécessaires
import csv  # Module pour la manipulation de fichiers CSV
import os  # Module pour les opérations sur le système d'exploitation
import shutil  # Module pour la manipulation de fichiers et de répertoires
import sqlite3  # Module pour l'interaction avec les bases de données SQLite

# Importations PyQt6 pour l'interface graphique
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMessageBox, QFileDialog, QTextEdit, QPushButton, QVBoxLayout, QDialog, QTableWidgetItem, \
    QCheckBox, QLabel
# Importation de la fonction pour appliquer un thème à l'interface
from qt_material import apply_stylesheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from core.classe import Classe
from database.db_handler import creer_db, ouvrir_db, sauvegarder_db
from ui.import_eleves_dialog import ImportElevesDialog

from .settings_dialog import SettingsDialog

# Importation de la boîte de dialogue des paramètres


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

        # Renseignement de la police de caractères pour l'export PDF
        #script_dir = os.path.dirname(os.path.abspath(__file__).replace("code", ""))
        #police = os.path.join(script_dir, 'ressources\\', 'Roboto-Regular.ttf')
        #pdfmetrics.registerFont(TTFont('Roboto-Regular', police))

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
        MenuBar.ajouter_eleve = QAction(tr('ajouter_eleve'), delegue_master)
        MenuBar.ajouter_eleve.setShortcut('Ctrl+E')
        #MenuBar.ajouter_eleve.triggered.connect(delegue_master.recup_onglet_eleves().ajouter_eleve_dialog)
        MenuBar.menu_eleves.addAction(MenuBar.ajouter_eleve)

        # Action Supprimer Élève
        self.supprimer_eleve = QAction(tr('supprimer_eleve'), delegue_master)
        self.supprimer_eleve.setShortcut('Del')
        self.supprimer_eleve.setEnabled(False)
        #self.supprimer_eleve.triggered.connect(delegue_master.recup_onglet_eleves().supprimer_eleve)
        MenuBar.menu_eleves.addAction(self.supprimer_eleve)

    # Méthode appelée lors de l'action Nouveau
    def nouveau_action(self):
        # On demande à l'utilisateur s'il souhaite supprimer les données actuelles
        if self.delegue_master.getElevesTab().nombre_eleves() > 0:
            # Affichage d'une boîte de dialogue de confirmation
            resultat = QMessageBox.question(self.delegue_master, self.delegue_master.langues.tr('confirmer'),
                                            self.delegue_master.langues.tr('message_confirmation_suppression'),
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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

    def exporter_pdf_action(self):
        # Obtient la traduction pour la langue sélectionnée
        tr = self.delegue_master.langues.tr

        # Crée des cases à cocher pour les semestres
        checkbox_semestre1 = QCheckBox(tr('semestre_1'), self.delegue_master)
        checkbox_semestre2 = QCheckBox(tr('semestre_2'), self.delegue_master)

        # Crée une boîte de dialogue pour choisir les semestres à exporter en PDF
        dialog = QDialog(self.delegue_master)
        dialog.setWindowIcon(QIcon("logo.png"))  # Définit une icône pour la boîte de dialogue
        dialog.setWindowTitle(tr('choisir_semestre'))  # Définit le titre de la boîte de dialogue
        layout = QVBoxLayout(dialog)  # Crée un layout vertical pour la boîte de dialogue

        # Ajoute un label pour indiquer à l'utilisateur de sélectionner les semestres à exporter
        layout.addWidget(QLabel(tr('selectionner_semestre_exporter')))
        # Ajoute les cases à cocher pour les semestres au layout
        layout.addWidget(checkbox_semestre1)
        layout.addWidget(checkbox_semestre2)

        # Ajoute un bouton pour valider l'exportation du PDF
        bouton_valider = QPushButton(tr('exporter'), self.delegue_master)
        # Connecte le clic du bouton à la fonction d'exportation du PDF en utilisant les paramètres choisis
        bouton_valider.clicked.connect(
            lambda: self.exporter_fichier_pdf(tr, checkbox_semestre1.isChecked(), checkbox_semestre2.isChecked(),
                                              dialog))
        layout.addWidget(bouton_valider)

        dialog.setLayout(layout)  # Applique le layout à la boîte de dialogue
        dialog.exec()  # Affiche la boîte de dialogue et attend que l'utilisateur interagisse avec

    def exporter_fichier_pdf(self, tr, semestre1_selected, semestre2_selected, dialog):
        if semestre1_selected or semestre2_selected:
            try:
                # Continuer avec l'exportation selon les choix de l'utilisateur
                dossier_pdf, _ = QFileDialog.getSaveFileName(self.delegue_master, tr('exporter_pdf'), tr('conseils'),
                                                             'PDF Files (*.pdf)')
                if dossier_pdf:
                    # Création d'un document PDF avec encodage UTF-8 et la police Plex Mono
                    doc = SimpleDocTemplate(dossier_pdf, pagesize=letter, encoding='utf-8')

                    # Style pour le texte en gras
                    styles = getSampleStyleSheet()
                    bold_style = styles['Normal']
                    bold_style.fontName = 'Roboto-Regular'

                    # Contenu du document PDF
                    elements = []

                    # Connexion à la base de données
                    conn = sqlite3.connect(self.delegue_master.db_temp_file)
                    cursor = conn.cursor()

                    # Récupération des données des élèves en fonction des choix de l'utilisateur
                    cursor.execute(
                        "SELECT e.nom, e.prenom, s1.remarques, s1.moyennes, s1.mentions, s2.remarques, s2.moyennes, s2.mentions FROM eleves e JOIN semestre1 s1 ON e.idEleves = s1.idEleves JOIN semestre2 s2 ON e.idEleves = s2.idEleves")

                    eleves = cursor.fetchall()

                    # Style du tableau
                    table_style = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])

                    for eleve in eleves:
                        # Création du tableau pour chaque élève

                        if semestre1_selected and semestre2_selected:
                            data = [
                                [Paragraph('<b>' + eleve[0] + ' ' + eleve[1] + '</b>', bold_style),
                                 Paragraph(tr('remarque'), styles['Normal']),
                                 Paragraph(tr('moyenne'), styles['Normal']),
                                 Paragraph(tr('mention'), styles['Normal'])],

                                [Paragraph(tr('semestre_1'), styles['Normal']),
                                 Paragraph(eleve[2] if eleve[2] else "", styles['Normal']),
                                 Paragraph(str(eleve[3]) if eleve[3] is not None else "0.0", styles['Normal']),
                                 Paragraph(tr('appreciations')[eleve[4]] if eleve[4] else tr('appreciations')[0],
                                           styles['Normal'])],

                                [Paragraph(tr('semestre_2'), styles['Normal']),
                                 Paragraph(eleve[5] if eleve[5] else "", styles['Normal']),
                                 Paragraph(str(eleve[6]) if eleve[6] else "0.0", styles['Normal']),
                                 Paragraph(tr('appreciations')[eleve[7]] if eleve[7] else tr('appreciations')[0],
                                           styles['Normal'])]
                            ]

                        elif semestre1_selected:
                            data = [
                                [Paragraph('<b>' + eleve[0] + ' ' + eleve[1] + '</b>', bold_style),
                                 Paragraph(tr('remarque'), styles['Normal']),
                                 Paragraph(tr('moyenne'), styles['Normal']),
                                 Paragraph(tr('mention'), styles['Normal'])],

                                [Paragraph(tr('semestre_1'), styles['Normal']),
                                 Paragraph(eleve[2] if eleve[2] else "", styles['Normal']),
                                 Paragraph(str(eleve[3]) if eleve[3] is not None else "0.0", styles['Normal']),
                                 Paragraph(tr('appreciations')[eleve[4]] if eleve[4] else tr('appreciations')[0],
                                           styles['Normal'])]
                            ]

                        else:
                            data = [
                                [Paragraph('<b>' + eleve[0] + ' ' + eleve[1] + '</b>', bold_style),
                                 Paragraph(tr('remarque'), styles['Normal']),
                                 Paragraph(tr('moyenne'), styles['Normal']),
                                 Paragraph(tr('mention'), styles['Normal'])],

                                [Paragraph(tr('semestre_2'), styles['Normal']),
                                 Paragraph(eleve[5] if eleve[5] else "", styles['Normal']),
                                 Paragraph(str(eleve[6]) if eleve[6] else "0.0", styles['Normal']),
                                 Paragraph(tr('appreciations')[eleve[7]] if eleve[7] else tr('appreciations')[0],
                                           styles['Normal'])]
                            ]

                        # Création du tableau
                        table = Table(data)
                        table.setStyle(table_style)

                        # Ajout du tableau au contenu du PDF
                        elements.append(table)

                        # Ajout d'un espace entre chaque élève
                        elements.append(Spacer(1, 12))

                    # Fermeture de la connexion à la base de données
                    conn.close()

                    # Génération du PDF
                    doc.build(elements)

                    QMessageBox.information(self.delegue_master, tr('succes'), tr('message_pdf') + dossier_pdf)

                    dialog.close()
            except Exception as e:
                QMessageBox.critical(self.delegue_master, tr('erreur'), tr('message_erreur') + str(e))
        else:
            QMessageBox.warning(self.delegue_master, tr('avertissement'),
                                tr('aucun_semestre_selectionne'))

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
        import_eleves_dialog = ImportElevesDialog(self.delegue_master)
        import_eleves_dialog.show()

    def importer_csv_action(self):
        file_dialog = QFileDialog()
        tr = self.delegue_master.langues.tr
        nom_fichier, _ = file_dialog.getOpenFileName(self.delegue_master, tr('importer_csv'), '', 'CSV Files (*.csv)')
        self.importer_csv(nom_fichier)
    
    def importer_csv(self, nom_fichier):
        if nom_fichier:
            try:
                with open(nom_fichier, newline='', encoding='utf-8') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=';')
                    self.delegue_master.recup_onglet_eleves().effacer_table()

                    # Ignorer la première ligne (en-tête)
                    next(csvreader)

                    for row, data in enumerate(csvreader):
                        self.delegue_master.recup_onglet_eleves().ajouter_eleve(data[0], data[1])

                QMessageBox.information(self.delegue_master, tr('succes'),
                                        tr('donnes_importees') + nom_fichier)
            except Exception as e:
                QMessageBox.critical(self.delegue_master, tr('erreur'),
                                     tr('message_erreur') + str(e))

    def exporter_csv_action(self):
        fichier = QFileDialog()
        tr = self.delegue_master.langues.tr
        nom_fichier, _ = fichier.getSaveFileName(self.delegue_master, tr('exporter_csv'), '', 'CSV Files (*.csv)')
        if nom_fichier:
            try:
                with open(nom_fichier, 'w', newline='', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=';')
                    # Ecrire la première ligne (en-tête)
                    csvwriter.writerow(['NOMS', 'Prenoms'])
                    for row in range(self.delegue_master.recup_onglet_eleves().recup_table().rowCount()):
                        data = []
                        for col in range(self.delegue_master.recup_onglet_eleves().recup_table().columnCount()):
                            item = self.delegue_master.recup_onglet_eleves().recup_table().item(row, col)
                            if item is not None:
                                data.append(item.text())
                            else:
                                data.append('')
                        csvwriter.writerow(data)

                QMessageBox.information(self.delegue_master, tr('succes'),
                                        tr('donnes_exportees') + nom_fichier)
            except Exception as e:
                QMessageBox.critical(self.delegue_master, tr('erreur'), tr('message_erreur') + str(e))

    def importer_txt_action(self):
        fichier = QFileDialog()
        tr = self.delegue_master.langues.tr
        nom_fichier, _ = fichier.getOpenFileName(self.delegue_master, tr('importer_txt'), '', 'TXT Files (*.txt)')
        if nom_fichier:
            try:
                with open(nom_fichier, 'r', encoding='utf-8') as txtfile:
                    self.delegue_master.recup_onglet_eleves().effacer_table()

                    for line in txtfile:
                        data = line.strip().split(' ')
                        self.delegue_master.recup_onglet_eleves().ajouter_eleve(data[0], data[1])

                QMessageBox.information(self.delegue_master, tr('succes'),
                                        tr('donnes_importees') + nom_fichier)
            except Exception as e:
                QMessageBox.critical(self.delegue_master, tr('erreur'),
                                     tr('message_erreur') + str(e))

    def exporter_txt_action(self):
        fichier = QFileDialog()
        tr = self.delegue_master.langues.tr
        nom_fichier, _ = fichier.getSaveFileName(self.delegue_master, tr('exporter_txt'), '', 'TXT Files (*.txt)')
        if nom_fichier:
            try:
                with open(nom_fichier, 'w', encoding='utf-8') as txtfile:
                    for row in range(self.delegue_master.recup_onglet_eleves().recup_table().rowCount()):
                        data = []
                        for col in range(self.delegue_master.recup_onglet_eleves().recup_table().columnCount()):
                            item = self.delegue_master.recup_onglet_eleves().recup_table().item(row, col)
                            if item is not None:
                                data.append(item.text())
                            else:
                                data.append('')
                        if row != 0:
                            txtfile.write('\n')
                        txtfile.write(' '.join(data))

                QMessageBox.information(self.delegue_master, tr('succes'), tr('donnes_exportees') + nom_fichier)
            except Exception as e:
                QMessageBox.critical(self.delegue_master, tr('erreur'), tr('message_erreur') + str(e))

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

