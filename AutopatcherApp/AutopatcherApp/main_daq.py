import sys

from PyQt5.QtWidgets import QDialog,QPushButton,QVBoxLayout, QApplication
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random

# imports for DAQ
import ctypes
import numpy
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
DAQmx_Val_FiniteSamps = 10178
DAQmx_Val_GroupByChannel = 0
##############################


class main_daq(QDialog):
    def __init__(self, parent=None):
        super(main_daq, self).__init__(parent)
        
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def CHK(self,err):
        """a simple error checking routine"""
        if err < 0:
            buf_size = 100
            #buf = ctypes.create_string_buffer('\000' * buf_size)
            buf = ctypes.create_string_buffer(b'\000' * buf_size)
            nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))


    def plot(self):
        ''' plot some random stuff '''
        # random data
        #data = [random.random() for i in range(10)]
        # initialize variables
        
        # DAQ ACCESS
        taskHandle = TaskHandle(0)
        max_num_samples = 1000
        data = numpy.zeros((max_num_samples,),dtype=numpy.float64)
        # now, on with the program
        self.CHK(nidaq.DAQmxCreateTask("",ctypes.byref(taskHandle)))
        self.CHK(nidaq.DAQmxCreateAIVoltageChan(taskHandle,b'Dev1/ai0',"",
                                           DAQmx_Val_Cfg_Default,
                                           float64(-10.0),float64(10.0),
                                           DAQmx_Val_Volts,None))
        self.CHK(nidaq.DAQmxCfgSampClkTiming(taskHandle,"",float64(10000.0),
                                        DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,
                                        uInt64(max_num_samples)));
        self.CHK(nidaq.DAQmxStartTask(taskHandle))
        read = int32()
        self.CHK(nidaq.DAQmxReadAnalogF64(taskHandle,max_num_samples,float64(10.0),
                                     DAQmx_Val_GroupByChannel,data.ctypes.data,
                                     max_num_samples,ctypes.byref(read),None))
        print('Acquired ' + repr(read.value) + ' points')
        if taskHandle.value != 0:
            nidaq.DAQmxStopTask(taskHandle)
            nidaq.DAQmxClearTask(taskHandle)
            
        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = main_daq()
    main.show()

    sys.exit(app.exec_())