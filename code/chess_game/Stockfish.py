import sys
print(sys.path)

from globalVar import *
import chess
import chess.engine
import random
import subprocess
import main as m

class Stockfish():
    def __init__(self):
        self.engine = subprocess.Popen(STOCKFISH_PATH, universal_newlines=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.engine.stdin.write("uci\n")
        self.engine.stdin.flush()
        self.engine.stdin.write("setoption name Skill Level value "+str(10)+"\n")
        self.engine.stdin.flush()
        self.color = "white"
        self.move_count = 0 
        self.board = chess.Board("rnbqkbnr/pppppppp/8/4N2Q/8/8/PPPPPPPP/RNB1KB1R w KQkq - 0 1")#
    def __del__(self): 
        self.engine.terminate()
    def setSide(self,IsWhite):
        if IsWhite:
            self.color = "white"
        else:
            self.color = "black"
    def robot_play_best_move(self):
        print self.board
        print self.board.turn
        print self.color
        fen = self.board.fen()
        if self.board.turn:
            if self.color != "white":
                return "NAO can't play not is turn"
        else:
            if self.color != "black":
                return "NAO can't play not is turn"
        self.board.turn 
        #Si vrai NAO peut jouer | Sinon NAO de joue pas
        print "position fen "+fen+"\n"
        print "go color "+ self.color +" depth 10 movetime 200\n"
        self.engine.stdin.write("position fen "+fen+"\n")
        self.engine.stdin.flush()
        self.engine.stdin.write("go color "+ self.color +" depth 10 movetime 200\n")
        self.engine.stdin.flush()
        while True:
            line = self.engine.stdout.readline()
            print line
            if line.startswith("bestmove"):
                best_move = line.split()[1]
                break
        move = chess.Move.from_uci(best_move)
        if self.board.is_capture(move):
            m.eatPawn(m.nomPion(self.board.piece_at(move.to_square).symbol()))
        self.board.push(move)
        print self.board
        if self.board.is_checkmate():
            m.win()
        elif self.board.is_check():
            m.sayCheck()
        if move.promotion is not None:
            m.choicePawnAtEnd("reine/queen")
        #print "EVAL" + str(self.get_eval())
        print self.board
        return chess.Move.from_uci(best_move)
                
    def get_eval(self):
        fen = self.board.fen()
        self.engine.stdin.write("position fen "+fen+"\n")
        self.engine.stdin.flush()
        self.engine.stdin.write("go color "+ self.color +" depth 10 movetime 200\n")
        self.engine.stdin.flush()
        while True:
            line = self.engine.stdout.readline()
            if line.startswith("info depth 10"):
                eval = line.split()[9]
                break
        return eval
    def get_board(self):
        return self.board
    def depth(self,choix):
        self.engine.stdin.write("setoption name Skill Level value "+str(choix*4)+"\n")
        self.engine.stdin.flush()
    def human_play(self,move):
        deplacement = chess.Move.from_uci(move[0]+move[1])
        deplacement2 = chess.Move.from_uci(move[1]+move[0])

        if deplacement in self.board.legal_moves :
            if self.board.is_checkmate():
                m.checkmate()
            if self.board.is_check():
                m.check()
            if self.board.is_capture(deplacement):
                m.pawnEaten(m.nomPion(self.board.piece_at(deplacement.to_square).symbol()))
            self.board.push(deplacement)
            return deplacement
        
        if deplacement2 in self.board.legal_moves :
            if self.board.is_checkmate():
                m.checkmate()
            if self.board.is_check():
                m.check()
            if self.board.is_capture(deplacement2):
                m.pawnEaten(m.nomPion(self.board.piece_at(deplacement2.to_square).symbol()))
            self.board.push(deplacement2)
            return deplacement2

        m.cheating()
        raise Exception("Human try to play "+move[0]+move[1]+" move does not exist")

                      
    def pawnEaten(self,deplacement):
        move = chess.Move.from_uci(deplacement)
        capture_message ="no Pawn eaten"
        if self.board.is_capture(move):
            captured_piece=self.board.piece_at(move.to_square)
            piece_symbol = captured_piece.symbol().lower()
            if piece_symbol == 'p':
                capture_message = "pion/pawn"
            elif piece_symbol == 'n':
                capture_message = "cavalier/knight"
            elif piece_symbol == 'b':
                capture_message = "fou/bishop"
            elif piece_symbol == 'r':
                capture_message = "tour/rook"
            elif piece_symbol == 'q':
                capture_message = "reine/queen"
            elif piece_symbol == 'k':
                capture_message = "roi/king"
            else:
                capture_message = "piece inconnue / unknown piece"
        return capture_message
    def DecisionMaker(self,state):
        randSeed = random.randint(0, 9)
        action = "NOTHING"
        fen = self.board.fen()
        print(self.board)
        self.engine.stdin.write("position fen "+fen+"\n")
        self.engine.stdin.flush()
        self.engine.stdin.write("go color "+ self.color +"depth 10 movetime 200\n")
        self.engine.stdin.flush()
        while True:
            line = self.engine.stdout.readline()
            if line.startswith("info depth 10"):
                centipawn = line.split()[9]
                break
        if(self.board.fullmove_number<10):  # ne fait aucune action en desou des 10 premier coup
            if state == "HUMAN_PLAYING":
                print("DECISIONMAKER FROM : "+state +" TO : ROBOT_PLAYING")
                return "ROBOT_PLAYING"
            if state == "ROBOT_PLAYING":
                print("DECISIONMAKER FROM : "+state +" TO : HUMAN_PLAYING")
                return "HUMAN_PLAYING"
        """
        #-----------------------
        if(self.board.is_game_over()):
            return board.result().split("-")[0].split("/")[-1]
        #-----------------------
        info = self.engine.analyse(self.board, chess.engine.Limit(time=1))
        score = info['score'].relative.score()
        if(not self.isWhite):
            score= score *-1
        #----------------------- 
        if(state =="LOOKING"):
            if(score>100):
                return "WINNING"
            if(score<-100):
                return "LOSING"
            return "PLAYING"
        #-----------------------
        if(state == "EVENT"):
            return "PLAYING"
        #-----------------------
        ran =random.randint(0,1)
        print(ran)
        if(state != "EVENT" and ran==0):
            return "EVENT"
        if(state == "WINNING" or state == "LOSING"):
            return "PLAYING"
        return action
        """