from State import State
import time

class Automatic(State):
    
    #Local Vairables
    mStartTime = 0
    mEndTime = 0
    mElapsedTime = 0
    mSetTime = 0

    def __init__(self, pMain = None, pSystemIO = None, pName = "", pSetTime = 1):
        super(Automatic, self).__init__(pMain, pSystemIO, pName)
        self.mStartTime = 0
        self.mEndTime = 0
        self.mElapsedTime = 0
        self.mSetTime = pSetTime
        print('Created: Automatic State')

    def Start(self):
        super(Automatic, self).Start()
        #self.mSystemIO.SerialWrite("RELZ " + str(self.mSetTime))
        #Start local timer
        self.mSystemIO.UIWriteTitle(self.mStateName)
        self.mStartTime = time.time()
        #self.mMainUIWindow.SendMessage("Please Wait " + str(self.mSetTime) + " Second(s)")

    def Update(self, pSender):
        super(Automatic, self).Update(pSender)
        #Update timer
        self.mEndTime = time.time()
        self.mElapsedTime = self.mEndTime - self.mStartTime
        #self.mMainUIWindow.DisplayData(1, self.mElapsedTime)
        
        #If timer has reached the required time, return 1
        if(self.mElapsedTime >= 2):
           # if(self.mSystemIO.SerialReport() == "0"):
                #self.mMainUIWindow.SendMessage("Manipulator Movement Complete!")
                return 1
            #else:
             #    self.mMainUIWindow.SendMessage("Moving Manipulator...")
            #return 1

        return 0

    def End(self):
        super(Automatic, self).End()
        #Set global variable to be read by other states
        #self.mMain.mBigTime = self.mSetTime



