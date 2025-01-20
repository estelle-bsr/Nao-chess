from Stockfish import Stockfish 
import sys
from globalVar import *
sys.path.append(PATH_TO_PROJECT+"movement\\")
sys.path.append(PATH_TO_PROJECT+"picture\\")
sys.path.append(PATH_TO_PROJECT)
sys.path.append("C:\\pynaoqi\\lib\\")
from OperationPicture import *
from movement import *
import math as math
from app import app


regardRobot(robot_ip,robot_port)


def main():
    state = "INIT"  # ["LOOKING","ERROR","PLAYING","DANCING"]
    stockfish = Stockfish()
    while True:
        # stockfish.DecisionMaker(state) # This would depend on your actual method structure

        if state == "INIT":
            
            """
            regardRobot(robot_ip,robot_port)
            side = isRobotWhite(robot_ip,robot_port)
            #side = True
            stockfish.setSide(side)
            #a = mouvement.start(True)
            a = 1
            stockfish.depth(a)
            if not side : 
                state = "HUMAN_PLAYING"
            else :
                state = "ROBOT_PLAYING"
            
            
            print("STATE INIT depth : "+str(a))
            """
        
        elif state == "HUMAN_PLAYING":
            move = "e2e4" #vue.getmove
            stockfish.human_play(move)
            
        
        elif state == "ROBOT_PLAYING":
            print stockfish.robot_play_best_move()
            pass
        
        elif state == "WINNING":
            # controllerMouvement.winning()  
            pass
        
        elif state == "LOSING":
            # controllerMouvement.losing()  
            pass
        
        elif state == "WIN":
            #controllerMouvement.win()
            state = "INIT"
            break
        
        elif state == "LOSE":
            #controllerMouvement.lose()
            state = "INIT"
            break
        
        elif state == "EVENT":
            #main.disrupt()
            pass
        
        elif state == "ERROR":
            print(stateMessage)
            #controllerMouvement.wrongMove()
            state = "LOOKING"
            break  # This may need to be removed if you don't want the loop to stop here
        
        else:
            print("Unknown state encountered")
            break  # Terminate the loop on unexpected state

        state = stockfish.DecisionMaker(state)

main()