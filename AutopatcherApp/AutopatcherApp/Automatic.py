from State import State
import time

class Automatic(State):
    
    #Local Vairables

    def __init__(self, pMain = None, pSystemIO = None, pName = ""):
        super(Automatic, self).__init__(pMain, pSystemIO, pName)
        print('Created: Automatic State')

    def Start(self):
        super(Automatic, self).Start()

    def Update(self, pSender):
        super(Automatic, self).Update(pSender)

    def End(self):
        super(Automatic, self).End()



