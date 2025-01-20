from threading import Thread
from Tkinter import *

from debug_view.debug_frame import DebugFrame

class Debug():
    """
        Classe generale contenant tous les outils pour le debogage.
    """

    ## Constructeur
    def __init__(self):

        # Creation de la fenetre de test
        self.debug_window = Tk()
        self.debug_window.geometry("800x600")
        self.debug_window.minsize(500, 375)
        self.debug_window.title("Nao Debug Tools")

        # Creation de la DebugFrame
        self.debug_frame = DebugFrame(master=self.debug_window)
        self.debug_frame.pack(expand=True, fill=BOTH)


    ## Fonction de lancement de la frame de Debug
    def start(self):
        
        # Lancement de la fenetre
        self.debug_window.mainloop()


    ## Flux de sortie sur les actions humaines 
    def printout_humain(self, message):
        
        # Ecriture sur le terminal d'actions humaines
        self.debug_frame.humain_action_console_terminal.printout(message)

    ## Flux d'erreur sur les actions humaines 
    def printerr_humain(self, message):
        
        # Ecriture sur le terminal d'actions humaines
        self.debug_frame.humain_action_console_terminal.printerr(message)

    ## Flux de sortie sur les actions de Nao 
    def printout_nao(self, message):
        
        # Ecriture sur le terminal d'actions de Nao
        self.debug_frame.nao_action_console_terminal.printout(message)

    ## Flux d'erreur sur les actions de Nao 
    def printerr_nao(self, message):
        
        # Ecriture sur le terminal d'actions de Nao
        self.debug_frame.nao_action_console_terminal.printerr(message)


## ---------- TEST ZONE ---------- ##
if __name__ == "__main__":
    test_frame = Debug()
    test_frame_thread = Thread(target=test_frame.start)
    test_frame_thread.start()

    # Simuler les appels dans un thread separe
    import time

    def test_logs():
        time.sleep(1)
        test_frame.printout_humain("Tacos")
        test_frame.printout_humain("Tacos")
        test_frame.printerr_humain("Kebab")
        test_frame.printout_nao("Je voudrais des Wings")
        test_frame.printout_humain("La sauce du chef avec les Wings ?")
        test_frame.printerr_nao("Mais c'est quoi encore ce truc !?")

    log_thread = Thread(target=test_logs)
    log_thread.start()