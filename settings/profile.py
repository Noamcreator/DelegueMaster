import json
import os


class Profile:
    def __init__(self):
        # Paramètres par défaut du profil
        self.premier_demarage = False
        self.langue = 'fr_fr'  # Langue par défaut
        self.note_max = 20.0  # Note maximale par défaut
        self.theme = 1  # Thème par défaut
        self.dark = False  # Mode sombre par défaut
        self.emplacement_ouvrir = ""  # Emplacement par défaut pour ouvrir les fichiers
        self.emplacement_enregistrer_sous = ""  # Emplacement par défaut pour enregistrer les fichiers
        self.emplacement_fichier_db = ""  # Emplacement par défaut pour enregistrer la base de données
        self.appreciations = []

        # profile.json dans le dossier "Délégué Master" qui est créé dans le dossier "Documents" de l'utilisateur
        documents_dir = os.path.join(os.path.expanduser('~'), 'Documents')
        self.profile_path = os.path.join(documents_dir, 'Délégué Master')

        # Créer le dossier "Délégué Master" s'il n'existe pas
        if not os.path.exists(self.profile_path):
            os.makedirs(self.profile_path)
            self.premier_demarage = True

        # Chemin complet du fichier profile.json
        self.profile_path = os.path.join(self.profile_path, 'profile.json')

        # Si le fichier profile.json n'existe pas, le crée en utilisant les paramètres par défaut
        if not os.path.exists(self.profile_path):
            self.enregistrer_fichier()
        else:
            # Si le fichier profile.json existe, charge ses données pour initialiser les paramètres du profil
            with open(self.profile_path, 'r') as f:
                profile = json.load(f)
                self.langue = profile['langue']
                self.note_max = float(profile['note_max'])
                self.theme = int(profile['theme'])
                self.dark = bool(profile['dark'])
                self.emplacement_ouvrir = profile['emplacement_ouvrir']
                self.emplacement_enregistrer_sous = profile['emplacement_enregistrer_sous']
                self.emplacement_fichier_db = profile['emplacement_fichier_db']
                self.appreciations = profile['appreciations']

    # Méthode pour enregistrer les paramètres du profil dans le fichier profile.json
    def enregistrer_fichier(self):
        with open(self.profile_path, 'w') as f:
            profile = {
                "langue": self.langue,
                "note_max": self.note_max,
                "theme": self.theme,
                "dark": self.dark,
                "emplacement_ouvrir": self.emplacement_ouvrir,
                "emplacement_enregistrer_sous": self.emplacement_enregistrer_sous,
                "emplacement_fichier_db": self.emplacement_fichier_db,
                "appreciations": self.appreciations
            }
            # Écriture des données du profil dans le fichier JSON avec une indentation pour une meilleure lisibilité
            json.dump(profile, f, indent=4)
