import sys
import time

import PIL.Image, PIL.ImageTk

from naoqi import ALProxy
from threading import Thread
from Tkinter import *

# ---------- TEMPORARY CONSTANTS ---------- #
robot_ip = "172.16.1.163" # Define IP adress.
robot_port = 9559 # Define port. 
# ----------------------------------------- #

class DebugCameraFrame(Frame):

    ## Constructeur
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)

        # Connexion a la camera de Nao
        self.nao_cam_proxy = ALProxy("ALVideoDevice", robot_ip, robot_port)

        # Definition de la resolution et de la 
        self.resolution = 2  # VGA
        self.colorSpace = 11 # RGB

        # "Abonnement" a la video de Nao
        self.video_nao = self.nao_cam_proxy.subscribeCamera("python_client", 1, self.resolution, self.colorSpace, 5) 

        # Creation de la variable qui contiendra l'image actuelle
        self.current_image = None

        # Creation du canva qui affichera l'image 
        self.camera_canva = Canvas(self, width=320, height=240)
        self.camera_canva.pack()

        # On cree un thread qui va importer et actualiser les images de la camera de Nao
        self.update_thread = Thread(target=self.update_webcam)

        # On lance le thread 
        self.update_thread.start()
    

    # Fonction qui actualise l'image prise par Nao dans l'interface
    def update_webcam(self):
        
        # Recuperation d'une image provenant de la camera de Nao
        nao_frame = self.nao_cam_proxy.getImageRemote(self.video_nao)

        # Recuperation de la largeur, hauteur et de l'array de l'image
        imageWidth = nao_frame[0]
        imageHeight = nao_frame[1]
        imageArray = nao_frame[6]

        # Stockage de la frame dans current_image
        self.current_image = PIL.Image.frombytes("RGB", (imageWidth, imageHeight), imageArray)
        
        # Conversion de l'image en noir et blanc
        self.current_image = self.current_image.convert("L")

        # Importation de current_image dans un format adapte a Tkinter
        self.photo = PIL.ImageTk.PhotoImage(image=self.current_image)

        # Affichage de l'image dans le canva
        self.camera_canva.create_image(0, 0, image=self.photo, anchor=NW)

        # Rappel de la fonction apres 1 ms
        self.after(1, self.update_webcam)

    # Fonction qui se desabonne du flux video de Nao
    # Fonction declenchee a la fermeture de l'application
    def unsubscribe_nao_cam(self):
        self.nao_cam_proxy.unsubscribe(self.video_nao)

