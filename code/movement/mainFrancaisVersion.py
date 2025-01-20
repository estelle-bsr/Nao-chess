from naoqi import ALProxy
from random import *
import time
import os
import math
import threading
from movement import *
import globalVar 

# Definir les modules necessaires.
tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
asr = ALProxy("ALSpeechRecognition", robot_ip, robot_port)
audioPlayer = ALProxy("ALAudioPlayer", robot_ip, robot_port)
audioDevice = ALProxy("ALAudioDevice", robot_ip, robot_port)
leds = ALProxy("ALLeds", robot_ip, robot_port)
motion = ALProxy("ALMotion", robot_ip, robot_port)
posture = ALProxy("ALRobotPosture", robot_ip, robot_port)
memory = ALProxy("ALMemory", robot_ip, robot_port)


def standUp():
    """
    Fonction pour que Nao se leve.
    """
    posture.goToPosture("Stand", 1.0) # Nao se lzve.

def sit():
    """
    Fonction pour que Nao s'assoit.
    """
    posture.goToPosture("Sit", 1.0) # Nao s'asseoit.

def resetLeds():
    """
    Fonction pour mettre les leds blanc.
    """
    print("Debut fonction : resetLeds.") # Indicate in the console for follow-up.
    leds.fadeRGB("FaceLeds", 1.0, 1.0, 1.0, 0) # Mettre les yeux blanc.
    leds.fadeRGB("ChestLeds", 1.0, 1.0, 1.0, 0) # Mettre le logo blanc.
    leds.fadeRGB("FeetLeds", 1.0, 1.0, 1.0, 0) # Mettre les pieds blanc.
    print("Fin fonction : resetLeds.") # Indicate in the console for follow-up.

def cheatingF ():
    """
    Fonction de la reaction de Nao quand son adversaire triche.
    """
    print("Debut fonction : cheatingF.") # Indicate in the console for follow-up.
    leds.fadeRGB("FaceLeds", 1.0, 0.0, 0.0, 0) # Mettre les yeux rouge.
    leds.fadeRGB("ChestLeds", 1.0, 0.0, 0.0, 0) # Mettre le logo rouge.
    leds.fadeRGB("FeetLeds", 1.0, 0.0, 0.0, 0) # Mettre les pieds rouge.
    globalVar.TexteARepete = "Tu as tricher !"
    tts.say("Tu as tricher !") # Nao indique la triche.
    time.sleep(2) # Attendre deux secondes.
    resetLeds() # Remttre les leds blanc.
    print("Fin fonction : cheatingF.") # Indicate in the console for follow-up.

def shakeHands():
    """
    Fonction pour serrer la main.
    """
    print("Debut fonction : shakeHands.") # Indicate in the console for follow-up.
    globalVar.TexteARepete = "Ai tu gaucher ou droitier ?"
    tts.say("Ai tu gaucher ou droitier ?") # Nao dit.
    asr.pause(True)
    asr.setVocabulary(["droitier", "gaucher", "droitiere", "gauchere"], False) # Mettre les mots a reconnaitre.
    asr.pause(True) # Activer la reconnaissance vocale.
    asr.setLanguage("French") # Mettre la langue francaise.
    asr.pause(False) # Arreter la reconnaissance vocale.
    asr.subscribe("Test_ASR")
    while True:
        time.sleep(3) # Attend trois seconde. 
        result = memory.getData("WordRecognized") # Recuperer la reponse de l adversaire. 
        asr.unsubscribe("Test_ASR")
        reponse = result[0].lower() # Recuperer la reponse.
        print("Nao a comprit comme reponse a la question gaucher ou droitier : " + reponse) # Afficher le suivis dans la console.
        if reponse == "droitier" or reponse== "droitiere": # Si la reponse est droitier ou droitiere,
            globalVar.TexteARepete = "Vouzaitte droitier. , Alors serrons nous la main."
            tts.say("Vouzaitte droitier.") # Nao dit.
            tts.say("Alors serrons nous la main.") # Nao dit.
            shakeHandsRight() # Appelle de fonction pour serrer la main droite.
            break # Sortir de la fonction.
        elif reponse == "gaucher" or reponse== "gauchere": # Si la reponse est gaucher ou gauchere,
            globalVar.TexteARepete = "Vouzaitte gaucher , Alors serrons nous la main"
            tts.say("Vouzaitte gaucher") # Nao dit.
            tts.say("Alors serrons nous la main") # Nao dit.
            shakeHandsLeft() # Appelle de fonction pour serrer la main gauche.
            break # Sortir de la fonction.
        globalVar.TexteARepete = "Je n'ai pas compris pouvez vous repeter"
        tts.say("Je n'ai pas compris pouvez vous repeter") # Nao dit.
        asr.subscribe("Test_ASR")
    print("Fin fonction : shakeHands.") # Indicate in the console for follow-up.

def shakeHandsRight():
    """
    Fonction pour serrer de la main gauche lorsque l'adversaire a dit droite.
    """
    joints_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"  
    ] # Definir les articulation du bras gauche.
    target_angles = [
        math.radians(0), # LShoulderPitch
        math.radians(18.2), # LShoulderRoll 
        math.radians(-13.3), # LElbowYaw 
        math.radians(0), # LElbowRoll
        math.radians(-104.5), # LWristYaw
        0.02, # LHand 

    ] # Definir les angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Faire le mouvement.
    thread_ouvrir_main = threading.Thread(target=hand, args=("ouvrir", "LHand")) # Creer le thread pour ouvrir la main.
    thread_ouvrir_main.start() # Demarer le thread.
    time.sleep(2) # Attendre 2 secondes.
    thread_fermer_main = threading.Thread(target=hand, args=("fermer", "LHand")) # Creer un thread pour fermer la main.
    thread_fermer_main.start() # Demarer le thread.
    # Attendre la fin des threads.
    thread_ouvrir_main.join()
    thread_fermer_main.join()
    for i in range (3): # Repeter trois fois,
        raiseLeftHand() # Lever le bras.
        lowerLeftHand() # Baisser le bras.
    hand("ouvrir","LHand") # Ouvrir la main.
    time.sleep(2) # Attendre deux secondes.
    hand("fermer","LHand") # Fermer la main. 

def raiseLeftHand():
    """
    Fonction pour lever le bras gauche. 
    """
    joints_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"  
    ] # Definir les articulations.
    target_angles = [
        math.radians(30), # LShoulderPitch
        math.radians(18.2), # LShoulderRoll 
        math.radians(-13.3), # LElbowYaw 
        math.radians(0), # LElbowRoll
        math.radians(-104.5), # LWristYaw
        0.02, # LHand 
    ] # Definir les angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Faire le mouvement.

def lowerLeftHand():
    """
    Baisser le bras gauche.
    """
    joints_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"  
    ] # Definir les articulations.
    target_angles = [
        math.radians(-30), # LShoulderPitch
        math.radians(18.2), # LShoulderRoll 
        math.radians(-13.3), # LElbowYaw 
        math.radians(0), # LElbowRoll
        math.radians(-104.5), # LWristYaw
        0.02, # LHand 
    ] # Definir les angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Faire le mouvement.

def shakeHandsLeft():
    """
    Serrer la main droite quand l'adversaire dit gauche.
    """
    joints_names = [ 
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" 
    ] # Definir les articulations.
    target_angles = [
        math.radians(0), # RShoulderPitch
        math.radians(-18.2), # RShoulderRoll
        math.radians(13.3), # RElbowYaw
        math.radians(0), # RElbowRoll 
        math.radians(0), # RWristYaw
        0.02, # RHand
    ] # Definir les angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Faire le mouvement.
    thread_ouvrir_main = threading.Thread(target=hand, args=("ouvrir", "RHand")) # Creer un thread pour ouvrir la main.
    thread_ouvrir_main.start() # Demarer le thread.
    time.sleep(2) # Attendre deux secondes.
    thread_fermer_main = threading.Thread(target=hand, args=("fermer", "RHand")) # Creer un thread pour fermer la main.
    thread_fermer_main.start() # Demarer le thread.
    # Attendre la fin des threads.
    thread_ouvrir_main.join()
    thread_fermer_main.join()
    for i in range (3): # Repeter trois fois,
        raiseRightHand() # Lever le bras.
        lowerRightHand() # Baisser le bras.
    hand("ouvrir","RHand") # Ouvrir la main.
    time.sleep(2) # Attendre deux secondes.
    hand("fermer","RHand") # Fermer la main.
        
def lowerRightHand():
    """
    Baisser le bras droit.
    """
    joints_names = [ 
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" 
    ] # Definir les articulations.
    target_angles = [
        math.radians(30), # RShoulderPitch
        math.radians(-18.2), # RShoulderRoll
        math.radians(13.3), # RElbowYaw
        math.radians(0), # RElbowRoll 
        math.radians(0), # RWristYaw
        0.02, # RHand
    ] # Definir les angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Faire le mouvement.

def raiseRightHand():
    """
    Baisser le bras droit.
    """
    joints_names = [ 
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" 
    ] # Definir les articulations.
    target_angles = [
        math.radians(-30), # RShoulderPitch
        math.radians(-18.2), # RShoulderRoll
        math.radians(13.3), # RElbowYaw
        math.radians(0), # RElbowRoll 
        math.radians(0), # RWristYaw
        0.02, # RHand
    ] # Definir les angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Faire le mouvement.

def hand(action, main_concernee):
    """
    Ouvrir ou fermer la main choisit.
    """
    if action == "ouvrir": # Si l action est ouvrir,
        if main_concernee == "RHand": # Si la main est la main droite.
            motion.openHand("RHand") # Ouvrir la main droite.
            print("Nao ouvre la main droite.") # Suivis dans la console.
        elif main_concernee == "LHand": # Si la main est la main gauche.
            motion.openHand("LHand") # Ouvrir la main gauche.
            print("Nao ouvre la main gauche.") # Suivis dans la console.
        else:
            print("ERREUR : Instruction non comprise") # Suivis dans la console.
    elif action == "fermer": # Si l action est fermer,
        if main_concernee == "RHand": # Si la main est la main droite.
            motion.closeHand("RHand") # Fermer la main droite.
            print("Nao ferme la main droite.") # Suivis dans la console.
        elif main_concernee == "LHand": # Si la main est la main gauche.
            motion.closeHand("LHand") # Fermer la main gauche. 
            print("Nao ferme la main gauche.") # Suivis dans la console.
        else:
            print("ERREUR : Instruction non comprise") # Suivis dans la console.
    else:
        print("ERREUR : Instruction non comprise") # Suivis dans la console.

def start2F(color):
    """
    Fonction pour commencer le jeu.

    Argument :
    color -- couleur

    """
    print("Debut fonction : start2F.") # Indicate in the console for follow-up.
    globalVar.TexteARepete = "Es-tu pret a jouer?"
    tts.say("Es-tu pret a jouer?")  # Nao demande au jouer si il est pret a jouer.
    asr.pause(True) # En attente de detection.
    asr.setVocabulary(["oui", "non"], False)  # Mettre les mots reconnus.
    asr.setLanguage("French")  # Mettre le language en francais. 
    asr.pause(False) # Fin d'analyse.
    asr.subscribe("Test_ASR")
    while True:
        time.sleep(3) # Attendre trois secondes.
        answer = memory.getData("WordRecognized")  # Recuperer les mots reconnu par Nao.
        asr.unsubscribe("Test_ASR")
        if answer and len(answer) > 0: # Si la reponse est valide,
            print("Nao a comprit a la question Es-tu pret a jouer ? ", answer[0].lower()) # Indiquer dans la console le suivi. 
            recognized_word = answer[0].lower()  # convertir le mot en minscule.
            if recognized_word == "oui": # Si l'adversaire dit oui,
                print("Nao a comprit oui.") # Indiquer dans la console le suivi. 
                globalVar.TexteARepete = "Ok, je joue les pions de couleur " + color + ". Je ne peux pas deplacer les piesses tout seul, alors jai besoin que vous deplaciez les piesses quand je vous le demande, ssil vous plait. Comme vous pouvez le constater, vous avez a votre disposition une application qui simule un taillemeur classique pour les jeux deschaics. Ce taillemeur indique le temps total restant a chaque joueur pour lenssemble de la partie. Vous trouverez aigalement plusieurs boutons : en cliquant sur le chrono de votre adversaire, vous arraitez votre tour et activez celui de votre adversaire. Avant le daibu de la partie, et de maniaire daifinitive, vous pouvez sailectionner une option pour ajouter 30 secondes a votre temps total a chaque nouveau tour. Il y a aussi un bouton 'raipaiter' qui me permet de raipaiter ce que jai dit si vous ne lavez pas compris. Mais dabord, quel niveau de jeu voulez-vous faire ? Donnez-moi un chiffre entre 1 et 4 en franssais."
                tts.say("Ok, je joue les pions de couleur " + color + ". Je ne peux pas deplacer les piesses tout seul, alors jai besoin que vous deplaciez les piesses quand je vous le demande, ssil vous plait.")  # Nao dit.
                tts.say("Comme vous pouvez le constater, vous avez a votre disposition une application qui simule un taillemeur classique pour les jeux deschaics. Ce taillemeur indique le temps total restant a chaque joueur pour lenssemble de la partie. Vous trouverez aigalement plusieurs boutons : en cliquant sur le chrono de votre adversaire, vous arraitez votre tour et activez celui de votre adversaire. Avant le daibu de la partie, et de maniaire daifinitive, vous pouvez sailectionner une option pour ajouter 30 secondes a votre temps total a chaque nouveau tour. Il y a aussi un bouton 'raipaiter' qui me permet de raipaiter ce que jai dit si vous ne lavez pas compris.")# Nao dit.
                tts.say("Mais dabord, quel niveau de jeu voulez-vous faire ? Donnez-moi un chiffre entre 1 et 4 en franssais.")  # Nao dit.
                asr.pause(True) # En attente de detection.
                asr.setVocabulary(["un", "deux", "trois", "quatre"], False) # Mettre les mots reconnus.
                asr.setLanguage("French") # Mettre le language en Francais. 
                asr.pause(False) # Fin de detection.
                asr.subscribe("Test_ASR") 
                time.sleep(3) # Attendre trois secondes.
                answerLevel = memory.getData("WordRecognized") # Recuperer les mots reconnu par Nao.
                print("Nao a comprit a la question Quel niveau veux tu jouer? ", answerLevel) # Indiquer dans la console le suivi. 
                res = choiceLevel(answerLevel)  # Envoyer le niveau choisit au cerveau.
                time.sleep(5) # Attendre cinq secondes.
                break
            elif recognized_word == "non": # Si l'adversaire refuse,
                print("Nao a comprit non.") # Indiquer dans la console le suivi. 
                globalVar.TexteARepete = "Je comprends, je suis un joueur redoutable !"
                tts.say("Je comprends, je suis un joueur redoutable !")  # Nao dit.
                break
        print("Nao a rien comprit.") # Indiquer dans la console le suivi. 
        globalVar.TexteARepete = "Daizoler, je nai pas compris. Etes-vous pret a jouer aux echecs ? Dites oui ou non, ssil vous plait."
        tts.say("Daizoler, je nai pas compris. Etes-vous pret a jouer aux echecs ? Dites oui ou non, ssil vous plait.")  # Nao dit.
        asr.subscribe("Test_ASR")
    print("Fin  fonction : start2F.") # Indicate in the console for follow-up.
    return res

def choiceLevel(level):
    """
    Fonction pour envoyer le niveau de jeu chosiit par l'adversaire au cerveau/IA.

    Argument :
    level -- niveau que le joueur a dit

    Retourner :
    Le niveau.

    """
    print("Debut fonction : choiceLevel.") # Indicate in the console for follow-up.
    niveau = 0 # Initialiser une variable qui stocke le menu choisit.
    if level and len(level) > 0: # Si l'adversaire choisit un niveau,
        word = level[0].lower() # prendre le premier element de la liste,
        print(word)
        if word == "un": # Si l'utilisateur repond niveau 1,
            print("Dans la fonction choice level, on est dans le if 1.") # Indiquer dans la console pour le suivis.
            globalVar.TexteARepete = "Ok, tu as choisis le niveau un."
            tts.say("Ok, tu as choisis le niveau un.") # Nao dit.
            niveau = 1 # Mettre le niveau a 1.
        elif word == "deux": # Si l'utilisateur repond niveau 2,
            print("Dans la fonction choice level, on est dans le if 2.") # Indiquer dans la console pour le suivis.
            globalVar.TexteARepete = "Ok, tu as choisis le niveau deux."
            tts.say("Ok, tu as choisis le niveau deux.") # Nao dit.
            niveau = 2 # Mettre le niveau a 2.
        elif word == "trois": # Si l'utilisateur repond niveau 3,
            print("Dans la fonction choice level, on est dans le if 3.") # Indiquer dans la console pour le suivis.
            globalVar.TexteARepete = "Ok, tu as choisis le niveau trois."
            tts.say("Ok, tu as choisis le niveau trois.") # Nao dit.
            niveau = 3 # Mettre le niveau a 3.
        elif word == "quatre": # Si l'utilisateur repond niveau 4,
            print("Dans la fonction choice level, on est dans le if 4.") # Indiquer dans la console pour le suivis.
            globalVar.TexteARepete = "Ok, tu as choisis le niveau quatre."
            tts.say("Ok, tu as choisis le niveau quatre.") # Nao dit.
            niveau = 4 # Mettre le niveau a 4.
        else :
            print("Nao n'a pas comprit") # Indiquer dans la console pour le suivis.
            globalVar.TexteARepete= "Daizoler, je nai pas compris le niveau que vous avez indiquer. Pouvez-vous me dire le niveau que vous avez choisi entre 1 et 4 ssil vous plait ? Noubliez pas de dire le numero."
            tts.say("Daizoler, je nai pas compris le niveau que vous avez indiquer. Pouvez-vous me dire le niveau que vous avez choisi entre 1 et 4 ssil vous plait ? Noubliez pas de dire le numero.") # Nao dit.
            asr.pause(True) # Activer la reconnaissance vocale.
            asr.setVocabulary(["un", "deux", "trois", "quatre"], False) # Mettre les mots a reconnaitre.
            asr.setLanguage("French") # Mettre le langage en francais.
            asr.pause(False) # Arreter la reconnaissance vocale.
            asr.subscribe("Test_ASR")
            time.sleep(5) # Attendre.
            answerLevel = memory.getData("WordRecognized") # Avoir le mot prononce l'adversaire.
            choiceLevel(answerLevel) # Relancer la fonction.
            return 0 # Sortir de la fonction.
    shakeHands() # Appeler la fonction serrer la main.
    return niveau # Retourner le niveau.
    print("Fin fonction : choiceLevel.") # Indicate in the console for follow-up.

def armsUp():
    """
    Fonction pour la position des bras de Nao quand il pleure.
    """
    print("Debut fonction : armsUp.") # Indicate in the console for follow-up.
    joints_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", 
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" 
    ] # Definir les angles des bras.
    target_angles = [
        # Bras gauche.
        math.radians(-31.9), # LShoulderPitch
        math.radians(18.2), # LShoulderRoll 
        math.radians(-13.3), # LElbowYaw 
        math.radians(-88.5), # LElbowRoll
        math.radians(-104.5), # LWristYaw
        0.02, # LHand 

        # Bras droit.
        math.radians(-31.9), # RShoulderPitch
        math.radians(-18.2), # RShoulderRoll
        math.radians(13.3), # RElbowYaw
        math.radians(88.5), # RElbowRoll 
        math.radians(104.5), # RWristYaw
        0.02, # RHand
    ] # Appliquer les angles aux articuations.
    print("Nao fait le mouvement de lever ses mains pour pleurer") # Indiquer dans la console pour le suivis.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Faire le mouvement.
    endTime = time.time() + 2  # Attendre deux secondes.
    while time.time() < endTime: # Tant que le temps ecoule est inferieur a deux secondes,
        motion.setAngles(joints_names, target_angles, 0.1)  # maintenir la position.
        time.sleep(0.1)  # Attendre.
    print("Nao a finit le mouvement de lever ses mains pour pleurer") # Indiquer dans la console pour le suivis.
    print("Fin fonction : armsUp.") # Indicate in the console for follow-up.

def songCheckmate(): 
    """
    Fonction pour lancer le son quand Nao perd.
    """
    print("Debut fonction : songCheckmate.") # Indicate in the console for follow-up.
    audio = "/home/nao/Niels/checkmat_reaction.mp3"  # Chemin du son.
    audioPlayer.playFile(audio)  # Play audio
    print("Lancer son.") # Indiquer dans la console pour le suivis.
    print("Fin fonction : songCheckmate.") # Indicate in the console for follow-up.

def checkmateF():
    """
    Fonction quand Nao perd une partie.
    """
    print("Debut fonction : checkmateF.") # Indicate in the console for follow-up.
    sit()  # Nao s'assoit.
    print("Changement des couleurs de leds.") # Indiquer dans la console pour le suivis.
    leds.fadeRGB("FaceLeds", 0x0000FF, 1.0)  # Mettre les yeux bleu.
    leds.fadeRGB("ChestLeds", 0x0000FF, 0) # Mettre le logo bleu.
    leds.fadeRGB("FeetLeds", 0x0000FF, 0) # Mettre les pieds bleu.
    threadArms = threading.Thread(target=armsUp) # Creer un thread pour le mouvement des bras.
    threadSong = threading.Thread(target=songCheckmate) # Creer un thread pour le son.
    print("Execution des threads.") # Indiquer dans la console pour le suivis.
    # Executer les threads.
    threadArms.start()
    threadSong.start()
    # Attendre la fin des threads.
    threadArms.join()
    threadSong.join()
    print("Fin d'execution des threads.") # Indiquer dans la console pour le suivis.
    print("Reinitialisation des leds et volume en cours.") # Indiquer dans la console pour le suivis.
    resetLeds() # Reinitialiser les leds.
    audioDevice.setOutputVolume(100)  # Reinitialiser le volume.
    print("Reinitialisation des leds et volume fait.") # Indiquer dans la console pour le suivis.
    print("Fin fonction : checkmateF") # Indiquer dans la console pour le suivis.

def checkF():
    """
    Fonction quand Nao est en echec.
    """
    print("Debut fonction : checkF.") # Indicate in the console for follow-up.
    print("Changement des couleurs de leds.") # Indiquer dans la console pour le suivis.
    leds.fadeRGB("FaceLeds", 0x0000FF, 1.0) # Mettre les yeux bleu.
    leds.fadeRGB("ChestLeds", 0x0000FF, 0) # Mettre le logo bleu.
    leds.fadeRGB("FeetLeds", 0x0000FF, 0) # Mettre les pieds bleu.
    print("Lancement son.") # Indiquer dans la console pour le suivis.
    audio = "/home/nao/Niels/check_reaction.mp3"  # Chemin du son
    audioDevice.setOutputVolume(50)  # Mettre le volume du son a 50.
    audioPlayer.playFile(audio)  # Jouer le son.
    print("Reinitialisation des leds et volume en cours.") # Indiquer dans la console pour le suivis.
    resetLeds() # Reinitialiser les leds.
    audioDevice.setOutputVolume(100)  # Reinitialiser le volume.
    print("Reinitialisation des leds et volume fait.") # Indiquer dans la console pour le suivis.
    print("Fin fonction : checkF") # Indiquer dans la console pour le suivis.

def disruptF():
    """
    Fonction pour distraire l'adversaire.
    """
    print("Debut fonction : disruptF.") # Indicate in the console for follow-up.
    reaction = ["chante",
                "petitPet",
                "Tu a aiter bercer trop prais du mur ?", 
                "Tu es tellement loin dairriaire que tu es persuader daitre le premier.", 
                "Tu nai pas encombrer par le processus de penser.", 
                "Je nattendais rien de toi je suis quand maime daissu.",  
                "Tu ai gentil mais je ne ferais pas un ailevage de toi.", 
                "La roue tourne, mais le hammsstaire est visiblement dessaider.", 
                "Tu nai pas le pingouin le plus glissant de la banquise.", 
                "C impossible de te sous-estimer.", 
                "Il lui manque dix minutes de cuisson.",
                "ATCHOOOUMM",
                "Tu ai la raison pour laquelle nous utilisons des panneaux AVERTISSEMENT."
                ] # Liste des actions possibles.
    nbRandom = randint(0,len(reaction)-1) # Generer un nombre aleatoire.
    action = reaction[nbRandom] # Recuperer une distraction aleatoire.
    if action == "chante": # Si l'action est de chanter.
        print("Action aleatoire de distraction : chante") # Indiquer dans la console pour le suivis.
        audio = "/home/nao/Niels/disrupt_reaction.mp3"  # Chemin du fichier audio.
        audioDevice.setOutputVolume(70)  # Mettre le volume a 70.
        print("Lancement son.") # Indiquer dans la console pour le suivis.
        audioPlayer.playFile(audio)  # Jouer le son.
        print("Reinitialisation du volume en cours.") # Indiquer dans la console pour le suivis.
        audioDevice.setOutputVolume(100)  # Reinitialiser le son.
        print("Reinitialisation du volume fait.") # Indiquer dans la console pour le suivis.
    elif action == "petitPet": # Si l'action est petitPet,
        print("Action aleatoire de distraction : petitPet") # Indiquer dans la console pour le suivis.
        audio = "/home/nao/Niels/petPetit.mp3"  # Chemin du fichier audio.
        audioDevice.setOutputVolume(70)  # Mettre le son a 70.
        print("Lancement son.") # Indiquer dans la console pour le suivis.
        audioPlayer.playFile(audio)  # Jouer le son.
        print("Reinitialisation du volume en cours.") # Indiquer dans la console pour le suivis.
        audioDevice.setOutputVolume(100)  # Reinitialiser le volume.
        print("Reinitialisation du volume fait.") # Indiquer dans la console pour le suivis.
    else:
        print("Action aleatoire de distraction : phrase") # Indiquer dans la console pour le suivis.
        globalVar.TexteARepete = action
        tts.say(action) # Nao dit.
    print("Fin fonction : disruptF") # Indiquer dans la console pour le suivis.
    
def sayCaseF(deplacement):
    """
    Fonction pour indiquer et dire le mouvement de pion.

    Argument:
    deplacement -- Le deplacement de pion sous la forme caseDeDepart/caseDArrivee/nomPionAnglais/nomPionFrancais.

    """
    print("Debut fonction : sayCaseF.") # Indicate in the console for follow-up.
    if '/' not in deplacement: # Si le parametre n'a pas un /,
        print("ERREUR : Aucun / dans le parametre.") # Indiquer dans la console pour le suivis.
        return # Arreter la fonction.
        
    parts = deplacement.split('/') # Separer le parametre par /.
    if len(parts) != 4: # Si le parametre n'est pas diviser en quatre.
        print("ERREUR : Le parametre n est pas diviser en quatre.") # Indiquer dans la console pour le suivis.
        return # Arreter la fonction.
       

    startingCase = parts[0].strip()  # Avoir la case de depart.
    startingCase.upper()
    arrivalCase = parts[1].strip() # Avoir la case d arrivee.
    arrivalCase.upper()
    namePawn = parts[3].strip() # Avoir le nom du pion.
    print("Nao dit son deplacement") # Indiquer dans la console pour le suivis.
    threadTalk = threading.Thread(target=sayPawn, args=(namePawn, startingCase, arrivalCase))
    threadMoov = threading.Thread(target=get_angle_en_fonction_case, args=(startingCase + arrivalCase,)) 
    # Executee les threads.
    print("Debut de thread pour indiquer les deplacement.") # Indiquer dans la console pour le suivis.
    threadMoov.start()
    threadTalk.start()
    # Attendre la fin des threads.
    threadTalk.join()
    threadMoov.join()
    print("Fin de thread pour indiquer les deplacement.") # Indiquer dans la console pour le suivis.

def sayPawn(namePawn, startingCase, arrivalCase):
    """
    Fonction pour  dire le mouvement de pion.

    Arguments:
    namePawn -- Le nom de pion.
    startingCase -- La case de depart.
    arrivalCase -- La case d arrivee.
    
    """
    globalVar.TexteARepete = "Peux tu bouger le " + namePawn + " qui ai a la case " + startingCase + " a la case " + arrivalCase + " s'il te plait ?"
    tts.say("Peux tu bouger le " + namePawn + " qui ai a la case ") # Nao dit.
    time.sleep(0.1)
    tts.say(startingCase) # Nao dit.
    time.sleep(0.1)
    tts.say(" a la case ") # Nao dit.
    time.sleep(0.1)
    tts.say(arrivalCase) # Nao dit.
    time.sleep(0.1)
    tts.say(" s'il te plait ?") # Nao dit.
    print("Nao a finit de dire son deplacement") # Indiquer dans la console pour le suivis.
    print("Fin fonction : sayCaseF.") # Indicate in the console for follow-up.

def pawnEatenF(namePawn):
    """
    Fonction quand l'adversaire mange un pion de Nao.

    Argument :
    namePawn -- Le nom de pion.
    
    """
    print("Debut fonction : pawnEatenF.") # Indicate in the console for follow-up.
    print("Changement des couleurs de leds.") # Indiquer dans la console pour le suivis.
    leds.fadeRGB("FaceLeds", 0x0000FF, 0) # Mettre les yeux bleu.
    leds.fadeRGB("ChestLeds", 0x0000FF, 0) # Mettre le logo bleu.
    leds.fadeRGB("FeetLeds", 0x0000FF, 0) # Mettre les pieds bleu.
    globalVar.TexteARepete = namePawn + " a erter manger."
    tts.say(namePawn + " a erter manger.") # Nao dit.
    audio = "/home/nao/Niels/cry.mp3"  # Chemin du son.
    print("Lancement son.") # Indiquer dans la console pour le suivis.
    audioPlayer.playFile(audio)  # Jouer le son.
    print("Reinitialisation des leds en cours.") # Indiquer dans la console pour le suivis.
    resetLeds() # Reinitialiser les leds.
    print("Reinitialisation des leds fait.") # Indiquer dans la console pour le suivis.
    print("Fin fonction : pawnEatenF.") # Indicate in the console for follow-up.

def eatPawnF(namePawn):
    """
    Fonction quand Nao mange un pion.

    Argument :
    namePawn -- Le nom de pion.
    
    """
    print("Debut fonction : eatPawnF.") # Indicate in the console for follow-up.
    print("Changement des couleurs de leds.") # Indiquer dans la console pour le suivis.
    leds.fadeRGB("FaceLeds", 0xFFFF00, 0) # Mettre les yeux jaune.
    leds.fadeRGB("ChestLeds", 0xFFFF00, 0) # Mettre le logo jaune.
    leds.fadeRGB("FeetLeds", 0xFFFF00, 0) # Mettre les pieds jaune.
    globalVar.TexteARepete = namePawn + " a erter manger par moi."
    tts.say(namePawn + " a erter manger par moi.") # Nao dit.
    print("Lancement son.") # Indiquer dans la console pour le suivis.
    audio = "/home/nao/Niels/laugh.mp3"  # Chemin du son.
    audioPlayer.playFile(audio)  # Jouer le son.
    print("Reinitialisation des leds en cours.") # Indiquer dans la console pour le suivis.
    resetLeds() # Reinitialiser les leds.
    print("Reinitialisation des leds fait.") # Indiquer dans la console pour le suivis.
    print("Fin fonction : eatPawnF.") # Indicate in the console for follow-up.

def choicePawnAtEndF(namePawn):
    """
    Fonction quand un des pions de Nao arrive de l'autre cote du plateau et qu'il choisit son nouveau pion.

    Argument :
    namePawn -- Le nom de pion.
    
    """
    print("Debut fonction : choicePawnAtEndF.") # Indicate in the console for follow-up.
    print("Nao parle.") # Indiquer dans la console pour le suivis.
    globalVar.TexteARepete = "Mon pion devient " + namePawn
    tts.say("Mon pion devient " + namePawn) # Nao dit.
    print("Nao a finit de parler.") # Indiquer dans la console pour le suivis.
    print("Fin fonction : choicePawnAtEndF.") # Indicate in the console for follow-up.

def winningF():
    """
    Fonction quand Nao est entrain de gagner.
    """
    print("Debut fonction : winningF.") # Indicate in the console for follow-up.
    print("Changement des couleurs de leds.") # Indiquer dans la console pour le suivis.
    leds.fadeRGB("FaceLeds", 0xFFFF00, 0) # Mettre les yeux jaune.
    leds.fadeRGB("ChestLeds", 0xFFFF00, 0) # Mettre le logo jaune.
    leds.fadeRGB("FeetLeds", 0xFFFF00, 0) # Mettre les pieds jaune.
    sentences = ["Felicitations, tu viens de remporter le prix du champion du monde des boulets !",  
                "Je ne veux pas dire que tu es dans de sales draps, mais ta machine a laver appelle un service d'urgence.", 
                "Ne tinquiaite pas si tu ne gagne pas la partie daichec, tu gagneras le prix de te foutre dans la merde.",
                "On dirait que tu es en train de nager dans une piscine de baitises sans bouer de sauvetage", 
                "On dirait que tu as raiussi a te mettre dans la merde.",
                "Avec tou sa, tu pourrais aicrire un manuel : Comment ssenfoncer avec style !",
                "Tu lui donne un aiventail, il va secouer la taite.",
                "Lui il a une taite a aiplucher les cailloux.",
                "Tu na pas inventer la poudre, mais tu naitais pas loins quand le canon a exploser.",
                "Tu es comme un aimant a ennuis, tu devrais peutaitre changer de marque !"
                ] # Liste des actions.
    nbRandom = randint(0,len(sentences)-1) # Generer un nombre aleatoire.
    sentence = sentences[nbRandom] # Avoir une reaction aleatoire.
    print("Nao parle.") # Indiquer dans la console pour le suivis.
    globalVar.TexteARepete = sentence
    tts.say(sentence) # Nao dit.
    print("Nao a finit de parler.") # Indiquer dans la console pour le suivis.
    print("Reinitialisation des leds et volume en cours.") # Indiquer dans la console pour le suivis.
    resetLeds() # Reinitialiser les leds.
    print("Reinitialisation des leds et volume fait.") # Indiquer dans la console pour le suivis.
    print("Fin fonction : winningF.") # Indicate in the console for follow-up.

def eyesMultiColored():
    """
    Fonction pour mettre les yeux de Nao multicolore.
    """
    print("Debut fonction : eyesMultiColored.") # Indicate in the console for follow-up.
    colors = [0xff0000, 0xffed00, 0x00ffc8, 0x0042ff, 0x6c00ff, 0xca00ff, 0xff0096] # Liste des couleurs.
    for i in colors: # Pour chaque couleur, 
        print("Changement couleur led.") # Indiquer dans la console pour le suivis.
        leds.fadeRGB("FaceLeds", i, 1.0) # mettre les yeux dans la couleur.
        time.sleep(0.2) # Attendre.
    print("Fin fonction : eyesMultiColored.") # Indicate in the console for follow-up.
    
def sayCheckF():
    """
    Fonction quand Nao fait un echec.
    """
    print("Debut fonction : sayCheckF.") # Indicate in the console for follow-up.
    print("Changement des couleurs de leds.") # Indiquer dans la console pour le suivis.
    leds.fadeRGB("FaceLeds", 0xFFFF00, 1.0) # Mettre les yeux jaune.
    leds.fadeRGB("ChestLeds", 0xFFFF00, 0) # Mattre le logo jaune.
    leds.fadeRGB("FeetLeds", 0xFFFF00, 0) # Mettre les pieds jaune.
    print("Nao parle.") # Indiquer dans la console pour le suivis.
    globalVar.TexteARepete = "Echec"
    tts.say("Echec") # Nao dit.
    print("Nao a finit de parler.") # Indiquer dans la console pour le suivis.
    audio = "/home/nao/Niels/laugh.mp3" # Chemin du son.
    print("Lancement son.") # Indiquer dans la console pour le suivis.
    audioPlayer.playFile(audio) # Jouer le son.
    print("Reinitialisation des leds et volume en cours.") # Indiquer dans la console
    resetLeds() # Reinitialiser les leds.
    print("Reinitialisation des leds et volume fait.") # Indiquer dans la console pour le suivis.
    print("Fin fonction : sayCheckF.") # Indicate in the console for follow-up.

#----------------------------------------------------------MOUVEMENTS DE DANSE---------------------------------------------------------------------------
def danceArmsDisco1():
    """
    Fonction pour le premier mouvement de danse avec les bras.
    """
    jointNames = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", # Bras gauche.
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"   # Bras droit.
    ]
    anglesMoovDance1 = [
        # Bras gauche
        math.radians(53.7),  # LShoulderPitch
        math.radians(-18.0),  # LShoulderRoll
        math.radians(-9.8),  # LElbowYaw
        math.radians(-57.0),  # LElbowRoll
        math.radians(12.4),  # LWristYaw
        math.radians(1.0),  # LHand

        # Bras droit.
        math.radians(-64.0),  # RShoulderPitch
        math.radians(-46.7),  # RShoulderRoll
        math.radians(-35.2),  # RElbowYaw
        math.radians(2.0),  # RElbowRoll
        math.radians(-40.7),  # RWristYaw
        math.radians(0.0),  # RHand
    ]
    duration = 2.0  # Duree du mouvement.
    print("Nao Debut un mouvement danceArmsDisco1.") # Indiquer dans la console pour le suivis.
    motion.angleInterpolation(jointNames, anglesMoovDance1, [duration]*len(jointNames), True) # Faire le mouvement.
    print("Nao fin un mouvement danceArmsDisco1.") # Indiquer dans la console pour le suivis.

def danceArmsDisco2():
    """
    Fonction du deuxieme mouvement de danse avec les bras.
    """
    jointNames = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", # Bras gauche.
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" # Bras droit.
    ]
    anglesMoovDance2 = [
        # Bras gauche
        math.radians(-63.3),  # LShoulderPitch
        math.radians(52.1),  # LShoulderRoll
        math.radians(-0.4),  # LElbowYaw
        math.radians(-2.0),  # LElbowRoll
        math.radians(104.5),  # LWristYaw
        math.radians(1.0),  # LHand

        # Bras droit.
        math.radians(45.4),  # RShoulderPitch
        math.radians(15.1),  # RShoulderRoll
        math.radians(30.4),  # RElbowYaw
        math.radians(82.7),  # RElbowRoll
        math.radians(20.4),  # RWristYaw
        math.radians(0.0),  # RHand
    ]
    duration = 2.0  #  Duree du mouvement.
    print("Nao Debut un mouvement danceArmsDisco2.") # Indiquer dans la console pour le suivis.
    motion.angleInterpolation(jointNames, anglesMoovDance2, [duration]*len(jointNames), True) # Faire le mouvement.
    print("Nao fin un mouvement danceArmsDisco2.") # Indiquer dans la console pour le suivis.

def danceLegDisco1():
    """
    Fonction pour le premier mouvement de danse avec les jambes.
    """
    jointNames = [
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll", # Jambes gauches.
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"  # Jambes droites.
    ]
    anglesMoovLegDance1 = [
        # Jambes gauches.
        math.radians(-20.9),  # LHipYawPitch
        math.radians(-1.1),  # LHipRoll
        math.radians(-44.3),  # LHipPitch
        math.radians(121.0),  # LKneePitch
        math.radians(-68.2),  # LAnklePitch
        math.radians(4.7),  # LAnkleRoll

        # Jambes droites.
        math.radians(-17.3),  # RHipYawPitch
        math.radians(-45.3),  # RHipRoll
        math.radians(-27.6),  # RHipPitch
        math.radians(-5.3),  # RKneePitch
        math.radians(30.5),  # RAnklePitch
        math.radians(-25.2),  # RAnkleRoll
    ]
    duration = 2.0  #  Duree du mouvement.
    print("Nao Debut un mouvement danceLegDisco1.") # Indiquer dans la console pour le suivis.
    motion.angleInterpolation(jointNames, anglesMoovLegDance1, [duration]*len(jointNames), True) # Faire le mouvement.
    print("Nao fin un mouvement danceLegDisco1.") # Indiquer dans la console pour le suivis.

def danceLegDisco2():
    """
    Fonction pour le deuxieme mouvement de danse avec les jambes.
    """
    jointNames = [
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll", # Jambes gauches.
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"  # Jambes droites.
    ]
    anglesMoovLegDance2 = [
        # Jambes gauches.
        math.radians(-1.1),  # LHipYawPitch
        math.radians(45.3),  # LHipRoll
        math.radians(13.9),   # LHipPitch
        math.radians(-5.3),  # LKneePitch
        math.radians(-0.9),  # LAnklePitch
        math.radians(7.3),   # LAnkleRoll

        # Jambes droites.
        math.radians(-1.1),  # RHipYawPitch
        math.radians(-8.0),   # RHipRoll
        math.radians(-47.5),    # RHipPitch
        math.radians(121.0),   # RKneePitch
        math.radians(-68.0),    # RAnklePitch
        math.radians(-3.4),    # RAnkleRoll
    ]
    duration = 2.0   #  Duree du mouvement.
    print("Nao Debut un mouvement danceLegDisco2.") # Indiquer dans la console pour le suivis.
    motion.angleInterpolation(jointNames, anglesMoovLegDance2, [duration]*len(jointNames), True) # Faire le mouvement.
    print("Nao fin un mouvement danceLegDisco2.") # Indiquer dans la console pour le suivis.

def dabDance():
    """
    Fonction pour faire le mouvement de DAB.
    """
    jointNames = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", # Bras gauche.
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"   # Bras droit.
    ]
    anglesMoovDance1 = [
        # Bras gauche.
        math.radians(-73.1),  # LShoulderPitch
        math.radians(74.0),  # LShoulderRoll
        math.radians(-38.7),  # LElbowYaw
        math.radians(-2.0),  # LElbowRoll
        math.radians(27.2),  # LWristYaw
        math.radians(1.0),  # LHand

        # Bras droit.
        math.radians(-33.2),  # RShoulderPitch
        math.radians(46.8),  # RShoulderRoll
        math.radians(34.9),  # RElbowYaw
        math.radians(69.1),  # RElbowRoll
        math.radians(7.0),  # RWristYaw
        math.radians(1.0),  # RHand
    ]
    duration = 2.0  #  Duree de l'animation.
    print("Nao Debut un mouvement dabDance.") # Indiquer dans la console pour le suivis.
    motion.angleInterpolation(jointNames, anglesMoovDance1, [duration]*len(jointNames), True) # Faire le mouvement.
    print("Attendre 4 secondes dabDance.") # Indiquer dans la console pour le suivis.
    time.sleep(4)
    print("Nao fin un mouvement dabDance.") # Indiquer dans la console pour le suivis.

def legsApartDance():
    """
    Fonction de mouvement de DAB au niveau des pieds.
    """
    jointNames = [
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll", # Jambes gauches.
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"  # Jambes droites.
    ]
    anglesMoovLegDance2 = [
        # Jambes gauches.
        math.radians(-8.9),  # LHipYawPitch
        math.radians(25.6),  # LHipRoll
        math.radians(16.4),   # LHipPitch
        math.radians(-3.5),  # LKneePitch
        math.radians(1.4),  # LAnklePitch
        math.radians(-22.8),   # LAnkleRoll

        # Jambes droites.
        math.radians(-8.9),  # RHipYawPitch
        math.radians(-30.5),   # RHipRoll
        math.radians(14.8),    # RHipPitch
        math.radians(-5.3),   # RKneePitch
        math.radians(7.0),    # RAnklePitch
        math.radians(22.8),    # RAnkleRoll
    ]
    duration = 4.0  #  Duree de l'animation.
    print("Nao Debut un mouvement legsApartDance.") # Indiquer dans la console pour le suivis.
    motion.angleInterpolation(jointNames, anglesMoovLegDance2, [duration]*len(jointNames), True) # Faire le mouvement.
    print("Attendre 4 secondes dabDance.") # Indiquer dans la console pour le suivis.
    time.sleep(4) # Attendre.
    print("Nao fin un mouvement legsApartDance.") # Indiquer dans la console pour le suivis.

def dance():
    """
    Fonction pour faire danser Nao.
    """
    print("Debut fonction : dance.") # Indicate in the console for follow-up.
    for i in range(2): # Rpeter deux fois,
        print("Nao se leve") # Indiquer dans la console pour le suivis.
        standUp() # Nao se leve.
        threadMoovArms1 = threading.Thread(target=danceArmsDisco1) # Creer un thread pour faire le premier mouvement de danse avec les bras.
        threadMoovLeg1= threading.Thread(target=danceLegDisco1) # Creer un thread pour faire le premier mouvement de danse avec les jambes.
        # Executee les threads.
        print("Debut de thread du premier mouvement de danse.") # Indiquer dans la console pour le suivis.
        threadMoovArms1.start()
        threadMoovLeg1.start()
        # Attendre la fin des threads.
        threadMoovArms1.join()
        threadMoovLeg1.join()
        print("Fin de thread du premier mouvement de danse.") # Indiquer dans la console pour le suivis.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print("Nao se leve") # Indiquer dans la console pour le suivis.
        standUp() # Nao se leve.
        print("Debut de thread du deuxieme mouvement de danse.") # Indiquer dans la console pour le suivis.
        threadMoovArms2 = threading.Thread(target=danceArmsDisco2) # Creer un thread pour faire le deuxieme mouvement de danse avec les bras.
        threadMoovLeg2= threading.Thread(target=danceLegDisco2) # Creer un thread pour faire le deuxieme mouvement de danse avec les jambes.
        # Executer les threads.
        threadMoovArms2.start()
        threadMoovLeg2.start()
        # Attendre la fin des threads.
        threadMoovArms2.join()
        threadMoovLeg2.join()
        print("Fin de thread du deuxieme mouvement de danse.") # Indiquer dans la console pour le suivis.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print("Nao se leve") # Indiquer dans la console pour le suivis.
    standUp() # Nao se leve.
    threadMoovHandsUp = threading.Thread(target=dabDance) # Creer un thread pour faire faire le DAB a Nao.
    threadMoovLegsApart = threading.Thread(target=legsApartDance) #Creer un thread pour mettre en position les jambes de Nao pour le DAB.
    # Executer les threads.
    print("Debut de thread du mouvement de DAB") # Indiquer dans la console pour le suivis.
    threadMoovHandsUp.start()
    threadMoovLegsApart.start()
    # Attendre la fin des threads.
    threadMoovHandsUp.join()
    threadMoovLegsApart.join()
    print("Fin de thread du mouvement de DAB") # Indiquer dans la console pour le suivis.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print("Nao se leve") # Indiquer dans la console pour le suivis.
    standUp() # Nao se leve.
    print("Fin fonction : dance.") # Indicate in the console for follow-up.
#-----------------------------------------------------------------------------------------------------------------------------------------
def songCheckmatewin():
    """
    Fonction pour lancer le son de victoire
    """
    print("Debut fonction : songCheckmatewin.") # Indicate in the console for follow-up.
    audio = "/home/nao/Niels/win.mp3" # Chemin du son.
    audioDevice.setOutputVolume(80)  # Mettre le volume a 50.
    print("Lancement son.") # Indiquer dans la console pour le suivis.
    audioPlayer.playFile(audio) # Jouer le son.
    print("Fin fonction : songCheckmatewin.") # Indicate in the console for follow-up.

def multiColored():
    """
    Fonction pour mettre les yeux multicolores. 
    """
    print("Debut fonction : multiColored.") # Indicate in the console for follow-up.
    for i in range (50): # Repeter 50 fois,
        colors = [0xff0000, 0xffed00, 0x00ffc8, 0x0042ff, 0x6c00ff, 0xca00ff, 0xff0096]  # Liste des couleurs.
        for color in colors:  # Pour chaque couleur,
            leds.fadeRGprint("Changement des couleurs de leds.") # Indiquer dans la console pour le suivis.B("FaceLeds", color, 0.1)  # Mettre les yeux en couleur.
            leds.fadeRGB("ChestLeds", color, 0.1)  # Mettre le ventre en couleur.
            leds.fadeRGB("FeetLeds", color, 0.1)  # Mettre les pieds en couleur.
    print("Fin fonction : multiColored.") # Indicate in the console for follow-up.

def winF():
    """
    Fonction quand Nao a gane la partie.
    """
    print("Debut fonction : winF.") # Indicate in the console for follow-up.
    print("Nao se leve") # Indiquer dans la console pour le suivis.
    standUp() # Nao se leve.
    print("Nao recule") # Indiquer dans la console pour le suivis.
    motion.moveTo(-0.3, 0.0, 0.0) # Faire reculer.
    print("Nao a finit de reculer et parle.") # Indiquer dans la console pour le suivis.
    globalVar.TexteARepete = "Echec et mat ! J'ai gagner ! Tu es nulle !"
    tts.say("Echec et mat ! J'ai gagner ! Tu es nulle !") # Nao dit.
    print("Nao a finit de parler.") # Indiquer dans la console pour le suivis.
    threadEyes = threading.Thread(target=multiColored) # Creer un thread pour mettre les yeux multicolores.
    threadDance = threading.Thread(target=dance) # Creer un thread pour faire danser Nao.
    threadSong = threading.Thread(target=songCheckmatewin) # Creer un thread pour lancer le son de fin.
    # Executer les threads.
    print("Debut de thread des yeux multicouleurs, danse et son.") # Indiquer dans la console pour le suivis.
    threadSong.start()
    threadEyes.start()
    threadDance.start()
    # Attendre la fin des threads.
    threadSong.join()
    threadEyes.join()
    threadDance.join()
    print("Fin de thread des yeux multicouleurs, danse et son.") # Indiquer dans la console pour le suivis.
    print("Reinitialisation des leds et volume en cours.") # Indiquer dans la console pour le suivis.
    audioDevice.setOutputVolume(100)  # Metrre le volume a 50.
    resetLeds() # Reinitialiser les leds.
    print("Reinitialisation des leds et volume fait.") # Indiquer dans la console pour le suivis.
    print("Nao se leve") # Indiquer dans la console pour le suivis.
    standUp() # Nao se leve.
    print("Fin fonction : winF.") # Indicate in the console for follow-up.

