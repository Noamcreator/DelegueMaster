from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QLineEdit, QTabWidget, QLabel, QTabBar, QDoubleSpinBox, QPushButton
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon

class ConseilsTab(QWidget):
    def __init__(self, delegue_master):
        super().__init__()

        self.delegue_master = delegue_master
        tr = self.delegue_master.langues.tr

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Création de QTabWidget pour contenir les onglets "Classe" et "Élèves"
        self.conseils_tab = QTabWidget()
        self.layout.addWidget(self.conseils_tab)
        
        # Ajout du minuteur
        self.timer_label = QLabel()
        self.layout.addWidget(self.timer_label)

        # Initialisation du minuteur
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.seconds_elapsed = 0

        # Onglet "Classe"
        self.classe_tab = QWidget()
        self.classe_layout = QVBoxLayout()
        self.classe_tab.setLayout(self.classe_layout)

        label_remarque_classe = QLabel(tr('remarque'))
        self.classe_layout.addWidget(label_remarque_classe)
        self.remarque_classe = QTextEdit()
        self.remarque_classe.textChanged.connect(self.mettre_a_jour_classe)
        self.classe_layout.addWidget(self.remarque_classe)

        label_moyenne_classe = QLabel(tr('moyenne'))
        self.classe_layout.addWidget(label_moyenne_classe)
        self.moyenne_classe = QDoubleSpinBox()
        self.moyenne_classe.cleanText()
        self.moyenne_classe.valueChanged.connect(self.mettre_a_jour_classe)
        self.classe_layout.addWidget(self.moyenne_classe)

        self.conseils_tab.addTab(self.classe_tab, 'Classe')

        # Onglet "Élèves"
        self.eleves_tab = QWidget()
        self.eleves_layout = QVBoxLayout()
        self.eleves_tab.setLayout(self.eleves_layout)

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText(tr('rechercher'))
        self.recherche.setClearButtonEnabled(True)
        self.recherche.textChanged.connect(self.rechercher_eleve)
        self.eleves_layout.addWidget(self.recherche)

        self.combo_eleves = QComboBox()
        self.eleves_layout.addWidget(self.combo_eleves)

        self.periodes_tab = QTabBar()

        for i in range(self.delegue_master.getClasse().get_nb_periodes()):
            self.periodes_tab.addTab('Période ' + str(i + 1))
        self.eleves_layout.addWidget(self.periodes_tab)

        label_remarque = QLabel(tr('remarque'))
        self.eleves_layout.addWidget(label_remarque)
        self.remarque = QTextEdit()
        self.remarque.textChanged.connect(self.mettre_a_jour_remarque)
        self.eleves_layout.addWidget(self.remarque)

        label_moyenne = QLabel(tr('moyenne'))
        self.eleves_layout.addWidget(label_moyenne)
        self.moyenne = QDoubleSpinBox()
        self.moyenne.cleanText()
        self.moyenne.valueChanged.connect(self.mettre_a_jour_moyenne)
        self.eleves_layout.addWidget(self.moyenne)

        label_appreciations = QLabel(tr('appreciation'))
        self.eleves_layout.addWidget(label_appreciations)
        appreciations = tr('appreciations')
        for appreciation in self.delegue_master.profile.appreciations:
            appreciations.append(appreciation)

        self.appreciation = QComboBox()
        self.appreciation.addItems(appreciations)
        self.appreciation.currentIndexChanged.connect(self.mettre_a_jour_appreciation)
        self.eleves_layout.addWidget(self.appreciation)
        
        # Ajouter les boutons "Précédent" et "Suivant"
        self.nav_layout = QHBoxLayout()
        self.btn_precedent = QPushButton()
        self.btn_precedent.clicked.connect(self.eleve_precedent)
        self.nav_layout.addWidget(self.btn_precedent)

        self.btn_suivant = QPushButton()
        self.btn_suivant.clicked.connect(self.eleve_suivant)
        self.nav_layout.addWidget(self.btn_suivant)

        self.eleves_layout.addLayout(self.nav_layout)

        self.conseils_tab.addTab(self.eleves_tab, 'Élèves')
        
        self.combo_eleves.currentIndexChanged.connect(self.mettre_a_jour)
        self.periodes_tab.currentChanged.connect(self.mettre_a_jour)

        # Mettre à jour l'état des boutons au démarrage
        self.mettre_a_jour_boutons()

    def mettre_a_jour(self):
        index_periode = self.periodes_tab.currentIndex()
        index_eleve = self.combo_eleves.currentIndex()

        if index_periode == -1 or index_eleve == -1:
            self.tout_desactiver()
            return

        self.tout_activer()
        
        classe = self.delegue_master.getClasse()
        eleve = classe.get_eleves()[index_eleve]
        periode = eleve.get_periode(index_periode)

        self.remarque.setText(periode.get_remarque())
        self.moyenne.setValue(periode.get_moyenne())
        self.appreciation.setCurrentIndex(periode.get_appreciation())

        self.mettre_a_jour_boutons()

    def mettre_a_jour_remarque(self):
        index_periode = self.periodes_tab.currentIndex()
        index_eleve = self.combo_eleves.currentIndex()

        if index_periode == -1 or index_eleve == -1:
            return

        classe = self.delegue_master.getClasse()
        eleve = classe.get_eleves()[index_eleve]
        periode = eleve.get_periode(index_periode)

        periode.set_remarque(self.remarque.toPlainText())

    def mettre_a_jour_moyenne(self):
        index_periode = self.periodes_tab.currentIndex()
        index_eleve = self.combo_eleves.currentIndex()

        if index_periode == -1 or index_eleve == -1:
            return

        classe = self.delegue_master.getClasse()
        eleve = classe.get_eleves()[index_eleve]
        periode = eleve.get_periode(index_periode)

        periode.set_moyenne(self.moyenne.value())

    def mettre_a_jour_appreciation(self):
        index_periode = self.periodes_tab.currentIndex()
        index_eleve = self.combo_eleves.currentIndex()

        if index_periode == -1 or index_eleve == -1:
            return

        classe = self.delegue_master.getClasse()
        eleve = classe.get_eleves()[index_eleve]
        periode = eleve.get_periode(index_periode)

        periode.set_appreciation(self.appreciation.currentIndex())

    def mettre_a_jour_classe(self):
        classe = self.delegue_master.getClasse()
        classe.set_remarque(self.remarque_classe.toPlainText())
        classe.set_moyenne(self.moyenne_classe.value())

    def vider(self):
        self.combo_eleves.clear()
        self.remarque.setText('')
        self.moyenne.setValue(0)
        self.appreciation.setCurrentIndex(0)

        self.remarque_classe.setText('')
        self.moyenne_classe.setValue(0)

        tab_bar = self.periodes_tab
        while tab_bar.count() > 0:
            tab_bar.removeTab(0)

        self.mettre_a_jour_boutons()

    def eleve_precedent(self):
        index = self.combo_eleves.currentIndex()
        if index > 0:
            self.combo_eleves.setCurrentIndex(index - 1)
            
    def eleve_suivant(self):
        index = self.combo_eleves.currentIndex()
        if index < self.combo_eleves.count() - 1:
            self.combo_eleves.setCurrentIndex(index + 1)

    def rechercher_eleve(self):
        text = self.recherche.text().lower()
        for i in range(self.combo_eleves.count()):
            if text in self.combo_eleves.itemText(i).lower():
                self.combo_eleves.setCurrentIndex(i)
                break

    def mettre_a_jour_boutons(self):
        total_eleves = self.combo_eleves.count()
        index = self.combo_eleves.currentIndex()

        if total_eleves == 0:
            self.btn_precedent.setText('')
            self.btn_suivant.setText('')
        else:
            if index > 0:
                prev_eleve = self.combo_eleves.itemText(index - 1)
                self.btn_precedent.setText(f'< {prev_eleve} ({index}/{total_eleves})')
            else:
                self.btn_precedent.setText('Démarrer le timer')
                self.btn_precedent.clicked.disconnect()  # Dissocier le signal précédent
                self.btn_precedent.clicked.connect(self.start_timer)

            if index < total_eleves - 1:
                next_eleve = self.combo_eleves.itemText(index + 1)
                self.btn_suivant.setText(f'{next_eleve} ({index + 2}/{total_eleves}) >')
            else:
                self.btn_suivant.setText('Exporter le conseil et stopper le timer')
                self.btn_suivant.clicked.disconnect()  # Dissocier le signal précédent
                self.btn_suivant.clicked.connect(self.exporter_conseil)

    
    def start_timer(self):
        self.btn_precedent.clicked.disconnect()
        self.btn_precedent.clicked.connect(self.eleve_precedent)
        self.timer.start(1000)  # Le minuteur se déclenchera toutes les 1000 ms (1 seconde)

    def stop_timer(self):
        self.timer.stop()
        
    def update_timer(self):
        self.seconds_elapsed += 1
        minutes = self.seconds_elapsed // 60
        seconds = self.seconds_elapsed % 60
        self.timer_label.setText(f"Temps écoulé : {minutes:02d}:{seconds:02d}")
        
    def exporter_conseil(self):
        self.btn_suivant.clicked.disconnect()
        self.btn_suivant.clicked.connect(self.eleve_suivant)
        self.stop_timer()
        self.delegue_master.menuBar.exporter_action()
        
    def tout_desactiver(self):
        self.recherche.setEnabled(False)
        self.combo_eleves.setEnabled(False)
        self.periodes_tab.setEnabled(False)
        self.remarque.setEnabled(False)
        self.moyenne.setEnabled(False)
        self.appreciation.setEnabled(False)
        self.btn_precedent.setEnabled(False)
        self.btn_suivant.setEnabled(False)
    
    def tout_activer(self):
        self.recherche.setEnabled(True)
        self.combo_eleves.setEnabled(True)
        self.periodes_tab.setEnabled(True)
        self.remarque.setEnabled(True)
        self.moyenne.setEnabled(True)
        self.appreciation.setEnabled(True)
        self.btn_precedent.setEnabled(True)
        self.btn_suivant.setEnabled(True)