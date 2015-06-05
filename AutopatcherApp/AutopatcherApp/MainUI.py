import sys
import signal
import os
from StateMachine import StateMachine
from PyQt4 import QtCore, QtGui, uic

class MainUI(QtGui.QMainWindow):

    mMain = None

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi('D:\Autopatcher Python\PythonAutopatcher\MainUI.ui',self)
        self.show()
        self.ui.pushButton.clicked.connect(self.OnNextButtonClicked)
        self.ui.pushButton_2.clicked.connect(self.OnZButtonClicked)


    #----------------------------------------------------------
    # UI Functions - Probably will be replaed as the UI changes
    #----------------------------------------------------------
    def SetMain(self, pMain = None):
        self.mMain = pMain

    def OnNextButtonClicked(self):
        self.mMain.mUIEvent.set()
        self.mMain.mUIEvent.clear()

    def OnZButtonClicked(self):
        self.mMain.mZEvent.set()
        self.mMain.mZEvent.clear()

    def DisplayCurrentState(self, pStateName):
        self.ui.label.setText(pStateName)

    def DisplayData(self, isTime, pData):
        if(isTime):
            self.ui.label_2.setText(str(int(pData)) + " Second(s)")
        else:
            self.ui.label_2.setText(str(int(pData)) + " Click(s)")

    def SendMessage(self, pMessage):
        self.ui.label_3.setText(pMessage)

    def FillComPortList(self, pPorts):
        for port in pPorts:
            self.ui.comboBox.addItem(str(port))

    def GetSelectedComPort(self):
        return self.ui.comboBox.currentText()


