class FenBoard:

    #Cette classe stock en plusieurs partie les informations contenues dans un code fen pour permettre une manipulation plus simple.
    #Sources:https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation

    #lines = [['v' for i in range 8 ] for j in range 8]
    lines = [['v'] * 8] * 8
    #des char, avec r = rook ; n = knight ; b = bishop ; q = queen ; k = king ; p = pawn ; v = vide, ce qui n'est pas comme dans la fen standard mais raf
    #exemple de string : rvvvNvvvv
    #Les majuscules sont les blancs, les minuscules les noirs

    halfturn = 0
    #le nombre de demi-tours, commencant a 0 pour "personne n'a encore joué", 1 pour "blanc a joué une fois", etc

    last_halfturn_with_capture_or_pawn_advance = 0
    #Nom assez clair, utilisé pour empécher les matchs trop longs (pas super important mais nécessaire pour générer le fen)

    castling_King_W = castling_King_B = castling_Queen_W = castling_Queen_B = True 
    #La possibilité d'un roque. Par défault c'est possible, ça devient impossible au fur et a mesure du jeu

    en_passant_doable = [-1, -1]
    #l'emplacement d'un en passant, si faisable. Change car c'est uniquement possible sur le dernier pion a avoir bougé, et seulement juste après
    
    def __init__(blank=false):
        if(blank) :
            
        else : 
            lines[0][0] = 'R'
            lines[0][1] = 'N'
            lines[0][2] = 'B'
            lines[0][3] = 'Q'
            lines[0][4] = 'K'
            lines[0][5] = 'B'
            lines[0][6] = 'N'
            lines[0][7] = 'R'

            lines[7][0] = 'r'
            lines[7][1] = 'n'
            lines[7][2] = 'b'
            lines[7][3] = 'q'
            lines[7][4] = 'k'
            lines[7][5] = 'b'
            lines[7][6] = 'n'
            lines[7][7] = 'r'

            for i in range (8) :
                lines[1][i] = 'P'
                lines[6][i] = 'p'
            

    def current_player(self):
            if(halfturn%2==0):
                return "w"
            else :
                return "b"

    def indexToSquare() :
        #TODO
    def squareToIndex() :
        #TODO


    def getNotation() : 
        #TODO


    def to_fen_string(self) : 
        fen_string = ''
        w = 'w'
        count_empty = 0
        for (j in range len(this.lines)) :      #pour chaque ligne, pour chaque case
            for (i in range len(this.lines)) :  #seulement possible car c'est un carré
                if (this.lines[j, i] == v) :     #si c'est vide, rien ajouter au fern (pour l'instant) et incrementer le compte
                    count_empty+=1
                
                else : 
                    if (count_empty!=0) :
                        fen_string = fen_string + count_empty   #avant d'ajouter un caractere, ajoute les cases vides
                        count_empty = 0
                    fen_string = fen_string + this.lines[j, i]

            if(count_empty!=0) :                                    #de même avant de finir la ligne
                fen_string = fen_string + count_empty
                count_empty = 0
            fen_string = fen_string + '/'
        
        fen_string = fen_string + ' '

        if(halfturn % 2 != 0)
            w = 'b' #
        
        fen_string = fen_string + w #

        return fen_string