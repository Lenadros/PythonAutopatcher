import os
import threading
import time
import serial
from SerialCom import SerialCom

class SystemIO(threading.Thread):

    #Serial communcation variables
    mComThread = None
    mComThread2 = None
    mPort = None
    mPort2 = None
    mMoveEvent = None
    mMoveEvent2 = None

    mMainWindow = None

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = None, daemon = None, pMainWindow = None):
        threading.Thread.__init__(self)
        self.mMainWindow = pMainWindow
        self.FindAvaliblePorts()
        self.mMoveEvent = threading.Event();
        self.mMoveEvent2 = threading.Event();

    #Main System IO Update Loop
    def run(self):
        while(1):
            x = 1

    #----------------------------------------------
    # Serial Port Functions
    #----------------------------------------------

    #List avalible ports on the computer
    def FindAvaliblePorts(self):
        AllPorts = ['COM' + str(i + 1) for i in range(256)]
        PortList = []
        for Port in AllPorts:
            try:
                mPort = serial.Serial(Port)
                mPort.close()
                PortList.append(Port)
            except(OSError, serial.SerialException):
                pass

        self.UIFillComList(PortList)

    #Open the user selected port
    def OpenPorts(self):
        Port = self.UIGetComPort(0)
        Port2 = self.UIGetComPort(1)
        self.mPort = serial.Serial(port = int(Port) - 1, baudrate = 9600, writeTimeout = 0)
        self.mPort2 = serial.Serial(port = int(Port2) - 1, baudrate = 9600, writeTimeout = 0)
        print("COM" + Port + " is opened")
        self.mComThread = SerialCom(self, self.mPort, self.mMoveEvent, self.mLock)
        self.mComThread2 = SerialCom(self, self.mPort2, self.mMoveEvent2, self.mLock)
        self.mComThread.start()
        self.mComThread2.start()


    #----------------------------------------------
    # Bridge Functions Between UI and State Machine
    #----------------------------------------------
    def UIWriteTitle(self, pString):
        self.mMainWindow.WriteTitle(pString)

    def UIFillComList(self, pPortList):
        self.mMainWindow.FillComPortList(pPortList)

    def UIGetComPort(self, pBox):
        return self.mMainWindow.GetSelectedComPort(pBox)[3:]

    def UIWritePosition(self, pPosition):
        self.mMainWindow.WriteData("X:" + str(pPosition[0]) + " Y:" + str(pPosition[1]) + " Z:" + str(pPosition[2]))

