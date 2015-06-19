import os
import threading
import time
import serial

class SerialCom(threading.Thread):
    
    mMainWindow = None
    mSerialPort = None
    bMovementInit = False
    mMovementEvent = threading.Event()
    mCurrentPos = None
    mPrevPos = None

    def __init__(self, pMainWindow = None):
        threading.Thread.__init__(self)
        self.mMainWindow = pMainWindow
        self.FindAvaliblePorts()

    def run(self):
        while(1):
            if(self.bMovementInit == True and self.mSerialPort != None):
                self.mCurrentPos = self.SReportPosition()
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

        self.mMainWindow.FillComPortList(PortList)

    #Open the user selected port
    def OpenPort(self):
        Port = self.mMainWindow.GetSelectedComPort()[3:]
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
        pMessage = self.mSerialPort.read().decode()
        if(pMessage == "A"):
            return 1
        return 0

    def SSetXPos(self, pX):
        self.mSerialPort.write("PX " + str(pX) + "\r\n")
        pMessage = self.mSerialPort.read().decode()
        if(pMessage == "A"):
            return 1
        return 0

    def SSetYPos(self, pY):
        self.mSerialPort.write("PY " + str(pY) + "\r\n")
        pMessage = self.mSerialPort.read().decode()
        if(pMessage == "A"):
            return 1
        return 0

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
        self.bMovementInit = True
        self.mSerialPort.write("ABS " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return 1
        return 0

    def SMoveXYZRel(self, pX, pY, pZ):
        self.mSerialPort.write("REL " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        print pPass
        if(pPass == "A"):
            print "Message Passed. Proceeding with Movement..."
            time.sleep(0.2)
            self.bMovementInit = True
            return True
        return False

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

    def SReportStatus(self):
        self.mSerialPort.write("S\r\n")
        pMessage = self.mSerialPort.read().decode();
        print pMessage
        return pMessage

    def SReadSerialMessage():
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