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
        self.mSerialCom = SerialCom()
        self.mSerialCom.start()

    #Main System IO Update Loop
    def run(self):
        x = 1

    #----------------------------------------------
    # Bridge Functions Between UI and State Machine
    #----------------------------------------------
    def UIWriteTitle(self, pString):
        self.mMainWindow.WriteTitle(pString)

