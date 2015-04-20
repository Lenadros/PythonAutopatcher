import sys
import signal
import os
from StateMachine import StateMachine
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class MainUI(QMainWindow):

    mMain = None

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi('D:\Autopatcher Python\MainUI.ui',self)
        self.show()
        self.ui.pushButton.clicked.connect(self.OnNextButtonClicked)

    def SetMain(self, pMain = None):
        self.mMain = pMain

    def OnNextButtonClicked(self):
        self.mMain.mUIEvent.set()
        self.mMain.mUIEvent.clear()

    def DisplayCurrentState(self, pStateName):
        self.ui.label.setText(pStateName)

    def DisplayData(self, isTime, pData):
        if(isTime):
            self.ui.label_2.setText(str(int(pData)) + " Second(s)")
        else:
            self.ui.label_2.setText(str(int(pData)) + " Click(s)")

    def SendMessage(self, pMessage):
        self.ui.label_3.setText(pMessage)


