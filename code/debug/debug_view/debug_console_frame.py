from Tkinter import *

class DebugConsoleFrame(Frame):

    # Constructeur de la classe
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)

        # Bloc de texte pour la console
        self.console_text_block = Text(self, wrap='word', height=15, width=60)
        self.console_text_block.pack(side=LEFT, fill=BOTH, expand=True)

        # Barre de defilement
        self.console_scrollbar = Scrollbar(self, command=self.console_text_block.yview)
        self.console_scrollbar.pack(side=RIGHT, fill=Y)
        self.console_text_block.config(yscrollcommand=self.console_scrollbar.set)

        # Configuration des tags de coloration
        self.console_text_block.tag_configure('normal', foreground="black")
        self.console_text_block.tag_configure('error', foreground="#FF0000")


    
    # Fonction d'ecriture dans le terminal
    def printout(self, message):
        self.console_text_block.insert(END, message + '\n', 'normal')
        self.console_text_block.see(END)


    # Fonction d'ecriture d'erreur dans le terminal
    def printerr(self, message):
        self.console_text_block.insert(END, message + '\n', 'error')
        self.console_text_block.see(END)