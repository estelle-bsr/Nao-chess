from naoqi import ALProxy
import math
import time
import math
import threading
from angles import les_angles
from globalVar import *


# Definit les modules. // Define modules.
motion = ALProxy("ALMotion", ip, port)
asr = ALProxy("ALSpeechRecognition", ip, port)
tts = ALProxy("ALTextToSpeech", ip, port)
posture_proxy = ALProxy("ALRobotPosture", ip, port)
aal_proxy = ALProxy("ALAutonomousLife", ip, port)
memory = ALProxy("ALMemory", ip, port)

posture_proxy.goToPosture("Stand", 0.5)
aal_proxy.setState("safeguard")


def initialiser_position():
    """
    Initialiser la position de Nao. // Initialise Nao's position.
    """
    motion.angleInterpolationWithSpeed("LHipYawPitch",math.radians(-5), 0.1) # Mettre le buste droit. // Stand up straight.
    # Mettre les bras droit. // Straighten your arms.
    motion.angleInterpolationWithSpeed("RShoulderRoll", math.radians(-12), 0.1)
    motion.angleInterpolationWithSpeed("RWristYaw", math.radians(9), 0.1)
    motion.angleInterpolationWithSpeed("LShoulderRoll", math.radians(12), 0.1)
    motion.angleInterpolationWithSpeed("LWristYaw", math.radians(-9), 0.1)
    motion.angleInterpolationWithSpeed("RShoulderPitch", math.radians(85), 0.1)
    motion.angleInterpolationWithSpeed("LShoulderPitch", math.radians(85), 0.1)


def position_dans_alphabet(lettre):
    """
    Fonction pour trouver la position d'une lettre dans l'alphabet. // Function for finding the position of a letter in the alphabet.

    Argument :
    lettre -- La lettre a rechercher. // The letter to look for.

    Retourne :
    La position de la lettre.
    """
    lettre = lettre.upper() # Convertir la lettre en majuscule pour normaliser. // Convert the letter to uppercase to standardise.
    if 'A' <= lettre <= 'Z': # Si c'est une lettre dans l'alphabet. // If it's a letter in the alphabet.
        return ord(lettre) - ord('A') + 1 # Retourner la position. // Reverse the position.
    else:
        return None  # Si non, retourner rien.  // If not, return nothing. 

def pointer_zone_case_brut(case):
    """
    Fonction qui fait pointer une case a Nao.  // Function that makes Nao point to a square. 

    Argument : 
    case -- La case visee. // The target box.

    """
    angles = les_angles["valeurs"][les_angles["cases"].index(case)] # Recuperer dans le fichier dans angles les coordonnees de la case. // Recover the coordinates of the box from the file in angles.
    mouvements = les_angles["mouvements"][les_angles["cases"].index(case)] # Recuperer dans le fichier dans angles le mouvement de la case. // Recover the movement of the square in the angles file.
    motion.angleInterpolationWithSpeed(mouvements, angles, 0.1) # Do it.

def get_angle_en_fonction_case(formule):
    print formule
    """
    Fonction pour faire pointer a Nao une case de depart et d'arrivee. // Function to make Nao point to a departure and arrival square.
    """
    if len(formule) == 4: # Si il y quatre caractere dans formule, // If there are four characters in the formula,
        case_depart = formule[:2] # Mettre les deux premiers caractere dans la case de depart. // Put the first two characters in the start box.
        case_arrivee = formule[2:] # Mettre les deux dernier caractere dans la case d'arrivee. // Put the last two characters in the arrival box.
        print("Nao point la case de depart.") # Suivis dans la console. // Follow-ups in the console.
        pointer_zone_case_brut(case_depart) # Nao pointe la case de depart. // Nao points to the starting square.
        initialiser_position() # Initialiser la position de Nao. // Initialise Nao's position.
        print("Nao point la case d'arrivee.") # Suivis dans la console. // Follow-ups in the console.
        pointer_zone_case_brut(case_arrivee) # Nao pointe la case d'arrivee. // Nao points to the arrival square.
        time.sleep(3) # Attrendre trois secondes. // Wait three secondes.
        initialiser_position()  # Initialiser la position de Nao. // Initialise Nao's position.
    else : 
        print("Le parametre formule n'a pas quatre caractere.") # Suivis dans la console. // Follow-ups in the console.