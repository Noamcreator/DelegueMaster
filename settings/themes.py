import qt_material


class Themes:
    def __init__(self, delegue_master):
        # Initialisation de la classe Themes avec une référence à l'instance de DelegueMaster
        self.delegue_master = delegue_master
        
            # Application du thème à l'application
        qt_material.apply_stylesheet(delegue_master.window(), theme=self.convertir_theme_int_en_str())

    # Méthode pour obtenir les noms des couleurs claires disponibles dans les thèmes
    def light_color(self):
        color_names = []
        for theme in qt_material.list_themes():
            if 'light_' in theme:
                # Séparation du nom de fichier XML en mots
                words = theme.split('_')
                # Extraction de la deuxième partie qui représente la couleur
                color_name = words[1].capitalize()
                # Suppression de l'extension .xml
                color_name = color_name.replace('.xml', '')
                if '500' in theme:
                    color_name = 'Dark ' + color_name  # Ajout de "Dark" pour les variantes sombres
                # Ajout du nom de la couleur à la liste
                color_names.append(color_name)
        return color_names

    # Méthode pour obtenir les noms des couleurs sombres disponibles dans les thèmes
    def dark_color(self):
        color_names = []
        for theme in qt_material.list_themes():
            if 'dark_' in theme:
                # Séparation du nom de fichier XML en mots
                words = theme.split('_')
                # Extraction de la deuxième partie qui représente la couleur
                color_name = words[1].capitalize()
                # Suppression de l'extension .xml
                color_name = color_name.replace('.xml', '')
                # Ajout du nom de la couleur à la liste
                color_names.append(color_name)
        return color_names

    # Méthode pour convertir le thème en chaîne de caractères pour l'interface utilisateur
    def convertir_theme_int_en_str(self):
        # Configuration de la feuille de style
        if self.delegue_master.profile.dark:
            return qt_material.list_themes()[self.delegue_master.profile.theme]  # Renvoie le thème sombre sélectionné
        else:
            # Si le mode sombre n'est pas activé, ajuste l'indice du thème en fonction des couleurs sombres disponibles
            return qt_material.list_themes()[self.delegue_master.profile.theme + len(self.dark_color())]
