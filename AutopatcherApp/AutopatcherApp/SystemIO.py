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
    
    #------------------------------------------------------
    # Serial Command Functions for Scientifica Manipulators
    #------------------------------------------------------

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

    def SReportPosition(self):
        self.mSerialPort.write("P\r\n");
        pMessage = self.mSerialPort.read().decode();
        print(pMessage)

    def SSetPosition(self, pX, pY, pZ):
        self.mSerialPort.write("P " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SReportXPos(self):
        self.mSerialPort.write("PX\r\n")
        pMessage = self.SerialReport.read().decode();
        return pMessage

    def SSetXPos(self, pX):
        self.mSerialPort.write("PX " + str(pX) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SReportYPos(self):
        self.mSerialPort.write("PY\r\n")
        pMessage = self.SerialReport.read().decode();
        return pMessage

    def SSetYPos(self, pY):
        self.mSerialPort.write("PY " + str(pY) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SReportZPos(self):
        self.mSerialPort.write("PZ\r\n")
        pMessage = self.SerialReport.read().decode();
        return pMessage

    def SSetZPos(self, pZ):
        self.mSerialPort.write("PZ " + str(pZ) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SZeroPos(self):
        self.mSerialPort.write("ZERO\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SMoveXYZAbs(self, pX, pY, pZ):
        self.mSerialPort.write("ABS " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SMoveXYZRel(self, pX, pY, pZ):
        self.mSerialPort.write("REL " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SVirtualJoy(self, pX, pY, pZ):
        self.mSerialPort.write("VJ " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SVirtualJoyScaled(self, pX, pY, pZ, pScale):
        self.mSerialPort.write("VJ " + str(pX) + " " + str(pY) + " " + str(pZ) + " " + pScale + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SStep(self):
        self.mSerialPort.write("STEP\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SStop(self):
        self.mSerialPort.write("STOP\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGetAccelDecel(self):
        self.mSerialPort.write("ACC\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetAccelDecel(self, pA):
        self.mSerialPort.write("ACC " + str(pA) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGetStartSpeed(self):
        self.mSerialPort.write("FIRST\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetStartSpeed(self, pS):
        self.mSerialPort.write("FIRST " + str(pS) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGetCDAccelDecel(self):
        self.mSerialPort.write("JACC\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetCDAccelDecel(self, pA):
        self.mSerialPort.write("JACC " + str(pA) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGetTopSpeed(self):
        self.mSerialPort.write("TOP\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetTopSpeed(self, pS):
        self.mSerialPort.write("TOP " + str(pS) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGoHomeInPos(self):
        self.mSerialPort.write("IN\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGetHomeInType(self):
        self.mSerialPort.write("INSET\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetHomeInType(self, pP):
        self.mSerialPort.write("INSET " + str(pP) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SSetStepSize(self, pD):
        self.mSerialPort.write("SETSTEP " + str(pD) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGoHomeOutPos(self):
        self.mSerialPort.write("OUT\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SSetHomeOutPos(self):
        self.mSerialPort.write("SET\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGetObjective(self):
        self.mSerialPort.write("OBJ\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetObjective(self, pO):
        self.mSerialPort.write("TOP " + str(pO) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGetObjChangeSpeed(self):
        self.mSerialPort.write("OBJS\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetObjChangeSpeed(self, pS):
        self.mSerialPort.write("OBJS " + str(pS) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGetObjLifeDis(self, pO):
        self.mSerialPort.write("OBJL " + str(pO) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetObjLifeDis(self, pO, pD):
        self.mSerialPort.write("OBJL " + str(pO) + " " + str(pD) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SObjUp(self, pO):
        self.mSerialPort.write("OBJU " + str(pO) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SObjDown(self, pO):
        self.mSerialPort.write("OBJD " + str(pO) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SQueryMode(self):
        self.mSerialPort.write("?\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SGetApproachAngle(self):
        self.mSerialPort.write("ANGLE\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetManAppAngle(self, pA):
        self.mSerialPort.write("ANGLE " + str(pA) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SSetAutoAppAngle(self):
        self.mSerialPort.write("ANGLE A\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    def SGetApproachOO(self):
        self.mSerialPort.write("APPROACH\r\n")
        pMessage = self.mSerialPort.read().decode();
        return pMessage

    def SSetApproachOO(self, pO):
        self.mSerialPort.write("APPROACH " + str(pO) + "\r\n")
        pMessage = self.mSerialPort.read().decode();
        if(pMessage == "A"):
            return 1
        return 0

    #----------------------------------------------
    # Bridge Functions Between UI and State Machine
    #----------------------------------------------
    def UIWriteTitle(self, pString):
        self.mMainWindow.WriteTitle(pString)

