# Definit les modules. // Define modules.
import sys
sys.path.append("z:\\Bureau\\Nao\\nao-chess\\movement\\")
sys.path.append("z:\\Bureau\\Nao\\nao-chess\\chess_game\\")
sys.path.append("C:\pynaoqi\lib")
from naoqi import ALProxy
from random import *
import time
import os
import math
import threading
from mainFrancaisVersion import *
from mainEnglishVersion import *
import globalVar 
import chess






robot_ip = "172.16.1.164"
robot_port = 9559



#-----------------------------------------------------------------------------------------------------------------------------------
# LE FRANCAIS EST ECRIT AVEC DES FAUTES CAR PYTHON NE PREND PAS EN CHARGE LES ACCENTS ET NAO NE PARLE PAS CORRECTEMENT LE FRANCAIS.
#-----------------------------------------------------------------------------------------------------------------------------------

def start(color):
    
    tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
    asr = ALProxy("ALSpeechRecognition", robot_ip, robot_port)
    audioPlayer = ALProxy("ALAudioPlayer", robot_ip, robot_port)
    audioDevice = ALProxy("ALAudioDevice", robot_ip, robot_port)
    leds = ALProxy("ALLeds", robot_ip, robot_port)
    motion = ALProxy("ALMotion", robot_ip, robot_port)
    posture = ALProxy("ALRobotPosture", robot_ip, robot_port)
    memory = ALProxy("ALMemory", robot_ip, robot_port)
 
    globalVar.language # Definir une variable globale. // Define a global variable.
    tts.setLanguage('English') # Mettre la langue en anglais. // Set the language to English. 
    globalVar.TexteARepete = "Do you want to play in French or English"
    tts.say("Do you want to play in French or English") # Nao dit. // Nao says.
    tts.setLanguage('French')  # Mettre la langue en francais. // Set the language to French. 
    globalVar.TexteARepete = "Veux-tu jouer en franssais ou en anglais"
    tts.say('Veux-tu jouer en franssais ou en anglais') # Nao dit. // Nao says.
    asr.pause(True) # Attendre la detection. // Waiting for detection.
    asr.setVocabulary(["french", "english","franssais","anglais"], False)  # Mettre les mots reconnaissable. // Set words to recognize.
    asr.pause(False) # Fin de l'analyse. // End of analysis.
    asr.subscribe("Test_ASR")
    while True:
        time.sleep(3) # Attendre 3 secondes. // Wait three second.
        answer = memory.getData("WordRecognized")  # Recuperer les mots reconnu. // Get recognized words
        asr.unsubscribe("Test_ASR")
        if answer and len(answer) > 0: # Si la reponse est valide. // If a valid response was recognized,
            print(answer[0].lower()) # Indicate follow-up in the console. 
            #MARC print_out("Nao a comprit en reponse  a Es tu pret a jouer ? :" + answer[0].lower()) 
            recognizedWord = answer[0].lower()  # convert the recognized word to lowercase
            if recognizedWord == "french" or recognizedWord == "franssais": # Si l'utilisateur choisit francais, // If the user says French,
                globalVar.TexteARepete = "Bonjour! je parle franssais"
                tts.say("Bonjour! je parle franssais") # Nao dit. // Nao says.
                if(color == True):
                    color = "Blan" # alors mettre la couleur blanche.
                else :
                    color = "Noir" # Si non mettre la couleur noire.
                res = start2(color) # Appeler la fonction de commencement de jeu. // Call up the game start function.
                return res
                break # Sortir de la fonction. // Exit function.
            elif recognizedWord == "english" or recognizedWord == "anglais": # Si l'utilisateur choisit anglais, // If the user says English,
                tts.setLanguage('English') # Mettre la langue en anglais. // Set the language to English. 
                globalVar.TexteARepete = "Hello! I'm speak english"
                tts.say("Hello! I'm speak english")  # Nao dit. // Nao says.
                globalVar.language = "anglais" # Mettre le lagage en anglais. // Put Englich language.
                if(color == True): 
                    color = "White" # alors mettre la couleur white.
                else :
                    color = "Black" # Si non mettre la couleur black.
                res = start2(color) # Appeler la fonction de commencement de jeu. // Call up the game start function.
                return res
                break # Sortir de la fonction. // Exit function.
        tts.setLanguage('English') # Mettre la langue en anglais. // Set the language to English. 
        globalVar.TexteARepete = "Sorry, I didn't understand. In which language? French or English"
        tts.say("Sorry, I didn't understand. In which language? French or English") # Nao dit. // Nao says.
        tts.setLanguage('French') # Mettre la langue en francais. // Set the language to Frenchf. 
        globalVar.TexteARepete = "Daizoler, je nai pas compris. En quelle langue? franssais ou anglais"
        tts.say("Daizoler, je nai pas compris. En quelle langue? franssais ou anglais")  # Nao dit. // Nao says.
        asr.subscribe("Test_ASR")  # Ecouter encore. // Listen again.
        
def disrupt():
    """
    Fonction pour distraire l'adversaire. // Function to distract the opponent.
    """
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        disruptF() # Appeler la fonction en francais. // Call the function in French.
    else :
        disruptA() # Si non appeler la version anglaise. // If not, call the English version.

def start2(color):
    """
    Fonction pour commencer le jeu. // Function to start the game.

    Arguments :
    color -- couleur // color.
    """
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        res = start2F(color) # Appeler la fonction en francais. // Call the function in French.
    else :
        res = start2A(color) # Si non appeler la version anglaise. // If not, call the English version.
    return res
def checkmate():
    """
    Fonction pour echec et mat. // Function to checkmat. 

    """
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        checkmateF() # Appeler la fonction en francais. // Call the function in French.
    else :
        checkmateA() # Si non appeler la version anglaise. // If not, call the English version.

def cheating():
    """
    Fonction pour quand l'adversaire triche. // Function for when the opponent cheats. 

    """
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        cheatingF() # Appeler la fonction en francais. // Call the function in French.
    else :
        cheatingA() # Si non appeler la version anglaise. // If not, call the English version.

def check():
    """
    Fonction pour echec. // Function to echec.

    """
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        checkF() # Appeler la fonction en francais. // Call the function in French.
    else :
        checkA() # Si non appeler la version anglaise. // If not, call the English version.

def sayCase(deplacement):
    """
    Fonction pour dire les deplacements. // Function for expressing movements.

    Argument :
    deplacement -- Deplacement du pion. // Deplacement of the pawn.

    """
    print globalVar.language
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        sayCaseF(deplacement) # Appeler la fonction en francais. // Call the function in French.
    else :
        sayCaseA(deplacement) # Si non appeler la version anglaise. // If not, call the English version.

def pawnEaten(namePawn):
    """
    Fonction pour manger un pion. // # Call the echec function in French.

    Argument :
    namePawn -- Nom du pion. // Name of the pawn.

    """
    if '/' not in namePawn: # Si le parametre n'a pas un /,
        return # Arreter la fonction.
        print("ERREUR : Aucun / dans le parametre.") # Indiquer dans la console pour le suivis.
    parts = namePawn.split('/') # Separate the parameter with /.
    if len(parts) != 2: # Si le parametre n'est pas diviser en deux.
        return # Arreter la fonction.
        print("ERREUR : Le parametre n est pas diviser en deux.") # Indiquer dans la console pour le suivis.

    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        namePawn = parts[1].strip()
        pawnEatenF(namePawn) # Appeler la fonction en francais. // Call the function in French.
    else :
        namePawn = parts[0].strip()
        pawnEatenA(namePawn) # Si non appeler la version anglaise. // If not, call the English version.
 
def eatPawn(namePawn):
    """
    Fonction pour quand Nao mange un pion. // Function for when Nao eats a pawn. 

    Argument :
    namePawn -- Nom du pion. // Name of the pawn.

    """
    if '/' not in namePawn: # Si le parametre n'a pas un /,
        return # Arreter la fonction.
        print("ERREUR : Aucun / dans le parametre.") # Indiquer dans la console pour le suivis.
    parts = namePawn.split('/') # Separate the parameter with /.
    if len(parts) != 2: # Si le parametre n'est pas diviser en deux.
        return # Arreter la fonction.
        print("ERREUR : Le parametre n est pas diviser en deux.") # Indiquer dans la console pour le suivis.
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        namePawn = parts[1].strip()
        eatPawnF(namePawn) # Appeler la fonction en francais. // Call the function in French.
    else :
        namePawn = parts[0].strip()
        eatPawnA(namePawn) # Si non appeler la version anglaise. // If not, call the English version.

def choicePawnAtEnd(namePawn):
    """
    Fonction pour dire le pion que Nao choisit. // Function to say which pawn Nao chooses.

    Argument :
    namePawn -- Nom du pion. // Name of the pawn.

    """
    if '/' not in namePawn: # Si le parametre n'a pas un /,
        return # Arreter la fonction.
        print("ERREUR : Aucun / dans le parametre.") # Indiquer dans la console pour le suivis.
    parts = namePawn.split('/') # Separate the parameter with /.
    if len(parts) != 2: # Si le parametre n'est pas diviser en deux.
        return # Arreter la fonction.
        print("ERREUR : Le parametre n est pas diviser en deux.") # Indiquer dans la console pour le suivis.
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        namePawn = parts[1].strip()
        choicePawnAtEndF(namePawn) # Appeler la fonction en francais. // Call the function in French.
    else :
        namePawn = parts[0].strip()
        choicePawnAtEndA(namePawn) # Si non appeler la version anglaise. // If not, call the English version.

def winning():
    """
    Fonction pour quand Nao est entrain de gagner. // Function for when Nao is winning. 

    """
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        winningF() # Appeler la fonction en francais. // Call the function in French.
    else :
        winningA() # Si non appeler la version anglaise. // If not, call the English version.

def sayCheck():
    """
    Fonction pour dire echec. // Function to indicate failure. 

    """
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        sayCheckF() # Appeler la fonction en francais. // Call the function in French.
    else :
        sayCheckA() # Si non appeler la version anglaise. // If not, call the English version.

def win():
    """
    Fonction pour quand Nao a gagne. // Function when Nao won. 

    """
    if globalVar.language == "francais" : # Si la langue est francais, // If language is French,
        winF() # Appeler la fonction en francais. // Call the function in French.
    else :
        winA() # Si non appeler la version anglaise. // If not, call the English version.


def repeter():
    """
    Fonction pour faire repeter Nao. // Function to make Nao repeat.

    """
    tts.say(globalVar.TexteARepete) # Nao dit // Nao says


def nomPion(a):
    if a == "K" or a == "k":
        return "King/Roi"
    elif a == "Q" or a == "q":
        return "Queen/Reine"
    elif a == "R" or a == "r":
        return "Rook/Tourreu"
    elif a == "B" or a == "b":
        return "Bishop/Fou"
    elif a == "N" or a == "n":
        return "Knight/Cavalier"
    elif a == "P" or a == "p":
        return "Pawn/Pion"
    else:
        return " / "

