import sys
import threading
import signal
import os
from PyQt5.QtWidgets import QApplication
from MainUI import MainUI
from StateMachine import StateMachine
from SystemIO import SystemIO

#Main controll loop
class Main(threading.Thread):
    
    mStateMachine = None
    mSystemIO = None
    mDoState = 1
    mUIEvent = None
    mZEvent = None

    #Global Variables For Access Between States
    mBigTime = 0

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = None, daemon = None, pMainWindow = None, pSystemIO = None):
        threading.Thread.__init__(self)
        self.mStateMachine = StateMachine(pMainWindow, self, pSystemIO)
        self.mDoState = 1
        self.mUIEvent = threading.Event()
        self.mZEvent = threading.Event()
        self.mSystemIO = pSystemIO
    
    #Run state machine in main loop
    def run(self):
        self.mUIEvent.wait()
        self.mSystemIO.OpenPort()
        while(self.mDoState):
            if(self.mStateMachine.Update() == 0):
                self.mDoState = 0

#Create GUI and dispaly it
mApp = QApplication(sys.argv)
mMainUIWindow = MainUI()

#Create system IO thread 
mSystemIO = SystemIO(None, None, None, None, None, None, mMainUIWindow)
mSystemIO.start()

#Initialize main thread for state machine controlling
mMainThread = Main(None, None, None, None, None, None, mMainUIWindow, mSystemIO)
mMainThread.start()

#Pass reference of Main to the GUI thread
mMainUIWindow.SetMain(mMainThread)

sys.exit(mApp.exec_())
