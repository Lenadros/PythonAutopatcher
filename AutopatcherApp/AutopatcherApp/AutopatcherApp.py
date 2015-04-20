import sys
import threading
import signal
import os
from PyQt5.QtWidgets import QApplication
from MainUI import MainUI
from StateMachine import StateMachine

#Main controll loop
class Main(threading.Thread):
    
    mStateMachine = None
    mDoState = 1
    mUIEvent = threading.Event()

    #Global Variables For Access Between States
    mBigTime = 0

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = None, daemon = None, pMainWindow = None):
        threading.Thread.__init__(self)
        self.mStateMachine = StateMachine(pMainWindow, self)
        self.mDoState = 1
    
    def run(self):
        while(self.mDoState):
            if(self.mStateMachine.Update() == 0):
                self.mDoState = 0

#Create GUI and dispaly it
mApp = QApplication(sys.argv)
mMainUIWindow = MainUI()

#Initialize main thread for state machine controlling
mMainThread = Main(None, None, None, None, None, None, mMainUIWindow)
mMainThread.start()

mMainUIWindow.SetMain(mMainThread)

sys.exit(mApp.exec_())
