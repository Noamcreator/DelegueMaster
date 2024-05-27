class Classe:
    def __init__(self):
        self.nom = ''
        self.nb_periodes = 2 # Nombre de périodes par défaut (Semestre 1 et 2)
        self.remarque = ''
        self.moyenne = 0.0
        self.eleves = []
    
    def ajouter_eleve(self, eleve):
        self.eleves.append(eleve)
        
    def supprimer_eleve(self, eleve):
        self.eleves.remove(eleve)
    
    def set_nom(self, nom):
        self.nom = nom

    def get_nom(self):
        return self.nom
    
    def get_eleves(self):
        return self.eleves
    
    def get_nb_eleves(self):
        return len(self.eleves)
    
    def get_eleve(self, index):
        return self.eleves[index]
    
    def get_nb_periodes(self):
        return self.nb_periodes
    
    def set_nb_periodes(self, nb_periodes):
        self.nb_periodes = nb_periodes
        
    def set_remarque(self, remarque):
        self.remarque = remarque
    
    def get_remarque(self):
        return self.remarque

    def set_moyenne(self, moyenne):
        self.moyenne = moyenne
    
    def get_moyenne(self):
        return self.moyenne