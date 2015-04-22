from State import State
import time

class Automatic(State):
    
    #Local Vairables
    mStartTime = 0
    mEndTime = 0
    mElapsedTime = 0
    mSetTime = 0

    def __init__(self, pMainWindow = None, pMain = None, pName = "", pSetTime = 1):
        super().__init__(pMainWindow, pMain, pName)
        self.mStartTime = 0
        self.mEndTime = 0
        self.mElapsedTime = 0
        self.mSetTime = pSetTime
        print('Created: Automatic State')

    def Start(self):
        super().Start()
        #Start local timer
        self.mStartTime = time.time()
        self.mMainUIWindow.SendMessage("Please Wait " + str(self.mSetTime) + " Second(s)")

    def Update(self):
        super().Update()
        #Update timer
        self.mEndTime = time.time()
        self.mElapsedTime = self.mEndTime - self.mStartTime
        self.mMainUIWindow.DisplayData(1, self.mElapsedTime)
        
        #If timer has reached the required time, return 1
        if(self.mElapsedTime >= self.mSetTime):
            return 1

        return 0

    def End(self):
        super().End()
        #Set global variable to be read by other states
        self.mMain.mBigTime = self.mSetTime



