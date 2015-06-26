import os
import threading
import time
import serial

class SerialCom(threading.Thread):
    
    mSystemIO = None
    mSerialPort = None
    bMovementInit = False
    mMovementEvent = threading.Event()
    mCurrentPos = None
    mPrevPos = None

    def __init__(self, pSystemIO = None):
        threading.Thread.__init__(self)
        self.mSystemIO = pSystemIO
        self.FindAvaliblePorts()

    def run(self):
        while(1):
            if(self.bMovementInit == True and self.mSerialPort != None):
                self.mCurrentPos = self.SReportPosition()
                self.mSystemIO.UIWritePosition(self.mCurrentPos)
                if(self.mCurrentPos != None and self.mPrevPos != None and self.mCurrentPos == self.mPrevPos):
                    self.mMovementEvent.set()
                    self.mMovementEvent.clear()
                    self.bMovementInit = False
                    #self.mCurrentPos = None
                    #self.mPrevPos = None
                self.mPrevPos = self.mCurrentPos
                #time.sleep(0.05)

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

        self.mSystemIO.UIFillComList(PortList)

    #Open the user selected port
    def OpenPort(self):
        Port = self.mSystemIO.UIFillComList()
        self.mSerialPort = serial.Serial(port = int(Port) - 1, baudrate = 9600, writeTimeout = 0)
        print("COM" + Port + " is opened")
    
    #------------------------------
    # Scientifica Command Functions
    #------------------------------
    def SReportPosition(self):
        self.mSerialPort.write("P\r\n");
        pPosition = self.SReadSerialMessage()
        return self.SDecodeXYZ(pPosition + '\r')

    def SSetPosition(self, pX, pY, pZ):
        self.mSerialPort.write("P " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetXPos(self, pX):
        self.mSerialPort.write("PX " + str(pX) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetYPos(self, pY):
        self.mSerialPort.write("PY " + str(pY) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetZPos(self, pZ):
        self.mSerialPort.write("PZ " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SZeroPos(self):
        self.mSerialPort.write("ZERO\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SMoveXYZAbs(self, pX, pY, pZ):
        self.bMovementInit = True
        self.mSerialPort.write("ABS " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            self.bMovementInit = True
            return True
        return False

    def SMoveXYZRel(self, pX, pY, pZ):
        self.mSerialPort.write("REL " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            self.bMovementInit = True
            return True
        return False

    def SVirtualJoy(self, pX, pY, pZ):
        self.mSerialPort.write("VJ " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SVirtualJoyScaled(self, pX, pY, pZ, pScale):
        self.mSerialPort.write("VJ " + str(pX) + " " + str(pY) + " " + str(pZ) + " " + pScale + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SStep(self):
        self.mSerialPort.write("STEP\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SStop(self):
        self.mSerialPort.write("STOP\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetAccelDecel(self):
        self.mSerialPort.write("ACC\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetAccelDecel(self, pA):
        self.mSerialPort.write("ACC " + str(pA) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetStartSpeed(self):
        self.mSerialPort.write("FIRST\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetStartSpeed(self, pS):
        self.mSerialPort.write("FIRST " + str(pS) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetCDAccelDecel(self):
        self.mSerialPort.write("JACC\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetCDAccelDecel(self, pA):
        self.mSerialPort.write("JACC " + str(pA) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetTopSpeed(self):
        self.mSerialPort.write("TOP\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetTopSpeed(self, pS):
        self.mSerialPort.write("TOP " + str(pS) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGoHomeInPos(self):
        self.mSerialPort.write("IN\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetHomeInType(self):
        self.mSerialPort.write("INSET\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetHomeInType(self, pP):
        self.mSerialPort.write("INSET " + str(pP) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetStepSize(self, pD):
        self.mSerialPort.write("SETSTEP " + str(pD) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGoHomeOutPos(self):
        self.mSerialPort.write("OUT\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetHomeOutPos(self):
        self.mSerialPort.write("SET\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetObjective(self):
        self.mSerialPort.write("OBJ\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetObjective(self, pO):
        self.mSerialPort.write("TOP " + str(pO) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetObjChangeSpeed(self):
        self.mSerialPort.write("OBJS\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetObjChangeSpeed(self, pS):
        self.mSerialPort.write("OBJS " + str(pS) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetObjLifeDis(self, pO):
        self.mSerialPort.write("OBJL " + str(pO) + "\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetObjLifeDis(self, pO, pD):
        self.mSerialPort.write("OBJL " + str(pO) + " " + str(pD) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SObjUp(self, pO):
        self.mSerialPort.write("OBJU " + str(pO) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SObjDown(self, pO):
        self.mSerialPort.write("OBJD " + str(pO) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SQueryMode(self):
        self.mSerialPort.write("?\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SGetApproachAngle(self):
        self.mSerialPort.write("ANGLE\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetManAppAngle(self, pA):
        self.mSerialPort.write("ANGLE " + str(pA) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetAutoAppAngle(self):
        self.mSerialPort.write("ANGLE A\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetApproachOO(self):
        self.mSerialPort.write("APPROACH\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetApproachOO(self, pO):
        self.mSerialPort.write("APPROACH " + str(pO) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SReadSerialMessage(self):
        pMessage = ""
        pChar = self.mSerialPort.read()
        while(pChar != "\r"):
             pMessage += pChar
             pChar = self.mSerialPort.read().decode()
        return pMessage

    #Decode recieved serial message into a XYZ array
    def SDecodeXYZ(self, pString):
        pXYZ = [0,0,0]
        pNum = ""
        i = 0

        try:
            pChar = pString[0]
            while(pChar != '\r'):
                pString = pString[1:]
                pNum += pChar
                pChar = pString[0]
                if(pChar == '\t' or pChar == '\r'):
                    pXYZ[i] = int(pNum)
                    i += 1
                    pString = pString[1:]
                    pNum = ""
        except Exception:
            return None
            pass

        print pXYZ
        return pXYZ