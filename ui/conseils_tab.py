from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QTextEdit, QLineEdit, QTabWidget, QLabel, QTabBar, QDoubleSpinBox

class ConseilsTab(QWidget):
    def __init__(self, delegue_master):
        super().__init__()
        
        self.delegue_master = delegue_master
        tr = self.delegue_master.langues.tr
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText(tr('rechercher'))
        self.recherche.setClearButtonEnabled(True)
        self.layout.addWidget(self.recherche)
        
        self.combo_eleves = QComboBox()
        self.combo_eleves.currentIndexChanged.connect(self.mettre_a_jour)
        self.layout.addWidget(self.combo_eleves)
        
        self.periodes_tab = QTabBar()
        self.periodes_tab.currentChanged.connect(self.mettre_a_jour)
        
        for i in range(self.delegue_master.getClasse().get_nb_periodes()):
            # Ajout du premier onglet au widget d'onglets
            self.periodes_tab.addTab('Période ' + str(i + 1))
        self.layout.addWidget(self.periodes_tab)
        
        label_remarque = QLabel(tr('remarque'))
        self.layout.addWidget(label_remarque)
        self.remarque = QTextEdit()
        self.remarque.textChanged.connect(self.mettre_a_jour_remarque)
        self.layout.addWidget(self.remarque)
        
        label_moyenne = QLabel(tr('moyenne'))
        self.layout.addWidget(label_moyenne)
        self.moyenne = QDoubleSpinBox()
        self.moyenne.cleanText()
        self.moyenne.valueChanged.connect(self.mettre_a_jour_moyenne)
        self.layout.addWidget(self.moyenne)
        
        label_appreciations = QLabel(tr('appreciation'))
        self.layout.addWidget(label_appreciations)
        appreciations = tr('appreciations')
        for appreciation in self.delegue_master.profile.appreciations:
            appreciations.append(appreciation)
        
        self.appreciation = QComboBox()
        self.appreciation.addItems(appreciations)
        self.appreciation.currentIndexChanged.connect(self.mettre_a_jour_appreciation)
        self.layout.addWidget(self.appreciation)

    def mettre_a_jour(self):
        index_periode = self.periodes_tab.currentIndex()
        index_eleve = self.combo_eleves.currentIndex()
        
        if index_periode == -1 or index_eleve == -1:
            return
        
        classe = self.delegue_master.getClasse()
        eleve = classe.get_eleves()[index_eleve]
        periode = eleve.get_periode(index_periode)
        
        self.remarque.setText(periode.get_remarque())
        self.moyenne.setValue(periode.get_moyenne())
        self.appreciation.setCurrentIndex(periode.get_appreciation())
        
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
        
    def vider(self):
        self.combo_eleves.clear()
        self.remarque.setText('')
        self.moyenne.setValue(0)
        self.appreciation.setCurrentIndex(0)
        
        tab_bar = self.periodes_tab
        while tab_bar.count() > 0:
            tab_bar.removeTab(0)