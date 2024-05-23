class Periode:
    def __init__(self):
        self.remarque = ''
        self.moyenne = 0.0
        self.appreciation = 0
        
    def get_remarque(self):
        return self.remarque
    
    def set_remarque(self, remarque):
        self.remarque = remarque

    def get_appreciation(self):
        return self.appreciation
    
    def set_appreciation(self, appreciation):
        self.appreciation = appreciation

    def get_moyenne(self):
        return self.moyenne

    def set_moyenne(self, moyenne):
        self.moyenne = moyenne