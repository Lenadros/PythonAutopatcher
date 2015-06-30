from State import State

class Manual(State):
    
    #Local Vairables
    mNumClicks = 0
    mCounter = 0

    def __init__(self, pMain = None,  pSystemIO = None, pName = ""):
        super(Manual, self).__init__(pMain, pSystemIO, pName)
        print('Created: Manual State')

    def Start(self):
        super(Manual, self).Start()

    def Update(self, pSender):
        super(Manual, self).Update(pSender)


    def End(self):
        super(Manual, self).End()


