import os
import threading
import time
import serial

class SerialCom(threading.Thread):
    
    mSystemIO = None
    mSerialPort = None
    bMovementInit = False
    mMovementEvent = None
    mCurrentPos = None
    mPrevPos = None

    def __init__(self, pSystemIO = None, pSerialPort = None, pEvent = None):
        threading.Thread.__init__(self)
        self.mSystemIO = pSystemIO
        self.mSerialPort = pSerialPort
        self.mMovementEvent = pEvent

    def run(self):
        while(1):
            if(self.bMovementInit == True and self.mSerialPort != None):
                self.mCurrentPos = self.SReportPosition()
                #self.mSystemIO.UIWritePosition(self.mCurrentPos)
                if(self.mCurrentPos != None and self.mPrevPos != None and self.mCurrentPos == self.mPrevPos):
                    self.mMovementEvent.set()
                    self.bMovementInit = False
                self.mPrevPos = self.mCurrentPos
    
    #------------------------------
    # Scientifica Command Functions
    #------------------------------
    def SReportPosition(self):
        self.SSendSerialMessage("P\r\n");
        pPosition = self.SReadSerialMessage()
        return self.SDecodeXYZ(pPosition + '\r')

    def SSetPosition(self, pX, pY, pZ):
        self.SSendSerialMessage("P " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetXPos(self, pX):
        self.SSendSerialMessage("PX " + str(pX) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetYPos(self, pY):
        self.SSendSerialMessage("PY " + str(pY) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetZPos(self, pZ):
        self.SSendSerialMessage("PZ " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SZeroPos(self):
        self.SSendSerialMessage("ZERO\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SMoveXYZAbs(self, pX, pY, pZ):
        self.bMovementInit = True
        self.SSendSerialMessage("ABS " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            self.bMovementInit = True
            return True
        return False

    def SMoveXYZRel(self, pX, pY, pZ):
        self.SSendSerialMessage("REL " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            self.bMovementInit = True
            return True
        return False

    def SVirtualJoy(self, pX, pY, pZ):
        self.SSendSerialMessage("VJ " + str(pX) + " " + str(pY) + " " + str(pZ) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SVirtualJoyScaled(self, pX, pY, pZ, pScale):
        self.SSendSerialMessage("VJ " + str(pX) + " " + str(pY) + " " + str(pZ) + " " + pScale + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SStep(self):
        self.SSendSerialMessage("STEP\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SStop(self):
        self.SSendSerialMessage("STOP\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetAccelDecel(self):
        self.SSendSerialMessage("ACC\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetAccelDecel(self, pA):
        self.SSendSerialMessage("ACC " + str(pA) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetStartSpeed(self):
        self.SSendSerialMessage("FIRST\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetStartSpeed(self, pS):
        self.SSendSerialMessage("FIRST " + str(pS) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetCDAccelDecel(self):
        self.SSendSerialMessage("JACC\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetCDAccelDecel(self, pA):
        self.SSendSerialMessage("JACC " + str(pA) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetTopSpeed(self):
        self.SSendSerialMessage("TOP\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetTopSpeed(self, pS):
        self.SSendSerialMessage("TOP " + str(pS) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGoHomeInPos(self):
        self.SSendSerialMessage("IN\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetHomeInType(self):
        self.SSendSerialMessage("INSET\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetHomeInType(self, pP):
        self.SSendSerialMessage("INSET " + str(pP) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetStepSize(self, pD):
        self.SSendSerialMessage("SETSTEP " + str(pD) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGoHomeOutPos(self):
        self.SSendSerialMessage("OUT\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetHomeOutPos(self):
        self.SSendSerialMessage("SET\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetObjective(self):
        self.SSendSerialMessage("OBJ\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetObjective(self, pO):
        self.SSendSerialMessage("TOP " + str(pO) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetObjChangeSpeed(self):
        self.SSendSerialMessage("OBJS\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetObjChangeSpeed(self, pS):
        self.SSendSerialMessage("OBJS " + str(pS) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetObjLifeDis(self, pO):
        self.SSendSerialMessage("OBJL " + str(pO) + "\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetObjLifeDis(self, pO, pD):
        self.SSendSerialMessage("OBJL " + str(pO) + " " + str(pD) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SObjUp(self, pO):
        self.SSendSerialMessage("OBJU " + str(pO) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SObjDown(self, pO):
        self.SSendSerialMessage("OBJD " + str(pO) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SQueryMode(self):
        self.SSendSerialMessage("?\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SGetApproachAngle(self):
        self.SSendSerialMessage("ANGLE\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetManAppAngle(self, pA):
        self.SSendSerialMessage("ANGLE " + str(pA) + "\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SSetAutoAppAngle(self):
        self.SSendSerialMessage("ANGLE A\r\n")
        pPass = self.SReadSerialMessage()
        if(pPass == "A"):
            return True
        return False

    def SGetApproachOO(self):
        self.SSendSerialMessage("APPROACH\r\n")
        pMessage = self.SReadSerialMessage()
        return pMessage

    def SSetApproachOO(self, pO):
        self.SSendSerialMessage("APPROACH " + str(pO) + "\r\n")
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

    def SSendSerialMessage(self, pMessage):
        self.mSerialPort.write(pMessage)

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

        #print pXYZ
        return pXYZ