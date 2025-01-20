from Tkinter import *

class DebugCommandsFrame(Frame):

    ## Constructeur
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)

        # Label du bloc des commandes
        self.commands_label = Label(self, text="Commands")
        self.commands_label.pack(padx=8, pady=8)

        # Valeur de l'Auto-mode
        self.auto_mode = IntVar()

        # Checkbutton du auto-mode
        # permettant de definir si les actions prevues par Nao 
        # sont lancees automatiquement ou non
        self.auto_mode_checkbutton = Checkbutton(self, text="Auto-mode", variable=self.auto_mode)
        self.auto_mode_checkbutton.pack(padx=8, pady=8)

        # Bouton pour lancer une action de Nao
        self.launch_button = Button(self, text="Launch", state=DISABLED, bg="#007852", fg="white", font="Verdana-Bold 14", command=self.launch_action)
        self.launch_button.pack(padx=8)
    

    # Methode pour acceder a la valeur de auto_mode 
    # sous forme de booleen
    def is_auto_mode(self):
        return bool(self.auto_mode.get())
        

    # Fonction qui va lancer l'action de Nao
    def launch_action(self):
        print("Action launched")

    