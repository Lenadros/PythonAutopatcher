import os
import threading
import time
from SerialCom import SerialCom

class SystemIO(threading.Thread):

    mSerialCom = None
    mMainWindow = None

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = None, daemon = None, pMainWindow = None):
        threading.Thread.__init__(self)
        self.mMainWindow = pMainWindow
        self.mSerialCom = SerialCom(self)
        self.mSerialCom.start()

    #Main System IO Update Loop
    def run(self):
        while(1):
            x = 1

    #----------------------------------------------
    # Bridge Functions Between UI and State Machine
    #----------------------------------------------
    def UIWriteTitle(self, pString):
        self.mMainWindow.WriteTitle(pString)

    def UIFillComList(self, pPortList):
        self.mMainWindow.FillComPortList(pPortList)

    def UIGetComPort(self):
        return self.mMainWindow.GetSelectedComPort()[3:]

    def UIWritePosition(self, pPosition):
        self.mMainWindow.WriteData("X:" + str(pPosition[0]) + " Y:" + str(pPosition[1]) + " Z:" + str(pPosition[2]))

