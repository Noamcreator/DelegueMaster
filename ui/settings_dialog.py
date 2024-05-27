import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QComboBox, QTabWidget, QVBoxLayout, QWidget, QHBoxLayout, \
    QCheckBox, QDoubleSpinBox, QPushButton, QLineEdit, QInputDialog
from qt_material import apply_stylesheet, QtStyleTools


class SettingsDialog(QDialog):
    def __init__(self, delegue_master):
        super().__init__(delegue_master)
        self.delegue_master = delegue_master

        # Module de traduction pour les langues
        tr = self.delegue_master.langues.tr

        # Définition de la taille de la fenêtre
        self.setGeometry(100, 100, 500, 200)

        # Centrer la fenêtre sur l'écran
        self.move(self.screen().geometry().center() - self.rect().center())

        # Layout principal de la fenêtre
        layout_principal = QVBoxLayout(self)

        # Onglets de paramètres
        SettingsDialog.onglets_parametre = QTabWidget()

        # Onglet pour les paramètres généraux
        onglet_general = QWidget()
        onglet_general_layout = QGridLayout()
        onglet_general.setLayout(onglet_general_layout)

        # Label pour la note maximale
        SettingsDialog.label_note_max = QLabel(tr('note_max') + ":")
        onglet_general_layout.addWidget(SettingsDialog.label_note_max, 0, 0)

        # Zone de saisie pour la note maximale
        note_maximum = QDoubleSpinBox()
        note_maximum.setValue(self.delegue_master.profile.note_max)
        note_maximum.valueChanged.connect(lambda value: self.changer_note_maximum(value))
        onglet_general_layout.addWidget(note_maximum, 0, 1)
        
        # Onglet pour les appréciations
        onglet_appreciations = QWidget()
        onglet_appreciations_layout = QVBoxLayout()
        onglet_appreciations.setLayout(onglet_appreciations_layout)

        self.appreciations_combo = QComboBox()
        self.appreciations_combo.addItems(self.delegue_master.profile.appreciations)
        onglet_appreciations_layout.addWidget(self.appreciations_combo)

        ajouter_appreciation_bouton = QPushButton(tr('ajouter_appreciation'))
        ajouter_appreciation_bouton.clicked.connect(self.ajouter_appreciation)
        onglet_appreciations_layout.addWidget(ajouter_appreciation_bouton)

        # Onglet pour les langues
        onglet_langues = QWidget()
        onglet_langues_layout = QGridLayout()
        onglet_langues.setLayout(onglet_langues_layout)

        langue_combo = QComboBox()  # ComboBox pour les langues
        langue_combo.addItems(self.delegue_master.langues.langues_noms)
        index = self.delegue_master.langues.langues.index(self.delegue_master.profile.langue)
        langue_combo.setCurrentIndex(index)
        langue_combo.currentIndexChanged.connect(lambda index: self.changer_langue(index))
        onglet_langues_layout.addWidget(langue_combo)

        # Onglet pour les thèmes
        onglet_themes = QWidget()
        onglet_themes_layout = QHBoxLayout()
        onglet_themes.setLayout(onglet_themes_layout)

        self.themes_combo = QComboBox()
        self.bouton_sombre = QCheckBox(tr('sombre'))
        self.bouton_sombre.setChecked(self.delegue_master.profile.dark)

        self.light_colors = self.delegue_master.themes.light_color()
        self.dark_colors = self.delegue_master.themes.dark_color()

        if self.bouton_sombre.isChecked():  # Sombre
            self.themes_combo.addItems(self.dark_colors)
        else:
            self.themes_combo.addItems(self.light_colors)

        self.themes_combo.setCurrentIndex(self.delegue_master.profile.theme)

        self.bouton_sombre.toggled.connect(lambda checked: self.change_clair_sombre(self.themes_combo.currentIndex()))
        self.themes_combo.currentIndexChanged.connect(
            lambda index: self.changer_theme(self.themes_combo.currentIndex()))

        self.bouton_personalisation = QPushButton("+")
        self.bouton_personalisation.clicked.connect(lambda: self.personalisation())

        onglet_themes_layout.addWidget(self.themes_combo)
        onglet_themes_layout.addWidget(self.bouton_sombre)
        # onglet_themes_layout.addWidget(self.bouton_personalisation)

        # Ajout des onglets à la fenêtre principale
        SettingsDialog.onglets_parametre.addTab(onglet_general, tr('generale'))
        SettingsDialog.onglets_parametre.addTab(onglet_appreciations, tr('appreciation'))  # Ajouter onglet appréciations
        SettingsDialog.onglets_parametre.addTab(onglet_langues, tr('langues'))
        SettingsDialog.onglets_parametre.addTab(onglet_themes, tr('themes'))

        layout_principal.addWidget(SettingsDialog.onglets_parametre)

        # Configuration du titre et de l'icône de la fenêtre
        self.setWindowTitle(tr('parametres'))

    # Méthode appelée lorsqu'une modification de la note maximale est effectuée
    def changer_note_maximum(self, value):
        # Mise à jour de la note maximale dans le profil
        self.delegue_master.profile.note_max = value
        # Enregistrement du profil mis à jour
        self.delegue_master.profile.enregistrer_fichier()
        # Appel d'une méthode pour mettre à jour l'affichage des conseils
        self.delegue_master.recup_onglet_conseils().changer_note_maximum()

    # Méthode pour nettoyer le cache
    # Méthode appelée lorsqu'une langue est sélectionnée
    def changer_langue(self, index):
        # Changement de la langue dans le profil
        langue_actuelle = self.delegue_master.langues.changer_langue(index)
        self.delegue_master.profile.langue = langue_actuelle
        # Enregistrement du profil mis à jour
        self.delegue_master.profile.enregistrer_fichier()

        # Mise à jour des textes dans les onglets avec la nouvelle langue
        self.mettre_a_jour_textes()

    def mettre_a_jour_textes(self):
        tr = self.delegue_master.langues.tr
        SettingsDialog.onglets_parametre.setTabText(0, tr('generale'))
        SettingsDialog.onglets_parametre.setTabText(1, tr('appreciation'))
        SettingsDialog.onglets_parametre.setTabText(2, tr('langues'))
        SettingsDialog.onglets_parametre.setTabText(3, tr('themes'))
        self.setWindowTitle(tr('parametres'))
        SettingsDialog.label_note_max.setText(tr('note_max') + ":")
        SettingsDialog.label_classe.setText(tr('classe') + ":")
        ajouter_appreciation_bouton.setText(tr('ajouter_appreciation'))
        self.bouton_sombre.setText(tr('sombre'))

    def ajouter_appreciation(self):
        tr = self.delegue_master.langues.tr
        text, ok = QInputDialog.getText(self, tr('ajouter_appreciation'), tr('entrer_appreciation'))
        if ok and text:
            self.delegue_master.profile.appreciations.append(text)
            self.delegue_master.profile.enregistrer_fichier()
            self.appreciations_combo.addItem(text)

    def changer_theme(self, index):
        self.delegue_master.profile.theme = index
        self.delegue_master.profile.enregistrer_fichier()
        apply_stylesheet(self.delegue_master, theme=self.delegue_master.themes.convertir_theme_int_en_str())

    def change_clair_sombre(self, index):
        self.delegue_master.profile.dark = self.bouton_sombre.isChecked()
        self.themes_combo.clear()
        if self.bouton_sombre.isChecked():
            self.themes_combo.addItems(self.dark_colors)
        else:
            self.themes_combo.addItems(self.light_colors)
        self.themes_combo.setCurrentIndex(index)
        self.changer_theme(index)

    def personalisation(self):
        tr = self.delegue_master.langues.tr
        text, ok = QInputDialog.getText(self, tr('personnalisation'), tr('entrer_nom_theme'))
        if ok and text:
            if self.bouton_sombre.isChecked():
                self.dark_colors.append(text)
            else:
                self.light_colors.append(text)
            self.themes_combo.addItem(text)
            self.themes_combo.setCurrentIndex(self.themes_combo.count() - 1)
            self.changer_theme(self.themes_combo.currentIndex())

