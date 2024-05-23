import os

def assets_path():
    # Obtenir le chemin absolu du dossier où se trouve ce script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Remonter de deux niveaux pour obtenir le répertoire du projet
    project_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    # Construire le chemin du dossier assets
    assets_path = os.path.join(project_dir, 'assets')
    return assets_path

def get_assets_path(file):
    # Construire le chemin du dossier assets + file
    assets_path_file = os.path.join(assets_path(), file)
    return assets_path_file
