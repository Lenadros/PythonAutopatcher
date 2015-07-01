from Automatic import Automatic

class AutoSquare(Automatic):

    mStep = 0

    def __init__(self, pMain = None, pSystemIO = None, pName = ""):
        super(AutoSquare, self).__init__(pMain, pSystemIO, pName)
        print('Created: AutoSquare State')

    def Start(self):
        super(AutoSquare, self).Start()
        self.mSystemIO.UIWriteTitle(self.mStateName)
        self.mSystemIO.mSerialCom.mMovementEvent.clear()
        self.mSystemIO.mSerialCom2.mMovementEvent.clear()

    def Update(self, pSender):
        super(AutoSquare, self).Update(pSender)
        if(self.mStep % 4 == 0):
            print "Step One Move"
            self.mSystemIO.mSerialCom.SMoveXYZRel(50000, 0, 0)
            self.mSystemIO.mSerialCom2.SMoveXYZRel(50000, 0, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
            self.mSystemIO.mSerialCom2.mMovementEvent.wait()
            self.mSystemIO.mSerialCom.mMovementEvent.clear()
            self.mSystemIO.mSerialCom2.mMovementEvent.clear()
            print "First Step Done"
        elif(self.mStep % 4 == 1):
            print "Step Two Move"
            self.mSystemIO.mSerialCom.SMoveXYZRel(0, 50000, 0)
            self.mSystemIO.mSerialCom2.SMoveXYZRel(0, 50000, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
            self.mSystemIO.mSerialCom2.mMovementEvent.wait()
            self.mSystemIO.mSerialCom.mMovementEvent.clear()
            self.mSystemIO.mSerialCom2.mMovementEvent.clear()
            print "Second Step Done"
        elif(self.mStep % 4 == 2):
            print "Step Three Move"
            self.mSystemIO.mSerialCom.SMoveXYZRel(-50000, 0, 0)
            self.mSystemIO.mSerialCom2.SMoveXYZRel(-50000, 0, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
            self.mSystemIO.mSerialCom2.mMovementEvent.wait()
            self.mSystemIO.mSerialCom.mMovementEvent.clear()
            self.mSystemIO.mSerialCom2.mMovementEvent.clear()
            print "Third Step Done"
        elif(self.mStep % 4 == 3):
            print "Step Four Move"
            self.mSystemIO.mSerialCom.SMoveXYZRel(0, -50000, 0)
            self.mSystemIO.mSerialCom2.SMoveXYZRel(0, -50000, 0)
            self.mSystemIO.mSerialCom.mMovementEvent.wait()
            self.mSystemIO.mSerialCom2.mMovementEvent.wait()
            self.mSystemIO.mSerialCom.mMovementEvent.clear()
            self.mSystemIO.mSerialCom2.mMovementEvent.clear()
            print "Fourth Step Done"
        self.mStep += 1

        if(self.mButtonSender != None and self.mButtonSender.text() == "Stop"):
            return False

        return True

    def End(self):
        super(AutoSquare, self).End()