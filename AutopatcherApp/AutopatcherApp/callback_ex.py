import PyDAQmx
from numpy import zeros
import ctypes

# Class of the data object
# one cannot create a weakref to a list directly
# but the following works well
class MyList(list):
    pass

# list where the data are stored
data = MyList()
id_data = PyDAQmx.DAQmxCallBack.create_callbackdata_id(data)
int32 = ctypes.c_long

def EveryNCallback_py(taskHandle, everyNsamplesEventType, nSamples, callbackData_ptr):
    callbackdata = PyDAQmx.DAQmxCallBack.get_callbackdata_from_id(callbackData_ptr)
    read = int32()
    data = zeros(1000)
    PyDAQmx.DAQmxReadAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByScanNumber,data,1000,ctypes.byref(read),None)
    callbackdata.extend(data.tolist())
    print "Acquired total %d samples"%len(data)
    return 0 # The function should return an integer

# Convert the python function to a C function callback
EveryNCallback = DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)

DAQmxRegisterEveryNSamplesEvent(taskHandle,DAQmx_Val_Acquired_Into_Buffer,1000,0,EveryNCallback,id_data)

