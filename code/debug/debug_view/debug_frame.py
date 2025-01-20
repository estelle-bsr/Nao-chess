import os

from Tkinter import *

from debug_camera_frame import DebugCameraFrame
from debug_commands_frame import DebugCommandsFrame
from debug_console_frame import DebugConsoleFrame
from game_board_frame import GameBoardFrame

IMG_FOLDER_PATH = 'debug/debug_view/example_images/'

## Classe GUI contenant toutes les informations et commandes pour le debogage de NAO
class DebugFrame(Frame):

    ## Constructeur
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)

        # Configuration de la grille de la frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # ---------- Blocs des gauche (terminaux) ---------- #
        self.terminals_frame = Frame(self, background='#E5E5E5')
        self.terminals_frame.grid(row=0, column=0, sticky=NSEW)

        # Configuration de la grille du bloc des terminaux
        self.terminals_frame.rowconfigure(0, weight=1)
        self.terminals_frame.rowconfigure(1, weight=10)
        self.terminals_frame.columnconfigure((0,1), weight=1)

        # Label Interpretation actions humaines
        self.humain_action_console_label = Label(self.terminals_frame, text="Interpretations actions humaines", background="#E5E5E5")
        self.humain_action_console_label.grid(row=0, column=0)

        # Terminal d'actions humaines
        self.humain_action_console_terminal = DebugConsoleFrame(self.terminals_frame, background="#0000FF", borderwidth=2)
        self.humain_action_console_terminal.grid(row=1, column=0, padx=4, pady=8, sticky=NS)

        # Label Actions Nao
        self.nao_action_console_label = Label(self.terminals_frame, text="Actions Nao", background="#E5E5E5")
        self.nao_action_console_label.grid(row=0, column=1)

        # Terminal d'actions Nao
        self.nao_action_console_terminal = DebugConsoleFrame(self.terminals_frame, background="#00FF00", borderwidth=2)
        self.nao_action_console_terminal.grid(row=1, column=1, padx=4, pady=8, sticky=NS)
        
        # -------------------------------------------------- #

        # ---------- Bloc de droite ---------- #

        self.right_frame = Frame(self, background='#FAFAFA')
        self.right_frame.grid(row=0, column=1, sticky=NSEW)

        # Configuration de la grille du bloc de droite
        self.right_frame.rowconfigure(0, weight=2)
        self.right_frame.rowconfigure(1, weight=1)
        self.right_frame.columnconfigure((0,1), weight=2)

        # Ajout de la frame d'image du plateau actuel
        self.actual_board_frame = GameBoardFrame(master=self.right_frame, title="Interpretation plateau actuel", image_name=IMG_FOLDER_PATH + "figma_chess_board_human.png")
        self.actual_board_frame.grid(row=0, column=0)

        # Ajout de la frame d'image du plateau prevu par Nao
        self.actual_board_frame = GameBoardFrame(master=self.right_frame, title="Actions Nao", image_name=IMG_FOLDER_PATH + "figma_chess_board_nao.png")
        self.actual_board_frame.grid(row=0, column=1)

        # Ajout de la frame du retour camera de Nao
        self.camera_nao = DebugCameraFrame(master=self.right_frame)
        self.camera_nao.grid(row=1, column=0, padx=4, pady=8, sticky=NSEW)

        # Ajout de la frame de commandes
        self.commands_frame = DebugCommandsFrame(master=self.right_frame)
        self.commands_frame.grid(row=1, column=1, padx=4, pady=8, sticky=NSEW)

## ---------- TEST ZONE ---------- ##


if __name__ == "__main__":

    # Creation de la fenetre de test
    test_window = Tk()
    test_window.geometry("800x600")
    test_window.minsize(500, 375)
    test_window.title("Nao Frame test")

    # Creation de la DebugFrame
    debug_frame = DebugFrame(master=test_window)
    debug_frame.pack(expand=True, fill=BOTH)

    # Lancement de la fenetre
    test_window.mainloop()