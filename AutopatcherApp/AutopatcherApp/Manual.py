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
        #Determine how many times the user must click from global varaible BigTime
        self.mSystemIO.UIWriteTitle(self.mStateName)

    def Update(self, pSender):
        super(Manual, self).Update(pSender)

        #Wait for event from UI
        if(self.mButtonSender != None):
            if(self.mButtonSender.text() == "Move Z"):
                print "Input Recieved"
                self.mSystemIO.SMoveXYZRel(0,0,-5000)

            if(self.mButtonSender.text() == "End Manual"):
                print "Manual State Forcefully Ended"
                return 1

        #If the user has clicked the right amount of times, return 1
        #if(self.mCounter == self.mNumClicks):
        #    return 1

        return 0

    def End(self):
        super(Manual, self).End()


