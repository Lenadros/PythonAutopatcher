import os
import threading
import serial
from PyDAQmx import *
import numpy
#import cv2
import ctypes

class SystemIO(threading.Thread):

    mSerialPort = None
    mMainWindow = None
    CameraDLL = None

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = None, daemon = None, pMainWindow = None):
        threading.Thread.__init__(self)
        self.mMainWindow = pMainWindow
        self.FindAvaliblePorts()

    def run(self):
        while(1):
            x = 1
    
    #List avalible ports on the computer
    def FindAvaliblePorts(self):
        AllPorts = ['COM' + str(i + 1) for i in range(256)]
        PortList = []
        for Port in AllPorts:
            try:
                mSerialPort = serial.Serial(Port)
                mSerialPort.close()
                PortList.append(Port)
            except(OSError, serial.SerialException):
                pass

        self.mMainWindow.FillComPortList(PortList)

    #Open GUI selected port
    def OpenPort(self):
        Port = self.mMainWindow.GetSelectedComPort()[3:]
        self.mSerialPort = serial.Serial(int(Port) - 1)
        print(Port + " is opened")

    def SerialWrite(self, pCommand):
        pCommand = pCommand + "\r\n"
        print(pCommand)
        self.mSerialPort.write(pCommand)

    def SerialReport(self):
        self.mSerialPort.write(b"S\r\n")
        return self.mSerialPort.read().decode()

    #----------------------------------------------
    # Bridge Functions Between UI and State Machine
    #----------------------------------------------
    def UIWriteTitle(self, pString):
        self.mMainWindow.WriteTitle(pString)

