import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import sys

class PolarEcgPlot(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ECG Signals in Polar Coordinates")
        # Create a central widget to hold the layout
        self.CentralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.CentralWidget)
        
        # Create a horizontal layout to hold both plots
        self.Layout = QtWidgets.QHBoxLayout(self.CentralWidget)

        # Initialize the first plotting widget
        self.PlotWidgetGraph1 = pg.PlotWidget(title="Graph 1 Signals")
        self.Layout.addWidget(self.PlotWidgetGraph1)  # Add to layout

        # Initialize the second plotting widget
        self.PlotWidgetGraph2 = pg.PlotWidget(title="Graph 2 Signals")
        self.Layout.addWidget(self.PlotWidgetGraph2)  # Add to layout


        # Set up the plot
        for PlotWidget in [self.PlotWidgetGraph1, self.PlotWidgetGraph2]:
            PlotWidget.setAspectLocked(True)  
            PlotWidget.showGrid(x=True, y=True) 

        # Store file paths and colors for both plots
        self.Graph1FilePaths = []
        self.Graph1Colors = []
        self.CurrentIndex1 = 0  # For the first plot
        self.SegmentSize1 = 0  

        self.Graph2FilePaths = []
        self.Graph2Colors = []
        self.CurrentIndex2 = 0  # For the second plot
        self.SegmentSize2 = 0  

        # Set up timers for both plots
        self.Graph1Timer = QtCore.QTimer()
        self.Graph1Timer.timeout.connect(self.UpdatePlotGraph1)

        self.Graph2Timer = QtCore.QTimer()
        self.Graph2Timer.timeout.connect(self.UpdatePlotGraph2)

        # Store ECG signals for both plots
        self.EcgGraph1Signals = []
        self.EcgGraph2Signals = []

    def LoadEcgGraph1Signals(self, FilePaths, Colors):
        self.Graph1FilePaths = FilePaths
        self.Graph1Colors = Colors
        self.EcgGraph1Signals = self.LoadSignalsFromFiles(FilePaths)
        print(f"Loaded ECG signals for Graph 1: {self.EcgGraph1Signals}")

        # Set segment size and calculate max radius for limits
        if self.EcgGraph1Signals:
            self.SegmentSize1 = len(self.EcgGraph1Signals[0]) // 10  
            self.CurrentIndex1 = 0
            
            MaxRadius = max([np.max(Signal) for Signal in self.EcgGraph1Signals if len(Signal) > 0], default=1)
            Buffer = 0.1  
            self.PlotWidgetGraph1.setLimits(xMin=-MaxRadius*(1 + Buffer), xMax=MaxRadius*(1 + Buffer), 
                                             yMin=-MaxRadius*(1 + Buffer), yMax=MaxRadius*(1 + Buffer))
            self.Graph1Timer.start(50)  

            self.UpdatePlotGraph1()  # Initially plot the signals

    def LoadEcgGraph2Signals(self, FilePaths, Colors):
        self.Graph2FilePaths = FilePaths
        self.Graph2Colors = Colors
        self.EcgGraph2Signals = self.LoadSignalsFromFiles(FilePaths)
        print(f"Loaded ECG signals for Graph 2: {self.EcgGraph2Signals}")

        # Set segment size and calculate max radius for limits
        if self.EcgGraph2Signals:
            self.SegmentSize2 = len(self.EcgGraph2Signals[0]) // 10  
            self.CurrentIndex2 = 0
            
            MaxRadius = max([np.max(Signal) for Signal in self.EcgGraph2Signals if len(Signal) > 0], default=1)
            Buffer = 0.1  
            self.PlotWidgetGraph2.setLimits(xMin=-MaxRadius*(1 + Buffer), xMax=MaxRadius*(1 + Buffer), 
                                             yMin=-MaxRadius*(1 + Buffer), yMax=MaxRadius*(1 + Buffer))
            self.Graph2Timer.start(50)  

            self.UpdatePlotGraph2()  # Initially plot the signals

    def LoadSignalsFromFiles(self, FilePaths):
        Signals = []
        for FilePath in FilePaths:
            try:
                Data = pd.read_csv(FilePath, header=None)
                EcgSignal = Data.values.flatten()
                Signals.append(EcgSignal)
            except Exception as e:
                print(f"Error loading {FilePath}: {e}")
                Signals.append(np.array([]))  
        return Signals

    def UpdatePlotGraph1(self):
        # Clear the plot only if it's the first time
        if self.CurrentIndex1 == 0:
            self.PlotWidgetGraph1.clear()

        # Check if there are any loaded signals
        if not self.EcgGraph1Signals:
            print("No ECG signals to display for Graph 1.")
            return

        AllSignalsFinished = True  

        for i, EcgSignal in enumerate(self.EcgGraph1Signals):
            if len(EcgSignal) == 0:
                continue  # Skip if the signal is empty
            
            if self.CurrentIndex1 < len(EcgSignal):
                AllSignalsFinished = False  

                R = EcgSignal[self.CurrentIndex1:self.CurrentIndex1 + self.SegmentSize1]  
                NumSegmentSamples = len(R)
                ThetaSegment = np.linspace(0, 2 * np.pi, NumSegmentSamples)
                X = R * np.cos(ThetaSegment)
                Y = R * np.sin(ThetaSegment)

                Color = self.Graph1Colors[i]
                self.PlotWidgetGraph1.plot(X, Y, pen=pg.mkPen(Color, width=2), clear=False)

        self.CurrentIndex1 += self.SegmentSize1

        if AllSignalsFinished:
            self.Graph1Timer.stop()
            print("All ECG signals for Graph 1 have been displayed. Stopping plot updates.")

    def UpdatePlotGraph2(self):
        # Clear the plot only if it's the first time
        if self.CurrentIndex2 == 0:
            self.PlotWidgetGraph2.clear()

        # Check if there are any loaded signals
        if not self.EcgGraph2Signals:
            print("No ECG signals to display for Graph 2.")
            return

        AllSignalsFinished = True  

        for i, EcgSignal in enumerate(self.EcgGraph2Signals):
            if len(EcgSignal) == 0:
                continue  # Skip if the signal is empty
            
            if self.CurrentIndex2 < len(EcgSignal):
                AllSignalsFinished = False  

                R = EcgSignal[self.CurrentIndex2:self.CurrentIndex2 + self.SegmentSize2]  
                NumSegmentSamples = len(R)
                ThetaSegment = np.linspace(0, 2 * np.pi, NumSegmentSamples)
                X = R * np.cos(ThetaSegment)
                Y = R * np.sin(ThetaSegment)

                Color = self.Graph2Colors[i]
                self.PlotWidgetGraph2.plot(X, Y, pen=pg.mkPen(Color, width=2), clear=False)

        self.CurrentIndex2 += self.SegmentSize2

        if AllSignalsFinished:
            self.Graph2Timer.stop()
            print("All ECG signals for Graph 2 have been displayed. Stopping plot updates.")

# Step 4: Run the application
if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    Window = PolarEcgPlot()
    Window.show()
    sys.exit(App.exec_())
