class State(object):
    #Local Variables
    mDummyTest = 0
    mStateName = "State"
    mMainUIWindow = None
    mMain = None

    def __init__(self, pMainWindow, pMain, pName):
        self.mStateName = pName
        self.mMainUIWindow = pMainWindow
        self.mMain = pMain
        print('State Initialized')

    #State Start Process
    def Start(self):
        print('State: Started')

    #Main Update for State
    def Update(self):
        self.mDummyTest = 1

    #State End Process
    def End(start):
        print('State: Ended')
