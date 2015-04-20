from State import State
from Automatic import Automatic
from Manual import Manual
#from MainUI import MainUI
from enum import Enum


class Process(Enum):
    START = 1;
    EXECUTE = 2;
    END = 3;

class StateMachine(object):
    #State machine control variables
    mStateCounter = 0
    mStateList = []
    mCurrentState = None
    mCurrentProcess = None

    #Reference variables
    mMainUIWindow = None
    mMain = None

    #Class Contructor
    def __init__(self, pMainWindow = None, pMain = None):
        self.mMainUIWindow = pMainWindow
        self.mMain = pMain
        self.mCurrentProcess = Process.START
        self.mStateCounter = 0

        self.mStateList.append(Automatic(self.mMainUIWindow, self.mMain, "Auto State One", 4))
        self.mStateList.append(Manual(self.mMainUIWindow, self.mMain, "Manual State One"))
        self.mStateList.append(Automatic(self.mMainUIWindow, self.mMain, "Auto State Two", 2))
        self.mStateList.append(Manual(self.mMainUIWindow, self.mMain, "Manual State Two"))
        self.mStateList.append(Automatic(self.mMainUIWindow, self.mMain, "Auto State Three", 3))
        self.mStateList.append(Manual(self.mMainUIWindow, self.mMain, "Manual State Three"))

        print('StateMachine Initialized With ' + str(len(self.mStateList)) + ' States')


    #Main update for state machine
    def Update(self):
        if(self.mCurrentProcess == Process.START):
            if(len(self.mStateList) < self.mStateCounter + 1):
                print('StateMachine: Ended')
                self.mMainUIWindow.DisplayCurrentState("END")
                return 0
            else:
                self.mCurrentState = self.mStateList[self.mStateCounter]
                self.mStateCounter += 1
                self.mCurrentState.Start()
                self.mMainUIWindow.DisplayCurrentState(self.mCurrentState.mStateName)
                self.mCurrentProcess = Process.EXECUTE
                return 1

        elif(self.mCurrentProcess == Process.EXECUTE):
            if(self.mCurrentState.Update()):
                print('StateMachine: Current State Has Ended')
                self.mCurrentProcess = Process.END
        
        elif(self.mCurrentProcess == Process.END):
            self.mCurrentState.End()
            self.mCurrentProcess = Process.START
           




