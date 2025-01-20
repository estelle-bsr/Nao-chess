import sys
from globalVar import *

import chess
import chess.engine
import subprocess

# Path to your Stockfish executable (adjust if necessary)
stockfish_path = "Z:\\Bureau\\Nao\\nao-chess\\chess_game\\stockfish\\stockfish-windows-x86-64-avx2.exe"

# Start the Stockfish engine using subprocess
engine = subprocess.Popen(stockfish_path, universal_newlines=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

# Send the "uci" command to initialize the UCI protocol
engine.stdin.write("uci\n")
engine.stdin.flush()

# Initialize the chess board
board = chess.Board()

# Get the best move from Stockfish by sending the appropriate UCI commands
engine.stdin.write("position startpos\n")
engine.stdin.flush()
engine.stdin.write("go movetime 2000\n")  # "2000" is the time in milliseconds for the move calculation
engine.stdin.flush()

# Read the move output from Stockfish
while True:
    line = engine.stdout.readline()
    if line.startswith("bestmove"):
        best_move = line.split()[1]
        break

# Convert the UCI move to a chess move
move = chess.Move.from_uci(best_move)

# Apply the move to the board
board.push(move)

# Print the result
print("Best move: {mov")
print(board)

# Don't forget to terminate the engine when you're done
engine.stdin.write("quit\n")
engine.stdin.flush()
engine.terminate()
