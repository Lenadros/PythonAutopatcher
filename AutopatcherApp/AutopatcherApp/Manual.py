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
        self.mSystemIO.UIWriteTitle(self.mStateName)

    def Update(self, pSender):
        super(Manual, self).Update(pSender)

        #Wait for event from UI
        if(self.mButtonSender != None):
            if(self.mButtonSender.text() == "Move Z"):
                print "Input Recieved. Now Moving"
                self.mSystemIO.SMoveXYZRel(0,0,-30000)
                self.mSystemIO.mMovementEvent.wait()
                print "Done Moving"

            if(self.mButtonSender.text() == "End Manual"):
                print "Manual State Forcefully Ended"
                return True

        return False

    def End(self):
        super(Manual, self).End()


