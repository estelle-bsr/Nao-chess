class Coup:
    depart = ""
    arriver = ""
    tour = True
    def __init__(self):
        self.depart = "depart"
        self.arriver = "arriver"
        self.tour = True
        print("a")
    def __repr__(self):
        return self.depart + " " + self.arriver + ","
        
class Partie:
    Coups = []
    Tour = True
    def __init__(self):
        self.Tour = True
        self.Coups = [Coup(),Coup()]
        print(len(self.Coups))
    def __repr__(self):
        tostring = ""
        for coup in self.Coups:
            tostring += str(coup)
        return tostring