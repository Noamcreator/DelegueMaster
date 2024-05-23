import sqlite3

from core.classe import Classe
from core.eleve import Eleve

def creer_db(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classe (
            nom TEXT,
            nombre_de_periodes INTEGER,
            remarque TEXT,
            moyenne REAL,
            appreciation INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eleves (
            idEleve INTEGER PRIMARY KEY,
            nom TEXT,
            prenom TEXT,
            date_de_naissance TEXT,
            sexe TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conseils (
            idEleve INTEGER,
            periode TEXT,
            remarque TEXT,
            moyenne REAL,
            appreciation INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def sauvegarder_db(path, classe):
    creer_db(path)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO classe (nom, nombre_de_periodes, remarque, moyenne, appreciation)
            VALUES (?, ?, ?, ?, ?)
            ''', (classe.get_nom(), classe.get_nb_periodes(), classe.get_remarque(), classe.get_moyenne(), classe.get_appreciation()))
    
    for index_eleve in range(len(classe.get_eleves())):
        eleve = classe.get_eleve(index_eleve)
        cursor.execute('''
            INSERT INTO eleves (idEleve, nom, prenom, date_de_naissance, sexe)
            VALUES (?, ?, ?, ?, ?)
            ''', (index_eleve, eleve.nom, eleve.prenom, eleve.date_naissance, eleve.sexe))
        for index_periode in range(len(eleve.get_periodes())):
            periode = eleve.get_periode(index_periode)
            cursor.execute('''
                INSERT INTO conseils (idEleve, periode, remarque, moyenne, appreciation)
                VALUES (?, ?, ?, ?, ?)
                ''', (index_eleve, index_periode, periode.get_remarque(), periode.get_moyenne(), periode.get_appreciation()))
    conn.commit()
    conn.close()

def ouvrir_db(path):
    classe = Classe()
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    # Charger les informations de la classe
    cursor.execute('SELECT * FROM classe')
    classe_info = cursor.fetchone()
    if classe_info:
        classe.set_nom(classe_info[0])
        classe.set_nb_periodes(classe_info[1])
        classe.set_remarque(classe_info[2])
        classe.set_moyenne(classe_info[3])
        classe.set_appreciation(classe_info[4])
    
    # Charger les informations des élèves
    cursor.execute('SELECT * FROM eleves')
    eleves = cursor.fetchall()
    for e in eleves:
        eleve = Eleve(e[1], e[2])
        eleve.set_date_naissance(e[3])
        eleve.set_sexe(e[4])
        
        # Récupérer le nombre de périodes 
        eleve.set_nb_periodes(classe.get_nb_periodes())
        
        # Charger les conseils pour l'élève
        cursor.execute('SELECT * FROM conseils WHERE idEleve = ?', (e[0],))
        conseils = cursor.fetchall()
        for p in conseils:
            periode = eleve.get_periode(int(p[1]))
            periode.set_remarque(p[2])
            periode.set_moyenne(p[3])
            periode.set_appreciation(p[4])
        
        classe.ajouter_eleve(eleve)

    conn.close()
    
    return classe