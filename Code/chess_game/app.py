import sys
from globalVar import *
sys.path.append(PATH_TO_PROJECT+"movement\\")
sys.path.append(PATH_TO_PROJECT+"picture\\")
sys.path.append(PATH_TO_PROJECT)
sys.path.append("C:\\pynaoqi\\lib\\")

#import movement as mov
import Tkinter as tk
import time
from naoqi import ALProxy
from Stockfish import Stockfish 
from OperationPicture import *
import main as m
import math as math
import random


# Configuration de connexion au robot

memory_proxy = ALProxy("ALMemory", robot_ip, robot_port)

# Capteurs tactiles
capteur_tactile_avant = "Device/SubDeviceList/Head/Touch/Front/Sensor/Value"
capteur_tactile_arriere = "Device/SubDeviceList/Head/Touch/Rear/Sensor/Value"

# Temps initial et variables globales
temps_initial_total = 10 * 60  # 10 minutes en secondes
en_cours_gauche = False
en_cours_droite = False
temps_gauche_restants = temps_initial_total
temps_droite_restants = temps_initial_total
temps_gauche_initial = 0
temps_droite_initial = 0
premier_coup = True
jeu_termine = False

# Variables globales pour les widgets
root = None
label_avant = None
label_arriere = None
bouton_gauche = None
bouton_droite = None
var_gauche = None
var_droite = None
check_gauche = None
check_droite = None

buffer_img = None
first_move = True
stockfish = None

# Fonction pour mettre a jour l'etat des capteurs
def mettre_a_jour_etat_capteur():
    global label_avant, label_arriere
    capteur_avant = memory_proxy.getData(capteur_tactile_avant)
    capteur_arriere = memory_proxy.getData(capteur_tactile_arriere)

    if capteur_avant == 1:
        label_avant.config(text="Capteur avant : Presse")
    else:
        label_avant.config(text="Capteur avant : Non presse")

    if capteur_arriere == 1:
        label_arriere.config(text="Capteur arriere : Presse")
    else:
        label_arriere.config(text="Capteur arriere : Non presse")

    root.after(500, mettre_a_jour_etat_capteur)

# Desactiver les checkbuttons apres le debut du jeu
def desactiver_checkbutton_30_seconde():
    check_gauche.config(state="disabled")
    check_droite.config(state="disabled")

# Gestion des clics sur les boutons
def cliquer_bouton_gauche():
    desactiver_checkbutton_30_seconde()
    global en_cours_gauche, en_cours_droite, temps_gauche_initial, temps_gauche_restants, temps_droite_restants, premier_coup,buffer_img
    buffer_img = CaptureVue(robot_ip,robot_port)
    if not en_cours_gauche and not jeu_termine:
        if en_cours_droite:
            temps_droite_restants -= time.time() - temps_droite_initial
        en_cours_gauche = True
        en_cours_droite = False
        temps_gauche_initial = time.time()

        if var_gauche.get():
            if not premier_coup:
                temps_gauche_restants += 30
            premier_coup = False

        bouton_gauche.config(bg="#4CAF50", state="disabled", relief="sunken")
        bouton_droite.config(bg="#B0B0B0", state="normal", relief="raised")
        mettre_a_jour_temporisateurs()

def cliquer_bouton_droite():
    desactiver_checkbutton_30_seconde()
    global buffer_img, stockfish , first_move
    regardRobot(robot_ip, robot_port)
    actuel_img = CaptureVue(robot_ip,robot_port)
    random_number = random.randint(1, 10)
    if random_number < 5:
        m.disrupt()
    if not first_move :  
        cv.imshow("buffer",buffer_img)
        cv.imshow("a",actuel_img)
        cv.waitKey(0)  
        cv.destroyAllWindows()
        print "human played "+ stockfish.color.upper()
        try:
            square_moved = get_two_squaresBis(buffer_img,actuel_img,stockfish.color.upper())
            print square_moved
            
        except:
            buffer_img = actuel_img
            return
        stockfish.human_play(square_moved)
        
    else : 
        first_move = False
    
    best_move = stockfish.robot_play_best_move()
    print best_move
    piece = stockfish.board.piece_at(best_move.to_square)

    m.sayCase(str(best_move)[:2] + '/' + str(best_move)[2:]+"/"+m.nomPion(piece.symbol()))#
    buffer_img = actuel_img
    global en_cours_droite, en_cours_gauche, temps_droite_initial, temps_droite_restants, temps_gauche_restants, premier_coup
    if not en_cours_droite and not jeu_termine:
        if en_cours_gauche:
            temps_gauche_restants -= time.time() - temps_gauche_initial
        en_cours_droite = True
        en_cours_gauche = False
        temps_droite_initial = time.time()

        if var_droite.get():
            if not premier_coup:
                temps_droite_restants += 30
            premier_coup = False

        bouton_droite.config(bg="#4CAF50", state="disabled", relief="sunken")
        bouton_gauche.config(bg="#B0B0B0", state="normal", relief="raised")
        mettre_a_jour_temporisateurs()

# Formater le temps en mm:ss
def formater_temps(temps):
    minutes = int(temps // 60)
    secondes = int(temps % 60)
    return "{:02}:{:02}".format(minutes, secondes)

# Fin de la partie
def terminer_jeu(joueur_perdant):
    global jeu_termine
    jeu_termine = True
    bouton_gauche.config(state="disabled")
    bouton_droite.config(state="disabled")
    if joueur_perdant == "gauche":
        bouton_gauche.config(bg="red", text="Joueur 1 a perdu !")
    elif joueur_perdant == "droite":
        bouton_droite.config(bg="red", text="Joueur 2 a perdu !")

# Mise a jour des temporisateurs
def mettre_a_jour_temporisateurs():
    global en_cours_gauche, en_cours_droite, temps_gauche_initial, temps_droite_initial
    global temps_gauche_restants, temps_droite_restants, jeu_termine

    if not jeu_termine:
        if en_cours_gauche:
            temps_ecoule_gauche = temps_gauche_restants - (time.time() - temps_gauche_initial)
            if temps_ecoule_gauche <= 0:
                temps_ecoule_gauche = 0
                terminer_jeu("gauche")
            bouton_gauche.config(text="Timer j1: " + formater_temps(temps_ecoule_gauche))

        if en_cours_droite:
            temps_ecoule_droite = temps_droite_restants - (time.time() - temps_droite_initial)
            if temps_ecoule_droite <= 0:
                temps_ecoule_droite = 0
                terminer_jeu("droite")
            bouton_droite.config(text="Timer j2: " + formater_temps(temps_ecoule_droite))
    root.after(100, mettre_a_jour_temporisateurs)

# Reinitialiser les variables globales des timers
def reinitialiser_variables():
    global en_cours_gauche, en_cours_droite, temps_gauche_restants, temps_droite_restants, temps_gauche_initial, temps_droite_initial, premier_coup, jeu_termine, buffer_img, first_move, stockfish

    # Reinitialiser les variables globales des temps
    temps_gauche_restants = temps_initial_total
    temps_droite_restants = temps_initial_total
    temps_gauche_initial = 0
    temps_droite_initial = 0
    premier_coup = True
    jeu_termine = False
    en_cours_gauche = False
    en_cours_droite = False
    first_move = True
    buffer_img = None
    stockfish = None

    # Reinitialiser les widgets
    bouton_gauche.config(bg="#B0B0B0", state="normal", relief="raised", text="Timer HUMAIN : 10:00")
    bouton_droite.config(bg="#B0B0B0", state="normal", relief="raised", text="Timer ROBOT : 10:00")
    label_avant.config(text="Capteur avant : Non presse")
    label_arriere.config(text="Capteur arriere : Non presse")
    check_gauche.config(state="normal")
    check_droite.config(state="normal")

    # Reinitialiser les timers visuels
    mettre_a_jour_temporisateurs()

    # Reinitialiser les capteurs tactiles
    mettre_a_jour_etat_capteur()

    # Reinitialiser les boutons de jeu et etat
    bouton_gauche.config(state="normal")
    bouton_droite.config(state="normal")

# Fonction pour demarrer une nouvelle partie
def start_game():
    reinitialiser_variables()  # Reinitialisation avant de commencer

    global buffer_img, stockfish ,first_move
    stockfish = Stockfish()
    regardRobot(robot_ip, robot_port)
    side = isRobotWhite(robot_ip, robot_port)
    first_move = side
    print(side)
    stockfish.setSide(side)
    buffer_img = CaptureVue(robot_ip, robot_port)
    #difficulte = m.start(side)
    difficulte = 4
    stockfish.depth(difficulte)
    print("difficulte")
    
    if side:
        cliquer_bouton_droite()
    else:
        cliquer_bouton_gauche()
    

# Fonction principale de l'application
def app():
    global root, label_avant, label_arriere, bouton_gauche, bouton_droite
    global var_gauche, var_droite, check_gauche, check_droite

    root = tk.Tk()
    root.state('zoomed')
    root.title("Detection des capteurs tactiles de la tete de NAO")
    root.config(bg="#2E2E2E")

    # Configuration de la colonne principale
    root.grid_columnconfigure(0, weight=1)

    # Frame pour les capteurs tactiles
    frame_capteurs = tk.Frame(root, bg="#2E2E2E", padx=20, pady=10)
    frame_capteurs.grid(row=0, column=0, sticky="n")
    frame_capteurs.grid_columnconfigure(0, weight=1)

    label_avant = tk.Label(frame_capteurs, text="Capteur avant : Non presse", bg="#34495E", fg="white", font=("Helvetica", 14), pady=10, relief="ridge", width=40)
    label_avant.grid(row=0, column=0, pady=5, sticky="ew")

    label_arriere = tk.Label(frame_capteurs, text="Capteur arriere : Non presse", bg="#34495E", fg="white", font=("Helvetica", 14), pady=10, relief="ridge", width=40)
    label_arriere.grid(row=1, column=0, pady=5, sticky="ew")

    # Frame pour les minuteurs
    frame_minuteurs = tk.Frame(root, bg="#2E2E2E")
    frame_minuteurs.grid(row=1, column=0, pady=20, sticky="ew")
    frame_minuteurs.grid_columnconfigure(0, weight=1)
    frame_minuteurs.grid_columnconfigure(1, weight=1)

    bouton_gauche = tk.Button(frame_minuteurs, text="Timer HUMAIN : 10:00", command=cliquer_bouton_gauche, bg="#B0B0B0", fg="black", font=("Helvetica", 14), relief="raised", height=3)
    bouton_gauche.grid(row=0, column=0, padx=20, sticky="nsew")

    bouton_droite = tk.Button(frame_minuteurs, text="Timer ROBOT : 10:00", command=cliquer_bouton_droite, bg="#B0B0B0", fg="black", font=("Helvetica", 14), relief="raised", height=3)
    bouton_droite.grid(row=0, column=1, padx=20, sticky="nsew")

    # Frame pour les checkbuttons
    frame_checkbuttons = tk.Frame(root, bg="#2E2E2E")
    frame_checkbuttons.grid(row=2, column=0, pady=10, sticky="ew")
    frame_checkbuttons.grid_columnconfigure(0, weight=1)
    frame_checkbuttons.grid_columnconfigure(1, weight=1)

    var_gauche = tk.BooleanVar()
    var_droite = tk.BooleanVar()
    check_gauche = tk.Checkbutton(frame_checkbuttons, text="Ajout de 30 secondes a chaque coup pour le joueur 1", variable=var_gauche, fg="black", bg="#0E87C9", font=("Helvetica", 14))
    check_gauche.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    check_droite = tk.Checkbutton(frame_checkbuttons, text="Ajout de 30 secondes a chaque coup pour le joueur 2", variable=var_droite, fg="black", bg="#0E87C9", font=("Helvetica", 14))
    check_droite.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

    # Bouton "Repeter" centre
    frame_repeater = tk.Frame(root, bg="#2E2E2E")
    frame_repeater.grid(row=3, column=0, pady=20, sticky="ew")
    frame_repeater.grid_columnconfigure(0, weight=1)

    bouton_repeater = tk.Button(frame_repeater, text="Repeter", command=m.repeter, bg="#F39C12", fg="black", font=("Helvetica", 14), relief="raised", height=3)
    bouton_repeater.grid(row=0, column=0, padx=20, sticky="nsew")

    frame_start_game = tk.Frame(root, bg="#2E2E2E")
    frame_start_game.grid(row=4, column=0, pady=20, sticky="ew")
    frame_start_game.grid_columnconfigure(0, weight=1)

    bouton_start_game = tk.Button(frame_start_game, text="Start Game", command=start_game, bg="#F39C12", fg="black", font=("Helvetica", 14), relief="raised", height=3)
    bouton_start_game.grid(row=0, column=0, padx=20, sticky="nsew")

   

    # Centrer tous les composants dans l'application
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(4, weight=1)

    # Lancement des mises a jour
    mettre_a_jour_etat_capteur()
    root.mainloop()
m.checkmate()
