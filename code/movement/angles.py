import math
from naoqi import ALProxy
import math
import time
import math
import threading

ip = "172.16.1.164" # Definir les adresse IP. // Define IP adress.
port = 9559 # Definir les ports. // Define port. 

# Definit les modules. // Define modules.
motion = ALProxy("ALMotion", ip, port)
asr = ALProxy("ALSpeechRecognition", ip, port)
tts = ALProxy("ALTextToSpeech", ip, port)
posture_proxy = ALProxy("ALRobotPosture", ip, port)
aal_proxy = ALProxy("ALAutonomousLife", ip, port)
memory = ALProxy("ALMemory", ip, port)

# Definir les angles correspondant aux mouvements. // Define the angles corresponding to the movements.
les_angles = {
    "cases" : [
        "h1", "g1", "f1", "e1", "d1", "c1", "b1", "a1",
        "h2", "g2", "f2", "e2", "d2", "c2", "b2", "a2",
        "h3", "g3", "f3", "e3", "d3", "c3", "b3", "a3",
        "h4", "g4", "f4", "e4", "d4", "c4", "b4", "a4",
        "h5", "g5", "f5", "e5", "d5", "c5", "b5", "a5",
        "h6", "g6", "f6", "e6", "d6", "c6", "b6", "a6",
        "h7", "g7", "f7", "e7", "d7", "c7", "b7", "a7",
        "h8", "g8", "f8", "e8", "d8", "c8", "b8", "a8",
    ], # Liste des cases de l'echiquier. // List of chessboard squares. 
    "valeurs" : [
        # Colonne 8. // Columns 8.
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(-8)], # A8
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(5)], # B8
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(-10)], # C8 
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(-18)], # D8
        [math.radians(0), math.radians(-80), math.radians(-42), math.radians(18)], # E8
        [math.radians(0), math.radians(-80), math.radians(-42), math.radians(10)], # F8
        [math.radians(0), math.radians(-80), math.radians(-42), math.radians(11)], # G8
        [math.radians(0), math.radians(-80), math.radians(-42)], # H8
        # Colonne 7. // Columns 7.
        [math.radians(0), math.radians(80), math.radians(-42)], # A7
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(5)], # B7
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(-10)], # C7
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(-18)], # D7 
        [math.radians(0), math.radians(-80), math.radians(-42), math.radians(18)], # E7
        [math.radians(0), math.radians(-80), math.radians(-42), math.radians(10)], # F7
        [math.radians(0), math.radians(-80), math.radians(-42), math.radians(11)], # G7
        [math.radians(0), math.radians(-80), math.radians(-42)], # H7
        # Colonne 6. // Columns 6.
        [math.radians(0), math.radians(80), math.radians(-42)], # A6
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(5)], # B6
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(-10)], # C6
        [math.radians(0), math.radians(80), math.radians(-42), math.radians(-18)], # D6
        [math.radians(0), math.radians(-80), math.radians(-42), math.radians(18)], # E6
        [math.radians(0), math.radians(-80), math.radians(-42), math.radians(10)], # F6
        [math.radians(0), math.radians(-80), math.radians(-42), math.radians(11)], # G6
        [math.radians(0), math.radians(-80), math.radians(-42)], # H6
        # Colonne 5. // Columns 5.
        [math.radians(10), math.radians(80), math.radians(-38)], # A5
        [math.radians(10), math.radians(80), math.radians(-38), math.radians(5)], # B5
        [math.radians(10), math.radians(80), math.radians(-40), math.radians(-10)], # C5
        [math.radians(10), math.radians(80), math.radians(-38), math.radians(-18)], # D5
        [math.radians(10), math.radians(-80), math.radians(-38), math.radians(18)], # E5
        [math.radians(10), math.radians(-80), math.radians(-38), math.radians(10)], # F5
        [math.radians(10), math.radians(-80), math.radians(-38), math.radians(11)], # G5
        [math.radians(10), math.radians(-80), math.radians(-38)], # H5
        # Colonne 4. // Columns 4.
        [math.radians(20), math.radians(80), math.radians(-38)], # A4
        [math.radians(20), math.radians(80), math.radians(-38), math.radians(5)], # B4
        [math.radians(20), math.radians(80), math.radians(-38), math.radians(-10)], # C4
        [math.radians(20), math.radians(80), math.radians(-38), math.radians(-18)], # D4
        [math.radians(20), math.radians(-80), math.radians(-38), math.radians(28)], # E4
        [math.radians(20), math.radians(-80), math.radians(-38), math.radians(10)], # F4
        [math.radians(20), math.radians(-80), math.radians(-38), math.radians(11)], # G4
        [math.radians(20), math.radians(-80), math.radians(-38)], # H4
        # Colonne 3. // Columns 3.
        [math.radians(25), math.radians(80), math.radians(-30)], # A3
        [math.radians(25), math.radians(80), math.radians(-30), math.radians(5)], # B3
        [math.radians(25), math.radians(80), math.radians(-30), math.radians(-10)], # C3
        [math.radians(25), math.radians(80), math.radians(-30), math.radians(-18)], # D3
        [math.radians(25), math.radians(-80), math.radians(-30), math.radians(18)], # E3
        [math.radians(25), math.radians(-80), math.radians(-30), math.radians(10)], # F3
        [math.radians(25), math.radians(-80), math.radians(-30), math.radians(11)], # G3
        [math.radians(25), math.radians(-80), math.radians(-30)], # H3
        # Colonne 2. // Columns 2.
        [math.radians(30), math.radians(80), math.radians(-15)], # A2
        [math.radians(30), math.radians(80), math.radians(-15), math.radians(5)], # B2
        [math.radians(30), math.radians(80), math.radians(-15), math.radians(-10)], # C2
        [math.radians(30), math.radians(80), math.radians(-15), math.radians(-18)], # D2
        [math.radians(30), math.radians(-80), math.radians(-15), math.radians(18)], # E2
        [math.radians(30), math.radians(-80), math.radians(-15), math.radians(10)], # F2
        [math.radians(30), math.radians(-80), math.radians(-15), math.radians(11)], # G2
        [math.radians(30), math.radians(-80), math.radians(-15)], # H2
        # Colonne 1. // Columns 1.
        [math.radians(40), math.radians(80), math.radians(-15)], # A1
        [math.radians(40), math.radians(80), math.radians(-15), math.radians(5)], # B1
        [math.radians(40), math.radians(80), math.radians(-15), math.radians(-10)], # C1
        [math.radians(40), math.radians(80), math.radians(-15), math.radians(-18)], # D1
        [math.radians(40), math.radians(-80), math.radians(-15), math.radians(18)], # E1
        [math.radians(40), math.radians(-80), math.radians(-15), math.radians(10)], # F1
        [math.radians(40), math.radians(-80), math.radians(-15), math.radians(11)], # G1
        [math.radians(40), math.radians(-80), math.radians(-15), math.radians(-5)], # H1
    ], # Liste des colonnes. // List of columns.
    "mouvements" : [
        # Ligne 8. // Line 8.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch"], # Colonne A. // Columns A.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne B. // Column B.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne C. // Column C.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne D. // Column D.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne E. // Column E.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne F. // Column F.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne G. // Column G.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne H. // Column H.
        # Ligne 7. // Line 7.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch"], # Colonne A. // Columns A.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne B. // Column B.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne C. // Column C.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne D. // Column D.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne E. // Column E.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne F. // Column F.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne G. // Column G.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne H. // Column H.
        # Ligne 6. // Line 6.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch"], # Colonne A. // Columns A.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne B. // Column B.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne C. // Column C.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne D. // Column D.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne E. // Column E.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne F. // Column F.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne G. // Column G.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne H. // Column H.
        # Ligne 5. // Line 5.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch"], # Colonne A. // Columns A.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne B. // Column B.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne C. // Column C.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne D. // Column D.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne E. // Column E.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne F. // Column F.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne G. // Column G.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne H. // Column H.
        # Ligne 4. // Line 4.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch"], # Colonne A. // Columns A.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne B. // Column B.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne C. // Column C.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne D. // Column D.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne E. // Column E.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne F. // Column F.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne G. // Column G.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne H. // Column H.
        # Ligne 3. // Line 3.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch"], # Colonne A. // Columns A.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne B. // Column B.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne C. // Column C.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne D. // Column D.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne E. // Column E.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne F. // Column F.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne G. // Column G.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne H. // Column H.
        # Ligne 2. // Line 2.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch"], # Colonne A. // Columns A.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne B. // Column B.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne C. // Column C.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne D. // Column D.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne E. // Column E.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne F. // Column F.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne G. // Column G.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne H. // Column H.
        # Ligne 1. // Line 1.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch"], # Colonne A. // Columns A.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne B. // Column B.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne C. // Column C.
        ["LShoulderPitch", "LWristYaw", "LHipYawPitch", "LShoulderRoll"], # Colonne D. // Column D.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne E. // Column E.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne F. // Column F.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne G. // Column G.
        ["RShoulderPitch", "RWristYaw", "LHipYawPitch", "RShoulderRoll"], # Colonne H. // Column H.
    ] # Liste des membres de Nao selon la ligne.  // List of Nao members by line. 
}

