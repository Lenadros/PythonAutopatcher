from State import State
from Automatic import Automatic
from Manual import Manual
#from MainUI import MainUI

class StateMachine(object):
    #State machine control variables
    mStateCounter = 0
    mStateList = []
    mCurrentState = None
    
    # START - 0
    # EXECUTE - 1
    # END -2
    mCurrentProcess = 0

    #Reference variables
    mMainUIWindow = None
    mMain = None
    mSystemIO = None

    #Class Contructor
    def __init__(self, pMainWindow = None, pMain = None, pSystemIO = None):
        self.mMainUIWindow = pMainWindow
        self.mMain = pMain
        self.mSystemIO = pSystemIO
        self.mStateCounter = 0

        self.mStateList.append(Manual(self.mMain, self.mSystemIO, "Manual State One"))
        self.mStateList.append(Automatic(self.mMain, self.mSystemIO, "Auto State One", 5000))
        self.mStateList.append(Automatic(self.mMain, self.mSystemIO, "Auto State Two", -6000))
        self.mStateList.append(Automatic(self.mMain, self.mSystemIO, "Auto State Three", 5000))

        print('StateMachine Initialized With ' + str(len(self.mStateList)) + ' States')


    #Main update for state machine
    def Update(self):
        if(self.mCurrentProcess == 0):
            if(len(self.mStateList) < self.mStateCounter + 1):
                print('StateMachine: Ended')
                self.mSystemIO.UIWriteTitle("END")
                return 0
            else:
                self.mCurrentState = self.mStateList[self.mStateCounter]
                self.mStateCounter += 1
                self.mCurrentState.Start()
                self.mCurrentProcess = 1
                return 1

        elif(self.mCurrentProcess == 1):
            pSender = None

            if(len(self.mMain.mUIQueue) != 0):
                pSender = self.mMain.mUIQueue.pop()

            if(self.mCurrentState.Update(pSender)):
                print('StateMachine: Current State Has Ended')
                self.mCurrentProcess = 2
        
        elif(self.mCurrentProcess == 2):
            self.mCurrentState.End()
            self.mCurrentProcess = 0
           




