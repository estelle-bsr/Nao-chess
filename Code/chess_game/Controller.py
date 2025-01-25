from Interface import IVue
from Interface import IMouvement

class ControllerVue(IVue):
    partie = str
    def __init__(self):
        self.partie = "e2e4"
    def async_GetMove(self):
        return self.partie
    def async_IsSomeoneMoved(self):
        pass
    def isWhite(self):
        return True

class ControllerMouvement(IMouvement):
    partie = str
    def __init__(self):
        self.partie = "e4"
    def getDifficulty():
        return 1
    def attendre(self)->bool:
        pass
    def play(self,deplacement):
        pass
    def reaction():
        pass
    def startup():
        pass
    def sit():
        pass
       


