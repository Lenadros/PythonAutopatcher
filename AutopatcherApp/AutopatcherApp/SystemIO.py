import threading
import serial


class SystemIO(threading.Thread):

    mSerialPort = None
    mMainWindow = None

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = None, daemon = None, pMainWindow = None):
        threading.Thread.__init__(self)
        self.mMainWindow = pMainWindow
        self.FindAvaliblePorts()
    
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
        self.mSerialPort = serial.Serial(self.mMainWindow.GetSelectedComPort())
        print(self.mMainWindow.GetSelectedComPort() + " is opened")

    def SerialWrite(self, pCommand):
        pCommand = pCommand + "\r\n"
        print(pCommand)
        self.mSerialPort.write(bytes(pCommand, 'UTF-8'))

    def SerialReport(self):
        self.mSerialPort.write(b"S\r\n")
        return self.mSerialPort.read().decode()

