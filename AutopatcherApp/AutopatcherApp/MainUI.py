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
        #self.ui = uic.loadUi('C:\Users\Leonard\Documents\PythonAutopatcher\MainUI.ui',self)
        self.show()
        self.ui.pushButton.clicked.connect(self.OnButtonClicked)
        self.ui.pushButton_2.clicked.connect(self.OnButtonClicked)
        self.ui.pushButton_3.clicked.connect(self.OnButtonClicked)


    #----------------------------------------------------------
    # UI Functions - Probably will be replaed as the UI changes
    #----------------------------------------------------------
    def SetMain(self, pMain = None):
        self.mMain = pMain

    def OnButtonClicked(self):
        self.mMain.mUIQueue.append(self.sender())

    def WriteTitle(self, pString):
        self.ui.label.setText(pString)

    def WriteData(self, pString):
        self.ui.label_2.setText(pString)

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
            self.ui.comboBox_2.addItem(str(port))

    def GetSelectedComPort(self, pBox):
        if(pBox == 0):
            return self.ui.comboBox.currentText()
        elif(pBox == 1):
            return self.ui.comboBox_2.currentText()


