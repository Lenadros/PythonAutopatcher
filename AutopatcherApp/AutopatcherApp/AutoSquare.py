from Automatic import Automatic

class AutoSquare(Automatic):

    mStep = 0

    def __init__(self, pMain = None, pSystemIO = None, pName = ""):
        super(AutoSquare, self).__init__(pMain, pSystemIO, pName)
        print('Created: AutoSquare State')

    def Start(self):
        super(AutoSquare, self).Start()
        self.mSystemIO.UIWriteTitle(self.mStateName)

    def Update(self, pSender):
        super(AutoSquare, self).Update(pSender)
        if(self.mStep % 4 == 0):
            self.mSystemIO.mSerialCom.SMoveXYZRel(50000, 0, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
        elif(self.mStep % 4 == 1):
            self.mSystemIO.mSerialCom.SMoveXYZRel(0, 50000, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
        elif(self.mStep % 4 == 2):
            self.mSystemIO.mSerialCom.SMoveXYZRel(-50000, 0, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
        elif(self.mStep % 4 == 3):
            self.mSystemIO.mSerialCom.SMoveXYZRel(0, -50000, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
        self.mStep += 1

        if(self.mButtonSender != None and self.mButtonSender.text() == "Stop"):
            return False

        return True

    def End(self):
        super(AutoSquare, self).End()