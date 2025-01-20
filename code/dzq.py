import sys
sys.path.append("z:\\Bureau\\Nao\\nao-chess\\movement\\")
sys.path.append("z:\\Bureau\\Nao\\nao-chess\\chess_game\\")
sys.path.append("C:\pynaoqi\lib")
from globalVar import *
from movement import *
sys.path.append("./picture")
import OperationPicture as op
import chessReader as cr
import cv2 as cv
import threading
import time
import os
import numpy as np
from naoqi import ALProxy
import math
from chessReader import *
from skimage.measure import compare_ssim as ssim
import main as m
import chess


