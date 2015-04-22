from State import State

class Manual(State):
    
    #Local Vairables
    mNumClicks = 0
    mCounter = 0

    def __init__(self, pMainWindow = None, pMain = None, pName = "", pSystemIO = None):
        super().__init__(pMainWindow, pMain, pName, pSystemIO)
        print('Created: Manual State')

    def Start(self):
        super().Start()
        #Determine how many times the user must click from global varaible BigTime
        self.mNumClicks = self.mMain.mBigTime
        self.mMainUIWindow.SendMessage("Press 'Next' " + str(self.mNumClicks) + ' Time(s) to Contine')
        self.mMainUIWindow.DisplayData(0, self.mCounter)

    def Update(self):
        super().Update()

        #Wait for event from UI
        print('ManualState: Waiting for button press')
        self.mMain.mZEvent.wait()
        self.mSystemIO.MoveZ()
        print('ManualState: Got button press')
        self.mCounter += 1
        self.mMainUIWindow.DisplayData(0, self.mCounter)

        #If the user has clicked the right amount of times, return 1
        if(self.mCounter == self.mNumClicks):
            return 1

        return 0

    def End(self):
        super().End()


