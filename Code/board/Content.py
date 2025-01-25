from enum import Enum

#Liste des contenus possible pour une case.
class Content(Enum):
    'Vide' = 0
    
    'Roi Noir' = 1
    'Roi Blanc' = 2

    'Reine Noire' = 3
    'Reine Blanche' = 4

    'Tour Noire' = 5
    'Tour Blanche' = 6

    'Fou Noir' = 7
    'Fou Blanc' = 8

    'Cavalier Noir' = 9
    'Cavalier Blanc' = 10

    'Pion Noir' = 11
    'Pion Blanc' = 12

#Comme cela ne sert qu'a communiquer le contenu du plateau a stockfish, 
#pas besoin d'associer de la logique a chaque piece.