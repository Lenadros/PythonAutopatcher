#SynchAIAO.py
# This is a near-verbatim translation of the example program
# C:\Users\Public\Documents\National Instruments\NI-DAQ\Examples\DAQmx ANSI C\Synchronization\Multi-Function\Synch AI-AO\SynchAI-AO.c

import ctypes
import numpy
import PyDAQmx
import matplotlib.pyplot as plt
import time
from pyqtgraph.Qt import QtCore, QtWidgets
import pyqtgraph as pg


app = QtWidgets.QApplication([])
plt = pg.plot()
curve = plt.plot()

class MyList(list):
    pass

# from pyqtgraph.examples.beeswarm import err

nidaq = ctypes.windll.nicaiu # load the DLL
##############################
# Setup some typedefs and constants
# to correspond with values in
# C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h
# the typedefs
int32 = ctypes.c_long
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong
float64 = ctypes.c_double
TaskHandle = uInt32
# the constants
DAQmx_Val_Cfg_Default = int32(-1)
DAQmx_Val_RSE = 10083
DAQmx_Val_Volts = 10348
DAQmx_Val_Rising = 10280
DAQmx_Val_GroupByChannel = 0
DAQmx_Val_ContSamps = 10123
DAQmx_Val_Acquired_Into_Buffer = 1

samplingRate = 10000
max_num_samples = 1000

totalAI = 0
##############################

# plot timer
ptr = 0
rand_data = numpy.random.normal(size=(50,5000))
def updatePlot():
    global curve, AIdata
    curve.setData(numpy.array(AIdata))
    app.processEvents()

timer = QtCore.QTimer()
timer.setInterval(200) # 200 ms interval
timer.timeout.connect(updatePlot)
timer.start(0)

AIdata = numpy.zeros((max_num_samples,), dtype=numpy.float64)

def CHK(err):
    """a simple error checking routine"""
    if err != 0:
        buf_size = 100
        buf = ctypes.create_string_buffer(b'\000' * buf_size)
        nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
        raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))

# this is a simplified version of the C function with the same name
def GetTerminalNameWithDevPrefix(device):
    triggerString = b'/' + device + b'/' + b'ai/StartTrigger'
    print(triggerString)
    return triggerString
 
def generateWvfrm(numElements, amplitude):
    AOdata = numpy.zeros((numElements,), dtype=numpy.float64)
    AOdata[1:numpy.round(numElements/2)] = amplitude
    # plotWvfrm(data)
    # plotOutput(data)
    return AOdata

def EveryNCallback_py(taskHandle, everyNsamplesEventType, nSamples, callbackData_ptr):
    callbackdata = PyDAQmx.DAQmxCallBack.get_callbackdata_from_id(callbackData_ptr)
    read = int32()
    AIdata = numpy.zeros((max_num_samples,), dtype=numpy.float64)
    CHK(nidaq.DAQmxReadAnalogF64(taskHandle,max_num_samples,float64(10.0),DAQmx_Val_GroupByChannel,AIdata.ctypes.data,max_num_samples,ctypes.byref(read),None))
    #callbackdata.extend(AIdata.tolist())
    callbackdata.clear()
    callbackdata.extend(AIdata.tolist())
    
    EveryNCallback_py.totalAI += read.value
    print('\r' + 'Acquired a total of ' + str(EveryNCallback_py.totalAI) + ' samples', end="")
    
    #plotOutput(AIdata)

    return 0 # The function should return an integer

def DoneCallback_py(taskHandle, status, callbackData_ptr):
    CHK(status) # error checking
    print("in DoneCallback_py")
    return status


def plotOutput(AIdata):
    # global curve
    global curve
    curve.setData(AIdata)
    app.processEvents()

# initialize variables
devName = b'Dev1'
aiName = b'ai0'
aoName = b'ao0'

aiChanName = devName + b'/' +aiName
aoChanName = devName + b'/' +aoName

AItaskHandle = TaskHandle(0)
AOtaskHandle = TaskHandle(0)

EveryNCallback_py.totalAI = 0;

data = numpy.zeros((max_num_samples,),dtype=numpy.float64)

try:
    
    AIdata = MyList()
    id_AIdata = PyDAQmx.DAQmxCallBack.create_callbackdata_id(AIdata)
    
    AOdata = generateWvfrm(max_num_samples, 10)
    
    # AI
    CHK(nidaq.DAQmxCreateTask("",ctypes.byref(AItaskHandle)))
    CHK(nidaq.DAQmxCreateAIVoltageChan(AItaskHandle, aiChanName,"",
                                       DAQmx_Val_Cfg_Default,
                                       float64(-10.0),float64(10.0),
                                       DAQmx_Val_Volts,None))
    CHK(nidaq.DAQmxCfgSampClkTiming(AItaskHandle,"",float64(samplingRate),
                                    DAQmx_Val_Rising,DAQmx_Val_ContSamps,
                                    uInt64(max_num_samples)));
    trigName = GetTerminalNameWithDevPrefix(devName)
    
    # AO
    CHK(nidaq.DAQmxCreateTask("",ctypes.byref(AOtaskHandle)))
    CHK(nidaq.DAQmxCreateAOVoltageChan( AOtaskHandle,
                                       aoChanName,
                                       "",
                                       float64(-10.0),
                                       float64(10.0),
                                       DAQmx_Val_Volts,
                                       None))
    CHK(nidaq.DAQmxCfgSampClkTiming( AOtaskHandle,
                                    "",
                                    float64(samplingRate),
                                    DAQmx_Val_Rising,
                                    DAQmx_Val_ContSamps,
                                    uInt64(max_num_samples)));
    
    CHK(nidaq.DAQmxCfgDigEdgeStartTrig(AOtaskHandle,
                                       trigName,
                                       DAQmx_Val_Rising))
    
    
    EveryNCallback = PyDAQmx.DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)
    DoneCallback = PyDAQmx.DAQmxDoneEventCallbackPtr(DoneCallback_py)
    
    CHK(nidaq.DAQmxRegisterEveryNSamplesEvent(AItaskHandle,DAQmx_Val_Acquired_Into_Buffer,max_num_samples,0,EveryNCallback,id_AIdata));
    CHK(nidaq.DAQmxRegisterDoneEvent(AItaskHandle,0,DoneCallback,id_AIdata));
    

    CHK(nidaq.DAQmxWriteAnalogF64( AOtaskHandle,
                                   max_num_samples,
                                   0,
                                   float64(10.0),
                                   DAQmx_Val_GroupByChannel,
                                   AOdata.ctypes.data,
                                   None,
                                   None))
    
    CHK(nidaq.DAQmxStartTask(AOtaskHandle))
    CHK(nidaq.DAQmxStartTask(AItaskHandle))
    
    print('Acquiring continuously. Press [Enter] to interrupt.')
    #input()
    

except PyDAQmx.DAQError as err:
    print('DAQmx Error: ' + err)
finally:
    if AItaskHandle:
        pass
        # CHK(nidaq.DAQmxStopTask(AItaskHandle))
        # CHK(nidaq.DAQmxClearTask(AItaskHandle))
    if AOtaskHandle:
        # CHK(nidaq.DAQmxStopTask(AOtaskHandle))
        # CHK(nidaq.DAQmxClearTask(AOtaskHandle))
        pass




if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.Qt.QtWidgets.QApplication.exec_()