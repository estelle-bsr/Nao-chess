import PIL.Image, PIL.ImageTk

from Tkinter import *

class GameBoardFrame(Frame):

    # Constructeur de la classe
    def __init__(self, master=None, title="Plateau de jeu", image_name=None, **kw):
        Frame.__init__(self, master, **kw)

        # Creation du label titre
        self.title_label = Label(self, text=title)
        self.title_label.pack()

        # Creation du canva (la zone de l'image)
        self.board_image_canvas = Canvas(self, width=350, height=350)
        self.board_image_canvas.pack()

        # Importation de l'image 
        image = PIL.Image.open(image_name)

        # Calcul des dimensions pour conserver le ratio
        canvas_width, canvas_height = 350, 350
        img_width, img_height = image.size

        # Calcul du facteur d'echelle pour s'ajuster au canvas tout en gardant les proportions
        scale = min(canvas_width / float(img_width), canvas_height / float(img_height))
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # Redimensionnement de l'image avec les nouvelles dimensions
        image = image.resize((new_width, new_height), PIL.Image.ANTIALIAS)

        # Conversion de l'image redimensionnee pour Tkinter
        self.board_image = PIL.ImageTk.PhotoImage(image)

        # Ajout de l'image dans le canva
        self.board_image_canvas.create_image(0, 0, anchor=NW, image=self.board_image)
        
        
