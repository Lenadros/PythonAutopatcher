class State(object):
    #Local Variables
    mDummyTest = 0
    mStateName = "State"
    mMain = None
    mSystemIO = None
    mButtonSender = None

    def __init__(self, pMain = None, pSystemIO = None, pName = "State"):
        self.mStateName = pName
        self.mMain = pMain
        self.mSystemIO = pSystemIO
        print('State Initialized')

    #State Start Process
    def Start(self):
        print('State: Started')

    #Main Update for State
    def Update(self, pSender):
        self.mButtonSender = pSender

    #State End Process
    def End(self,start):
        print('State: Ended')
