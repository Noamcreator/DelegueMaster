from core.periode import Periode


class Eleve:
    def __init__(self, nom, prenom):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = None
        self.sexe = None
        self.periodes = []
    
    def set_nom(self, nom):
        self.nom = nom
    
    def get_nom(self):
        return self.nom
    
    def set_prenom(self, prenom):
        self.prenom = prenom
        
    def get_prenom(self):
        return self.prenom
        
    def get_nom_complet(self):
        return self.nom + " " + self.prenom
    
    def set_date_naissance(self, date_naissance):
        self.date_naissance = date_naissance
        
    def get_date_naissance(self):
        return self.date_naissance
    
    def set_sexe(self, sexe):
        self.sexe = sexe
        
    def get_sexe(self):
        return self.sexe
        
    def add_periode(self, periode):
        self.periodes.append(periode)
    
    def set_nb_periodes(self, nb_periodes):
        if nb_periodes == len(self.periodes):
            return
        if nb_periodes < len(self.periodes):
            del self.periodes[nb_periodes:]
        if nb_periodes > len(self.periodes):
            for i in range(nb_periodes - len(self.periodes)):
                self.periodes.append(Periode())
                
    def set_periodes(self, periodes):
        self.periodes = periodes
        
    def get_periodes(self):
        return self.periodes
    
    def get_periode(self, index):
        if index >= len(self.periodes):
            return None
        return self.periodes[index]