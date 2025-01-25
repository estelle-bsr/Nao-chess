class Square:
    content = Content.Vide


    def is_filled(self) : #Renvoie si la case est pleine. Pas 100% utile mais aide a la lisibilité
        return (content != Content.Vide)

    def __init__(self, Cont = Content.Vide) : #si un contenu n'es pas spécifié, c'est vide
        self.content = Cont