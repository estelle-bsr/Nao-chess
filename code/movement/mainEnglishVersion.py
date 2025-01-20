from naoqi import ALProxy
from random import *
import time
import os
import math
import threading
from movement import *
import globalVar 


# Define modules.
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
    Function to get Nao up.
    """
    posture.goToPosture("Stand", 1.0) # Nao gets up.

def sit():
    """
    Function for Nao to sit down.
    """
    posture.goToPosture("Sit", 1.0) # Nao sits down.

def resetLeds():
    """
    Function to set the LEDs to white.
    """
    print("Start function: resetLeds.") # Indicate in the console for follow-up.
    leds.fadeRGB("FaceLeds", 1.0, 1.0, 1.0, 0) # Put on white eyes.
    leds.fadeRGB("ChestLeds", 1.0, 1.0, 1.0, 0) # Put on the white logo.
    leds.fadeRGB("FeetLeds", 1.0, 1.0, 1.0, 0) # Put feets in white.
    print("End function: resetLeds.") # Indicate in the console for follow-up.

def cheatingA ():
    """
    Function of Nao's reaction when his opponent cheats.
    """
    print("Start function: cheatingA.") # Indicate in the console for follow-up.
    leds.fadeRGB("FaceLeds", 1.0, 0.0, 0.0, 0) # Put on red eyes.
    leds.fadeRGB("ChestLeds", 1.0, 0.0, 0.0, 0) # Put on the white red.
    leds.fadeRGB("FeetLeds", 1.0, 0.0, 0.0, 0) # Put feets in red.
    print("Nao speaks.") # Indicate follow-up in the console.
    globalVar.TexteARepete = "You cheated!"
    tts.say("You cheated!") # Nao indicates cheating.
    print("Nao finish speak.") # Indicate follow-up in the console.
    time.sleep(2) # Wait two seconds.
    resetLeds() # Reset the LEDs.
    print("End function: cheatingA.") # Indicate in the console for follow-up.

def shakeHands():
    """
    Shake hands function.
    """
    print("Start function : shakeHands.") # Indicate in the console for follow-up.
    globalVar.TexteARepete = "Are you left- or right-handed?"
    tts.say("Are you left- or right-handed?") # Nao says.
    asr.pause(True) # Activate voice recognition.
    asr.setVocabulary(["left-handed", "right-handed", "left", "right"], False) # Putting words to recognise.
    asr.setLanguage("English")  # Put on the English language.
    asr.pause(False) # Stop voice recognition.
    asr.subscribe("Test_ASR")
    while True:
        time.sleep(3) # Wait three seconds. 
        result = memory.getData("WordRecognized") # Recover the opponent's response. 
        asr.unsubscribe("Test_ASR") # Function call to shake right hand.
        reponse = result[0].lower() # Recover the answer.
        print("Nao's answer to the question left- or right-handed : " + reponse) # Display monitoring in the console.
        if reponse == "left" or reponse == "left-handed": # If the answer is right-handed,
            globalVar.TexteARepete = "You're left-handed. , So let's shake hands."
            tts.say("You're left-handed.") # Nao says.
            tts.say("So let's shake hands.") # Nao says.
            shakeHandsRight() # Function call to shake right hand.
            break # Exit the function.
        elif reponse == "right" or reponse == "right-handed":  # If the answer is left-handed,
            globalVar.TexteARepete = "You're right-handed. , So let's shake hands."
            tts.say("You're right-handed.") # Nao says.
            tts.say("So let's shake hands.") # Nao says.
            shakeHandsLeft() # Function call to shake left hand.
            break # Exit the function.
        globalVar.TexteARepete = "I didn't understand can you repeat that"
        tts.say("I didn't understand can you repeat that") # Nao says.
        asr.subscribe("Test_ASR")
    print("End function : shakeHands.") # Indicate in the console for follow-up.

def shakeHandsLeft():
    """
    Shake the right hand when the opponent says left.
    """
    joints_names = [ 
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" 
    ] # Define the joints.
    target_angles = [
        math.radians(0), # RShoulderPitch
        math.radians(-18.2), # RShoulderRoll
        math.radians(13.3), # RElbowYaw
        math.radians(0), # RElbowRoll 
        math.radians(0), # RWristYaw
        0.02, # RHand
    ] # Define angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Make the move.
    thread_ouvrir_main = threading.Thread(target=hand, args=("ouvrir", "RHand")) # Create a thread to open the hand.
    thread_ouvrir_main.start() # Start the thread.
    time.sleep(2) # Wait two seconds.
    thread_fermer_main = threading.Thread(target=hand, args=("fermer", "RHand")) # Create a thread to close the hand.
    thread_fermer_main.start() # Start the thread.
    # Wait for threads to finish.
    thread_ouvrir_main.join()
    thread_fermer_main.join()
    for i in range (3): # Repeat three times,
        raiseRightHand() # Raise the arm.
        lowerRightHand() # Lower the arm.
    hand("ouvrir","RHand") # Open right hand.
    time.sleep(2) # Wait two seconds.
    hand("fermer","RHand") # Close right hand.

def shakeHandsRight():
    """
    Function to shake with the left hand when the opponent has said right.
    """
    joints_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"  
    ] # Define the left arm joints.
    target_angles = [
        math.radians(0), # LShoulderPitch
        math.radians(18.2), # LShoulderRoll 
        math.radians(-13.3), # LElbowYaw 
        math.radians(0), # LElbowRoll
        math.radians(-104.5), # LWristYaw
        0.02, # LHand 

    ] # Define angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Make the move.
    thread_ouvrir_main = threading.Thread(target=hand, args=("ouvrir", "LHand")) # Create the thread to open the hand.
    thread_ouvrir_main.start() # Start thread.
    time.sleep(2) # Wait 2 seconds.
    thread_fermer_main = threading.Thread(target=hand, args=("fermer", "LHand")) # Create a thread to close the hand.
    thread_fermer_main.start() # Demarer le thread.
    # Wait for threads to finish.
    thread_ouvrir_main.join()
    thread_fermer_main.join()
    for i in range (3): # Repeat three times,
        raiseLeftHand() # Raise your arm.
        lowerLeftHand() # Lower your arm.
    hand("ouvrir","LHand") #  Open your hand.
    time.sleep(2) # Wait two seconds.
    hand("fermer","LHand") # Close the hand.  

def lowerRightHand():
    """
    Lower the right arm.
    """
    joints_names = [ 
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" 
    ] # Define the joints.
    target_angles = [
        math.radians(30), # RShoulderPitch
        math.radians(-18.2), # RShoulderRoll
        math.radians(13.3), # RElbowYaw
        math.radians(0), # RElbowRoll 
        math.radians(0), # RWristYaw
        0.02, # RHand
    ] # Define angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Make the move.


def raiseLeftHand():
    """
    Function for raising the left arm. 
    """
    joints_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"  
    ] # Defining joints.
    target_angles = [
        math.radians(30), # LShoulderPitch
        math.radians(18.2), # LShoulderRoll 
        math.radians(-13.3), # LElbowYaw 
        math.radians(0), # LElbowRoll
        math.radians(-104.5), # LWristYaw
        0.02, # LHand 
    ] # Define angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Make the move.

def raiseRightHand():
    """
    Raise the right arm.
    """
    joints_names = [ 
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" 
    ] # Define the joints.
    target_angles = [
        math.radians(-30), # RShoulderPitch
        math.radians(-18.2), # RShoulderRoll
        math.radians(13.3), # RElbowYaw
        math.radians(0), # RElbowRoll 
        math.radians(0), # RWristYaw
        0.02, # RHand
    ] # Define angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Make the move.
    
def lowerLeftHand():
    """
    Lower left arm.
    """
    joints_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"  
    ] # Defining joints.
    target_angles = [
        math.radians(-30), # LShoulderPitch
        math.radians(18.2), # LShoulderRoll 
        math.radians(-13.3), # LElbowYaw 
        math.radians(0), # LElbowRoll
        math.radians(-104.5), # LWristYaw
        0.02, # LHand 
    ] # Define angles.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Make the move.

def hand(action, main_concernee):
    """
    Open or close the chosen hand.

    Arguments:
    action -- The action of the hand open or close.
    main_concernee -- The concerned hand (right or left).

    """
    if action == "ouvrir": # If the action is open,
        if main_concernee == "RHand": # If the hand is the right hand,
            motion.openHand("RHand") # Open the right hand.
            print("Nao opens his right hand.") # Follow-ups in the console.
        elif main_concernee == "LHand": # If the hand is the left hand,
            motion.openHand("LHand") # Open the left hand.
            print("Nao opens his left hand.") # Follow-ups in the console.
        else:
            print("ERROR: Instruction not understood.") # Follow-ups in the console.
    elif action == "fermer": # If the action is close,
        if main_concernee == "RHand": # If the hand is the right hand,
            motion.closeHand("RHand")  # Close the right hand.
            print("Nao closes his right hand.") # Follow-ups in the console.
        elif main_concernee == "LHand": # Si la main est la main gauche.
            motion.closeHand("LHand")  # Close the left hand.
            print("Nao closes his left hand.") # Follow-ups in the console.
        else:
            print("ERROR: Instruction not understood.") # Follow-ups in the console.
    else:
        print("ERROR: Instruction not understood.") # Follow-ups in the console.


def start2A(color):
    """
    Function to start the game.

    Arguments:
    color -- Color of pawns played by Nao. 

    """
    print("Start function: start2A.") # Indicate in the console for follow-up.
    globalVar.TexteARepete ="Are you ready to play?"
    tts.say("Are you ready to play?")  # Nao asks the player if he is ready to play.
    asr.pause(True) # Waiting for detection.
    asr.setVocabulary(["yes", "no"], False)  # Put in the recognised words.
    asr.setLanguage("English")  # Set the language to English. 
    asr.pause(False) # End of analysis.
    asr.subscribe("Test_ASR")
    while True:
        time.sleep(3) # Wait three seconds.
        answer = memory.getData("WordRecognized")  # Recover words recognised by Nao.
        asr.unsubscribe("Test_ASR")
        if answer and len(answer) > 0: # If the response is valid,
            print("Nao understood in reply to Are you ready to play? :", answer[0].lower()) # Indicate follow-up in the console. 
            recognized_word = answer[0].lower() # convert the word to minscule.
            if recognized_word == "yes": # If the user says yes,
                print("Nao understood, yes.") # Indicate follow-up in the console. 
                globalVar.TexteARepete = "Okay, I'll play the pawns " + color + ". I can't move the pieces by myself, so I'll need you to move the pieces when I ask you, please. As you can see, you have an application that simulates a classic chess game timer. This timer shows the total time remaining for each player to play the entire game. You will also find several buttons: by clicking on your opponent's timer, you stop your turn and start your opponent's turn. Before the game begins, and permanently, you can select an option to add 30 seconds to your total time for each new turn. There is also a 'repeat' button that allows me to repeat what I said if you didn't understand it. If you don't want to use the app, you can tap the front of my head to indicate that your turn is over and start your opponent's turn. You can tap the back of my head to make me repeat what I said. But first, what level of play do you want to do? Give me a number between 1 and 4 in English."
                tts.say("Okay, I'll play the pawns " + color + ". I can't move the pieces by myself, so I'll need you to move the pieces when I ask you, please.")  # Nao says.
                tts.say("As you can see, you have an application that simulates a classic chess game timer. This timer shows the total time remaining for each player to play the entire game. You will also find several buttons: by clicking on your opponent's timer, you stop your turn and start your opponent's turn. Before the game begins, and permanently, you can select an option to add 30 seconds to your total time for each new turn. There is also a 'repeat' button that allows me to repeat what I said if you didn't understand it. If you don't want to use the app, you can tap the front of my head to indicate that your turn is over and start your opponent's turn. You can tap the back of my head to make me repeat what I said.") # Nao says.
                tts.say("But first, what level of play do you want to do? Give me a number between 1 and 4 in English.")  # Nao says.
                asr.pause(True) # Awaiting detection.
                asr.setVocabulary(["one", "two", "three", "four"], False) # Set words to recognize.
                asr.setLanguage("English") # Set language to English.
                asr.pause(False) # End of analysis.
                asr.subscribe("Test_ASR")
                time.sleep(3) # Wait three seconds.
                answerLevel = memory.getData("WordRecognized")
                resultat = choiceLevel(answerLevel)  # Send the game level back to AI
                time.sleep(5) # Wait.
                return resultat
                break
            elif recognized_word == "no": # If user says no,
                print("Nao understood, no.") # Indicate follow-up in the console. 
                globalVar.TexteARepete = "I understand, I'm a formidable player!"
                tts.say("I understand, I'm a formidable player!")  # Nao says.
                return resultat
                break
        print("Nao don't understand.") # Indicate follow-up in the console. 
        globalVar.TexteARepete = "Sorry, I didn't understand. Are you ready to play chess? Please say yes or no."
        tts.say("Sorry, I didn't understand. Are you ready to play chess? Please say yes or no.")  # Nao says.
        asr.subscribe("Test_ASR")  # Listen again
        print("End function: start2A.") # Indicate in the console for follow-up.
        

def choiceLevel(level):
    """
    Function to send the level of play chosen by the opponent to the brain/IA.

    Argument:
    level -- The level chosen by the opponent.

    """
    print("Start function: choiceLevel.") # Indicate in the console for follow-up.
    step =0
    if level and len(level) > 0: # If the opponent chooses a level,
        word = level[0].lower() # take the first element of the list,
        print(word)
        if word == "one": # If the user answers level 1,
            print("The choice level function is in if 1.") # Indicate in the console for follow-up.
            globalVar.TexteARepete ="Okay, you've chosen level one."
            tts.say("Okay, you've chosen level one.") # Nao says.
            step = 1 # Put step to 1.
        elif word == "two": # If the user answers level 2,
            print("The choice level function is in if 2.") # Indicate in the console for follow-up.
            globalVar.TexteARepete = "Okay, you've chosen level two."
            tts.say("Okay, you've chosen level two.") # Nao says.
            step = 2 # Put step to 2.
        elif word == "three": # If the user answers level 3,
            print("The choice level function is in if 3.") # Indicate in the console for follow-up.
            globalVar.TexteARepete = "Okay, you've chosen level three."
            tts.say("Okay, you've chosen level three.") # Nao says.
            step = 3 # Put step to 3.
        elif word == "four": # If the user answers level 4,
            print("The choice level function is in if 4.") # Indicate in the console for follow-up.
            globalVar.TexteARepete = "Okay, you've chosen level four."
            tts.say("Okay, you've chosen level four.") # Nao says.
            step = 4 # Put step to 4.
        else :
            print("Nao didn't understand.") # Indicate in the console for follow-up.
            globalVar.TexteARepete = "Sorry I didn't understand the level you said. Can you tell me the level you chose between 1 and 4 please? Remember to say the number."
            tts.say("Sorry I didn't understand the level you said. Can you tell me the level you chose between 1 and 4 please? Remember to say the number.") # Nao says.
            asr.pause(True) # Activate voice recognition.
            asr.setVocabulary(["one", "two", "three", "four"], False) # Set words to recognize.
            asr.setLanguage("English") # Set language to English.
            asr.pause(False) # Stop speech recognition.
            asr.subscribe("Test_ASR")
            time.sleep(5) # Wait.
            answerLevel = memory.getData("WordRecognized") # Having the word pronounces the opponent.
            choiceLevel(answerLevel) # Relaunch the function.
            return 0 # Exit function.
    shakeHands() # Call shake hands.
    return step # Send the level.
    print("End function: choiceLevel.") # Indicate in the console for follow-up.

def armsUp():
    """
    Function for the position of Nao's arms when he cries.
    """
    print("Start function: armsUp.") # Indicate in the console for follow-up.
    joints_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", 
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" 
    ] # Define arm angles.
    target_angles = [
        # Left arm.
        math.radians(-31.9), # LShoulderPitch
        math.radians(18.2), # LShoulderRoll 
        math.radians(-13.3), # LElbowYaw 
        math.radians(-88.5), # LElbowRoll
        math.radians(-104.5), # LWristYaw
        0.02, # LHand 

        # Right arm.
        math.radians(-31.9), # RShoulderPitch
        math.radians(-18.2), # RShoulderRoll
        math.radians(13.3), # RElbowYaw
        math.radians(88.5), # RElbowRoll 
        math.radians(104.5), # RWristYaw
        0.02, # RHand
    ] # Apply angles to joints.
    print("Nao raises her hands to cry") # Indicate in the console for follow-up.
    motion.angleInterpolation(joints_names, target_angles, [1.5]*len(joints_names), True) # Make the move.
    endTime = time.time() + 2  # Wait two seconds.
    while time.time() < endTime: # As long as the elapsed time is less than two seconds,
        motion.setAngles(joints_names, target_angles, 0.1)  # maintain position.
        time.sleep(0.1)  # Wait.
    print("Nao finishes the movement of raising her hands to cry") # Indicate in the console for follow-up.
    print("End function: armsUp.") # Indicate in the console for follow-up.

def songCheckmate(): 
    """
    Function to play the sound when Nao loses.
    """
    print("Start function: songCheckmate.") # Indicate in the console for follow-up.
    audio = "/home/nao/Niels/checkmat_reaction.mp3" # Sound path.
    audioPlayer.playFile(audio)  # Play audio
    print("Lancer son.") # Indicate in the console for follow-up.
    print("End function: songCheckmate.") # Indicate in the console for follow-up.

def checkmateA():
    """
    Function when Nao loses a game.
    """
    print("Start function: checkmateA.") # Indicate in the console for follow-up.
    sit()  # Nao sits down.
    print("Change of LED colours.") # Indicate in the console for follow-up.
    leds.fadeRGB("FaceLeds", 0x0000FF, 1.0)  # Put on blue eyes.
    leds.fadeRGB("ChestLeds", 0x0000FF, 0) # Put on the blue logo.
    leds.fadeRGB("FeetLeds", 0x0000FF, 0) # Put feets in blue.
    threadArms = threading.Thread(target=armsUp) # Create a thread for arm movement.
    threadSong = threading.Thread(target=songCheckmate) # Create a thread for the sound.
    print("Thread execution.") # Indicate in the console for follow-up.
    # Thread execution.
    threadArms.start()
    threadSong.start()
    # Wait for threads to finish.
    threadArms.join()
    threadSong.join()
    print("End of thread execution.") # Indicate in the console for follow-up.
    print("LED and volume reset in progress.") # Indicate in the console for follow-up.
    resetLeds() # Reset the LEDs.
    audioDevice.setOutputVolume(100)  # Reset the volume.
    print("LED and volume reset done.") # Indicate in the console for follow-up.
    print("End of function: checkmateF") # Indicate in the console for follow-up.

def checkA():
    """
    Function when Nao fails.
    """
    print("Start of function: checkA") # Indicate in the console for follow-up.
    print("Change of LED colours.") # Indicate in the console for follow-up.
    leds.fadeRGB("FaceLeds", 0x0000FF, 1.0) # Put on blue eyes.
    leds.fadeRGB("ChestLeds", 0x0000FF, 0) # Put on the blue logo.
    leds.fadeRGB("FeetLeds", 0x0000FF, 0) # Put feets in blue.
    print("Sound launch.") # Indicate in the console for follow-up.
    audio = "/home/nao/Niels/check_reaction.mp3"  # Sound path.
    audioDevice.setOutputVolume(50)  # Set the sound volume to 50.
    audioPlayer.playFile(audio)  # Play the sound.
    print("LED and volume reset in progress.") # Indicate in the console for follow-up.
    resetLeds() # Reset the LEDs.
    audioDevice.setOutputVolume(100)  # Reinitialiser le volume.
    print("LED and volume reset done.") # Indicate in the console for follow-up.
    print("End of function: checkA") # Indicate in the console for follow-up.

def disruptA():
     
    """
    Function to distract the opponent.
    """
    print("Start function: disruptA.") # Indicate in the console for follow-up.
    reaction = ["sing",
                "smallFart",
                "You were rocked too close to the wall, weren't you? ",
                "You're so far behind that he's convinced he's first. ",
                "You're not encumbered by the thought process.",
                "I didn't expect anything from you, but I'm still disappointed. ",
                "You're sweet, but I wouldn't breed from you.",
                "The wheel turns, but the hamster is clearly dead.",
                "You're not the slipperiest penguin on the ice floe.",
                "It's impossible to underestimate you.",
                "It needs 10 minutes of cooking time.",
                "You're the reason we use WARNING signs."
                ] # List of action.
    nbRandom = randint(0,len(reaction)-1) # Generate a random number.
    action = reaction[nbRandom] # Recover a random distraction.
    if action == "sing": # If the action is to sing,
        print("Random distraction action : sing") # Indicate in the console for follow-up.
        audio = "/home/nao/Niels/disrupt_reaction.mp3"  # Audio file path.
        audioDevice.setOutputVolume(70)  # Set the volume to 70.
        print("Sound launch.") # Indicate in the console for follow-up.
        audioPlayer.playFile(audio)  # Play the sound.
        print("Resets the current volume.") # Indicate in the console for follow-up.
        audioDevice.setOutputVolume(100)  # Reinitialiser le son.
        print("Volume reset done.") # Indicate in the console for follow-up.
    elif action == "smallFart": # If the action is smallFart,
        print("Random distraction action: smallFart.") # Indicate in the console for follow-up.
        audio = "/home/nao/Niels/petPetit.mp3"  # Audio file path.
        audioDevice.setOutputVolume(70)  # Set the sound to 70.
        print("Sound launch.") # Indicate in the console for follow-up.
        audioPlayer.playFile(audio)  # Play the sound.
        print("Resets the current volume.") # Indicate in the console for follow-up.
        audioDevice.setOutputVolume(100)  # Reinitialiser le volume.
        print("Volume reset done.") # Indicate in the console for follow-up.
    else:
        print("Random distraction action: sentence") # Indicate in the console for follow-up.
        globalVar.TexteARepete = action
        tts.say(action) # Nao says.
    print("End function: disruptA.") # Indicate in the console for follow-up.
    
def sayCaseA(deplacement):
    """
    Function say and indicate pawn movement.

    Argument:
    deplacement -- Say and indicate deplacement's pawn.

    """
    print("Start function: sayCaseA.") # Indicate in the console for follow-up.
    if '/' not in deplacement: # If the parameter does not have a /,
        return # Stop the function.
        print("ERROR: No / in parameter.") # Indicate in the console for follow-up.
    parts = deplacement.split('/') # Separate the parameter with /.
    if len(parts) != 4: # If the parameter is not divided in four,
        return # Stop the function.
        print("ERROR: The parameter is not divided in four.") # Indicate in the console for follow-up.
    
    startingCase =  parts[0].strip() # Have the starting square.
    arrivalCase = parts[1].strip() # Have the arrival box.
    namePawn = parts[2].strip() # Have the pawn's name.
    print("Nao says its moving.") # Indicate in the console for follow-up.
    globalVar.TexteARepete = " Can you move the " + namePawn + " in the square " + startingCase + " to the square " + arrivalCase + " please ?"
    tts.say("Can you move the " + namePawn + " in the square ") # Nao says.
    time.sleep(0.5) # Wait.
    tts.say(startingCase) # Nao says.
    time.sleep(0.5) # Wait.
    tts.say(" to the square ") # Nao says.
    time.sleep(0.5) # Wait.
    tts.say(arrivalCase) # Nao says.
    time.sleep(0.5) # Wait.
    tts.say(" please ?") # Nao says.
    get_angle_en_fonction_case(startingCase+arrivalCase)
    print("Nao has finished saying his move") # Indicate in the console for follow-up.
    print("End function: sayCaseA.") # Indicate in the console for follow-up.
 
def pawnEatenA(namePawn):
    """
    Function when the opponent eats one of Nao's pawns.

    Argument:
    namePawn --  The name of the pawn.

    """
    print("Start function: pawnEatenA.") # Indicate in the console for follow-up.
    print("Change of LED colours.") # Indicate in the console for follow-up.
    #MARC print_out("Change of LED colours.") 
    leds.fadeRGB("FaceLeds", 0x0000FF, 0) # Put on blue eyes.
    leds.fadeRGB("ChestLeds", 0x0000FF, 0) # Put on the blue logo.
    leds.fadeRGB("FeetLeds", 0x0000FF, 0) # Put feets in blue.
    globalVar.TexteARepete = namePawn + " was eaten."
    tts.say(namePawn + " was eaten.") # Nao says.
    audio = "/home/nao/Niels/cry.mp3"  # Sound path.
    print("Sound launch.") # Indicate in the console for follow-up.
    #MARC print_out("Sound launch.") 
    audioPlayer.playFile(audio)  # Play the sound.
    print("LEDs are being reset.") # Indicate in the console for follow-up.
    #MARC print_out("LEDs are being reset.") 
    resetLeds() # Reset the LEDs.
    print("LED reset done.") # Indicate in the console for follow-up.
    print("End function: pawnEatenA.") # Indicate in the console for follow-up.

def eatPawnA(namePawn):
    """
    Function when Nao eats a pawn.

    Argument:
    namePawn --  The name of the pawn.

    """
    print("Start function: eatPawnA.") # Indicate in the console for follow-up.
    print("Change of LED colours.") # Indicate in the console for follow-up.
    #MARC print_out("Change of LED colours.") 
    leds.fadeRGB("FaceLeds", 0xFFFF00, 0) # Put on yellow eyes.
    leds.fadeRGB("ChestLeds", 0xFFFF00, 0) # Put on the yellow logo.
    leds.fadeRGB("FeetLeds", 0xFFFF00, 0) # Put feets in yellow.
    globalVar.TexteARepete = namePawn + " was eaten by me."
    tts.say(namePawn + " was eaten by me.") # Nao says.
    print("Sound launch.") # Indicate in the console for follow-up.
    #MARC print_out("Sound launch.") 
    audio = "/home/nao/Niels/laugh.mp3"  # Sound path.
    audioPlayer.playFile(audio)  # Play the sound.
    print("Reset the LEDs.") # Indicate in the console for follow-up.
    #MARC print_out("Reset the LEDs.") 
    resetLeds() # Reset the LEDs.
    print("LEDs reset.") # Indicate in the console for follow-up.
    print("End function: eatPawnA.") # Indicate in the console for follow-up.

def choicePawnAtEndA(namePawn):
    """
    Works when one of Nao's pieces arrives on the other side of the board and he chooses his new piece.

    Argument:
    namePawn --  The name of the pawn.

    """
    print("Start function: choicePawnAtEndA.") # Indicate in the console for follow-up.
    print("Nao speaks.") # Indicate in the console for follow-up.
    globalVar.TexteARepete = "My pawn becomes " + namePawn
    tts.say("My pawn becomes " + namePawn) # Nao says.
    print("Nao has finished speaking.") # Indicate in the console for follow-up.
    print("End function: choicePawnAtEndA.") # Indicate in the console for follow-up.

def winningA():
    """
    Function when Nao is winning.
    """
    print("Start function: winningA.") # Indicate in the console for follow-up.
    print("Change of LED colours.") # Indicate in the console for follow-up.
    leds.fadeRGB("FaceLeds", 0xFFFF00, 0) # Put on yellow eyes.
    leds.fadeRGB("ChestLeds", 0xFFFF00, 0) # Put on the yellow logo.
    leds.fadeRGB("FeetLeds", 0xFFFF00, 0) # Put feets in yellow.
    sentences = ["Congratulations, you've just won the world champion ball and chain prize!",  
                "I'm not saying you're in trouble, but your washing machine needs an emergency service.", 
                "Don't worry if you don't win the game daichec, you'll win the prize for getting yourself into trouble.",
                "You seem to be swimming in a pool of nonsense without a lifebuoy.", 
                "It looks like you've got yourself in trouble again.",
                "With all that, you could write a manual: How to sink in with style!",
                "You give him a fan, he'll shake his head.",
                "He has a head for peeling stones.",
                "You didn't invent gunpowder, but you weren't far away when the cannon went off.",
                "You're like a magnet for trouble. Maybe you should change brands!"
                ] # List of actions.
    nbRandom = randint(0,len(sentences)-1) # Generate a random number.
    sentence = sentences[nbRandom] # Have a random reaction.
    print("Nao speaks.") # Indicate in the console for follow-up.
    globalVar.TexteARepete = sentence
    tts.say(sentence) # Nao says.
    print("Nao has finished speaking.") # Indicate in the console for follow-up.
    print("LED and volume reset in progress.") # Indicate in the console for follow-up.
    resetLeds() # Reset the LEDs.
    print("LED and volume reset done.") # Indicate in the console for follow-up.
    print("End function: winningA.") # Indicate in the console for follow-up.

def eyesMultiColored():
    """
    Function to make Nao's eyes multicoloured.
    """
    print("Start function: eyesMultiColored.") # Indicate in the console for follow-up.
    colors = [0xff0000, 0xffed00, 0x00ffc8, 0x0042ff, 0x6c00ff, 0xca00ff, 0xff0096] # List of colours.
    for i in colors: # For each colour, 
        print("LED colour change.") # Indicate in the console for follow-up.
        #MARC print_out("LED colour change.") 
        leds.fadeRGB("FaceLeds", i, 1.0) # putting the eyes in the colour.
        time.sleep(0.2) # Wait.
    print("End function: eyesMultiColored.") # Indicate in the console for follow-up.
    
def sayCheckA():
    """
    Function when Nao fails.
    """
    print("Start function: sayCheckA.") # Indicate in the console for follow-up.
    print("LED colour change.") # Indicate in the console for follow-up.
    leds.fadeRGB("FaceLeds", 0xFFFF00, 1.0) # Put on yellow eyes.
    leds.fadeRGB("ChestLeds", 0xFFFF00, 0) # Mattre le logo jaune.
    leds.fadeRGB("FeetLeds", 0xFFFF00, 0) # Put feets in yellow.
    print("Nao speaks.") # Indicate in the console for follow-up.
    globalVar.TexteARepete = "Echec"
    tts.say("Echec") # Nao says.
    print("Nao has finished speaking.") # Indicate in the console for follow-up.
    audio = "/home/nao/Niels/laugh.mp3" # Sound path.
    print("Sound launch.") # Indicate in the console for follow-up.
    audioPlayer.playFile(audio) # Play the sound.
    print("LED and volume reset in progress.") # Indiquer dans la console
    resetLeds() # Reset the LEDs.
    print("LED and volume reset done.") # Indicate in the console for follow-up.
    print("End function: sayCheckA.") # Indicate in the console for follow-up.



#----------------------------------------------------------DANCE MOVES---------------------------------------------------------------------------
def danceArmsDisco1():
    """
    Function for the first dance movement with the arms.
    """
    jointNames = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", # Left arm.
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"   # Right arm.
    ]
    anglesMoovDance1 = [
        # Left arm.
        math.radians(53.7),  # LShoulderPitch
        math.radians(-18.0),  # LShoulderRoll
        math.radians(-9.8),  # LElbowYaw
        math.radians(-57.0),  # LElbowRoll
        math.radians(12.4),  # LWristYaw
        math.radians(1.0),  # LHand

        # Right arm.
        math.radians(-64.0),  # RShoulderPitch
        math.radians(-46.7),  # RShoulderRoll
        math.radians(-35.2),  # RElbowYaw
        math.radians(2.0),  # RElbowRoll
        math.radians(-40.7),  # RWristYaw
        math.radians(0.0),  # RHand
    ]
    duration = 2.0  # Duration of movement.
    print("Nao starts a danceArmsDisco1 movement.") # Indicate in the console for follow-up.
    motion.angleInterpolation(jointNames, anglesMoovDance1, [duration]*len(jointNames), True) # Make the move.
    print("Nao finishes a dance moveArmsDisco1.") # Indicate in the console for follow-up.

def danceArmsDisco2():
    """
    Function of the second dance movement with the arms.
    """
    jointNames = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", # Left arm.
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand" # Right arm.
    ]
    anglesMoovDance2 = [
        # Left arm.
        math.radians(-63.3),  # LShoulderPitch
        math.radians(52.1),  # LShoulderRoll
        math.radians(-0.4),  # LElbowYaw
        math.radians(-2.0),  # LElbowRoll
        math.radians(104.5),  # LWristYaw
        math.radians(1.0),  # LHand

        # Right arm.
        math.radians(45.4),  # RShoulderPitch
        math.radians(15.1),  # RShoulderRoll
        math.radians(30.4),  # RElbowYaw
        math.radians(82.7),  # RElbowRoll
        math.radians(20.4),  # RWristYaw
        math.radians(0.0),  # RHand
    ]
    duration = 2.0  # Duration of movement.
    print("Nao starts a danceArmsDisco2 movement.") # Indicate in the console for follow-up.
    motion.angleInterpolation(jointNames, anglesMoovDance2, [duration]*len(jointNames), True) # Make the move.
    print("Nao finishes a dance moveArmsDisco2.") # Indicate in the console for follow-up.

def danceLegDisco1():
    """
    Function for the first dance movement with the legs.
    """
    jointNames = [
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll", # Left legs.
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"  # Right legs.
    ]
    anglesMoovLegDance1 = [
        # Left legs.
        math.radians(-20.9),  # LHipYawPitch
        math.radians(-1.1),  # LHipRoll
        math.radians(-44.3),  # LHipPitch
        math.radians(121.0),  # LKneePitch
        math.radians(-68.2),  # LAnklePitch
        math.radians(4.7),  # LAnkleRoll

        # Right legs.
        math.radians(-17.3),  # RHipYawPitch
        math.radians(-45.3),  # RHipRoll
        math.radians(-27.6),  # RHipPitch
        math.radians(-5.3),  # RKneePitch
        math.radians(30.5),  # RAnklePitch
        math.radians(-25.2),  # RAnkleRoll
    ]
    duration = 2.0  # Duration of movement.
    print("Nao starts a dance moveLegDisco1.") # Indicate in the console for follow-up.
    motion.angleInterpolation(jointNames, anglesMoovLegDance1, [duration]*len(jointNames), True) # Make the move.
    print("Nao finishes a danceLegDisco1 move.") # Indicate in the console for follow-up.

def danceLegDisco2():
    """
    Function for the second dance movement with the legs.
    """
    jointNames = [
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll", # Left legs.
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"  # Right legs.
    ]
    anglesMoovLegDance2 = [
        # Left legs.
        math.radians(-1.1),  # LHipYawPitch
        math.radians(45.3),  # LHipRoll
        math.radians(13.9),   # LHipPitch
        math.radians(-5.3),  # LKneePitch
        math.radians(-0.9),  # LAnklePitch
        math.radians(7.3),   # LAnkleRoll

        # Right legs.
        math.radians(-1.1),  # RHipYawPitch
        math.radians(-8.0),   # RHipRoll
        math.radians(-47.5),    # RHipPitch
        math.radians(121.0),   # RKneePitch
        math.radians(-68.0),    # RAnklePitch
        math.radians(-3.4),    # RAnkleRoll
    ]
    duration = 2.0   # Duration of movement.
    print("Nao starts a dance danceLegDisco2.") # Indicate in the console for follow-up.
    motion.angleInterpolation(jointNames, anglesMoovLegDance2, [duration]*len(jointNames), True) # Make the move.
    print("Nao finishes a danceLegDisco2 move.") # Indicate in the console for follow-up.

def dabDance():
    """
    Function to move DAB.
    """
    jointNames = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", # Left arm.
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"   # Right arm.
    ]
    anglesMoovDance1 = [
        # Left arm.
        math.radians(-73.1),  # LShoulderPitch
        math.radians(74.0),  # LShoulderRoll
        math.radians(-38.7),  # LElbowYaw
        math.radians(-2.0),  # LElbowRoll
        math.radians(27.2),  # LWristYaw
        math.radians(1.0),  # LHand

        # Right arm.
        math.radians(-33.2),  # RShoulderPitch
        math.radians(46.8),  # RShoulderRoll
        math.radians(34.9),  # RElbowYaw
        math.radians(69.1),  # RElbowRoll
        math.radians(7.0),  # RWristYaw
        math.radians(1.0),  # RHand
    ]
    duration = 2.0  #  Duree de l'animation.
    print("Nao starts a dance dabDance.") # Indicate in the console for follow-up.
    motion.angleInterpolation(jointNames, anglesMoovDance1, [duration]*len(jointNames), True) # Make the move.
    print("Wait 4 seconds dabDance.") # Indicate in the console for follow-up.
    time.sleep(4)
    print("Nao finishes a dabDance move.") # Indicate in the console for follow-up.

def legsApartDance():
    """
    DAB movement function at foot level.
    """
    jointNames = [
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll", # Left legs.
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"  # Right legs.
    ]
    anglesMoovLegDance2 = [
        # Left legs.
        math.radians(-8.9),  # LHipYawPitch
        math.radians(25.6),  # LHipRoll
        math.radians(16.4),   # LHipPitch
        math.radians(-3.5),  # LKneePitch
        math.radians(1.4),  # LAnklePitch
        math.radians(-22.8),   # LAnkleRoll

        # Right legs.
        math.radians(-8.9),  # RHipYawPitch
        math.radians(-30.5),   # RHipRoll
        math.radians(14.8),    # RHipPitch
        math.radians(-5.3),   # RKneePitch
        math.radians(7.0),    # RAnklePitch
        math.radians(22.8),    # RAnkleRoll
    ]
    duration = 4.0  #  Duree de l'animation.
    print("Nao starts a dance legsApartDance.") # Indicate in the console for follow-up.
    motion.angleInterpolation(jointNames, anglesMoovLegDance2, [duration]*len(jointNames), True) # Make the move.
    print("Wait 4 seconds legsApartDance.") # Indicate in the console for follow-up.
    time.sleep(4)
    print("Nao finishes a legsApartDance move.") # Indicate in the console for follow-up.
    
def dance():
    """
    Function to make Nao dance.
    """
    for i in range(2): # Repeat twice,
        print("Nao gets up.") # Indicate in the console for follow-up.
        standUp() # Nao gets up.
        threadMoovArms1 = threading.Thread(target=danceArmsDisco1) # Create a thread to make the first dance movement with the arms.
        threadMoovLeg1= threading.Thread(target=danceLegDisco1) # Create a thread to make the first dance movement with the legs.
        # Execute threads.
        print("Start of thread for the first dance movement.") # Indicate in the console for follow-up.
        threadMoovArms1.start()
        threadMoovLeg1.start()
        # Wait for threads to finish.
        threadMoovArms1.join()
        threadMoovLeg1.join()
        print("End of thread for the first dance movement.") # Indicate in the console for follow-up.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print("Nao gets up.") # Indicate in the console for follow-up.
        standUp() # Nao gets up.
        print("Start of thread for the second dance movement.") # Indicate in the console for follow-up.
        threadMoovArms2 = threading.Thread(target=danceArmsDisco2) #  Create a thread to do the second dance movement with the arms.
        threadMoovLeg2= threading.Thread(target=danceLegDisco2) # Create a thread to do the second dance movement with the legs.
        # Execute threads.
        threadMoovArms2.start()
        threadMoovLeg2.start()
        # Wait for threads to finish.
        threadMoovArms2.join()
        threadMoovLeg2.join()
        print("End of thread for the second dance movement.") # Indicate in the console for follow-up.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print("Nao gets up.") # Indicate in the console for follow-up.
    standUp() # Nao gets up.
    threadMoovHandsUp = threading.Thread(target=dabDance) # Create a thread to make Nao do the DAB.
    threadMoovLegsApart = threading.Thread(target=legsApartDance) # Create a thread to position Nao's legs for the DAB.
    # Execute threads.
    print("Start of DAB movement thread.") # Indicate in the console for follow-up.
    threadMoovHandsUp.start()
    threadMoovLegsApart.start()
    # Wait for threads to finish.
    threadMoovHandsUp.join()
    threadMoovLegsApart.join()
    print("End of DAB movement thread.") # Indicate in the console for follow-up.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print("Nao gets up.") # Indicate in the console for follow-up.
    standUp() # Nao gets up.
#-----------------------------------------------------------------------------------------------------------------------------------------

def songCheckmatewin():
    """
    Fonction pour lancer le son de victoire.
    """
    print("Start function: songCheckmatewin.") # Indicate in the console for follow-up.
    audio = "/home/nao/Niels/win.mp3" # Sound path.
    audioDevice.setOutputVolume(80)  # Set the volume to 50.
    print("Sound launch.") # Indicate in the console for follow-up.
    audioPlayer.playFile(audio) # Play the sound.
    print("End function: songCheckmatewin.") # Indicate in the console for follow-up.

def multiColored():
    """
    Fonction pour mettre les yeux multicolores.
    """
    print("Start function: multiColored.") # Indicate in the console for follow-up.
    for i in range (50): # Repeat 50 times,
        colors = [0xff0000, 0xffed00, 0x00ffc8, 0x0042ff, 0x6c00ff, 0xca00ff, 0xff0096]  # List of colours.
        for color in colors:  # For each colour,
            fadeRGB("FaceLeds", color, 1.0) # Put the colour eyes.
            leds.fadeRGB("ChestLeds", color, 0.1)  # Put the colour logo.
            leds.fadeRGB("FeetLeds", color, 0.1)  # Put the colour feet
    print("End function: multiColored.") # Indicate in the console for follow-up.

def winA():
    """
    Function when Nao has won the game.
    """
    print("Start function: winA.") # Indicate in the console for follow-up.
    print("Nao gets up.") # Indicate in the console for follow-up.
    standUp() # Nao gets up.
    print("Nao steps back.") # Indicate in the console for follow-up.
    motion.moveTo(-0.3, 0.0, 0.0) # Nao steps back.
    print("Nao has finished backing up and is speaking.") # Indicate in the console for follow-up.
    globalVar.TexteARepete = "Checkmate! I've won! You are shit!"
    tts.say("Checkmate! I've won! You are shit!") # Nao says.
    print("Nao has finished speaking.") # Indicate in the console for follow-up.
    threadEyes = threading.Thread(target=multiColored) # Create a thread to add multicoloured eyes.
    threadDance = threading.Thread(target=dance) # Create a thread to make Nao dance.
    threadSong = threading.Thread(target=songCheckmatewin) # Create a thread to launch the end sound.
    # Execute threads.
    print("Debut de thread des yeux multicouleurs, danse et son.") # Indicate in the console for follow-up.
    threadSong.start()
    threadEyes.start()
    threadDance.start()
    # Wait for threads to finish.
    threadSong.join()
    threadEyes.join()
    threadDance.join()
    print("End of thread of multicoloured eyes, dance and sound.") # Indicate in the console for follow-up.
    print("LED and volume reset in progress.") # Indicate in the console for follow-up.
    audioDevice.setOutputVolume(100) # Set the volume to 50.
    resetLeds() # Reset the LEDs.
    print("LED and volume reset done.") # Indicate in the console for follow-up.
    print("Nao gets up.") # Indicate in the console for follow-up.
    standUp() # Nao gets up.
    print("End function: winA.") # Indicate in the console for follow-up.

