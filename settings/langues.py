import json
import os

from utils.files_utils import get_assets_path
class Langues:
    def __init__(self, delegue_master):
        self.delegue_master = delegue_master

        self.langues = []

        # Chemin vers le dossier contenant les fichiers JSON de langues
        self.dossier_langues = get_assets_path('languages')

        # Parcours du dossier des langues pour récupérer les noms des fichiers JSON
        for filename in os.listdir(self.dossier_langues):
            if filename.endswith('.json'):
                self.langues.append(filename[:-5])

        # Langue actuellement sélectionnée
        self.langue_actuelle = delegue_master.profile.langue
        self.langue_json = None
        self.charger_langues(self.langue_actuelle)

        # Noms des langues pour l'affichage dans l'interface utilisateur
        self.langues_noms = self.recup_noms_langues()

    # Charger les données de la langue spécifiée depuis le fichier JSON correspondant
    def charger_langues(self, langue):
        file = os.path.join(self.dossier_langues, f'{langue}.json')
        with open(file, 'r', encoding='utf-8') as f:
            self.langue_json = json.load(f)

    # Changer la langue de l'application en fonction de l'index sélectionné
    def changer_langue(self, index):
        self.langue_actuelle = self.langues[index]
        self.charger_langues(self.langue_actuelle)

        # Mettre à jour la langue dans les différents composants de l'application
        self.delegue_master.changer_langue()
        self.delegue_master.menuBar.changer_langue()
        self.delegue_master.recup_onglet_eleves().changer_langue()
        self.delegue_master.recup_onglet_conseils().changer_langue()
        return self.langue_actuelle

    # Fonction de traduction pour récupérer la traduction d'une clé donnée
    def tr(self, cle):
        if cle in self.langue_json:
            return self.langue_json[cle]
        else:
            print(cle, "n'existe pas dans la langue :", self.langues_noms[self.langues.index(self.langue_actuelle)])
            return cle

    # Récupérer la langue actuelle
    def recup_langue(self):
        return self.langue_actuelle

    # Récupérer la liste des fichiers de langue disponibles
    def recup_fichier_langues(self):
        return self.langues

    # Récupérer les noms des langues pour l'affichage dans l'interface utilisateur
    def recup_noms_langues(self):
        langues_noms = []
        for langue in self.langues:
            file = os.path.join(self.dossier_langues, f'{langue}.json')
            with open(file, 'r', encoding='utf-8') as f:
                langues_noms.append(json.load(f)['nom_langue'])

        return langues_noms
