from Automatic import Automatic

class AutoSquare(Automatic):

    mStep = 0

    def __init__(self, pMain = None, pSystemIO = None, pName = ""):
        super(AutoSquare, self).__init__(pMain, pSystemIO, pName)
        print('Created: AutoSquare State')

    def Start(self):
        super(AutoSquare, self).Start()

    def Update(self, pSender):
        super(AutoSquare, self).Update(pSender)
        if(mStep % 4 == 0):
            self.mSystemIO.mSerialCom.SMoveXYZRel(5000, 0, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
        elif(mStep % 4 == 1):
            self.mSystemIO.mSerialCom.SMoveXYZRel(0, 5000, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
        elif(mStep % 4 == 2):
            self.mSystemIO.mSerialCom.SMoveXYZRel(-5000, 0, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
        elif(mStep % 4 == 3):
            self.mSystemIO.mSerialCom.SMoveXYZRel(0, -5000, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
        mStep += 1

    def End(self):
        super(AutoSquare, self).End()