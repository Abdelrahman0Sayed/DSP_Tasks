import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider
from PyQt5.QtGui import QIcon , QFont # Package to set an icon , fonts and images
from PyQt5.QtCore import Qt , QTimer  # used for alignments.
from PyQt5.QtWidgets import QHBoxLayout ,QWidget, QPushButton, QColorDialog
import pyqtgraph as pg


class FetchApi_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName("Link Window")
        self.setWindowTitle("Real-Time Data Fetching")
        self.resize(1303, 595)
        self.setupUiElements()
        self.setStyleSheet("Background-color:#F0F0F0;")
        self.timer = QTimer(self) # Used primarly for cine mode
        self.timeIndex = 0 # For Cine Mode Scrolling
        self.graphColor= "#E8E8E8"

        self.fetchData()

    def setupUiElements(self):

        # Central Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        
        # Start Button
        self.startButton = QPushButton("Start", self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(60, 480, 131, 51))
        self.startButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(lambda: self.startDrawing())

        # Stop Button
        self.stopButton = QPushButton("Pause", self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(200, 480, 131, 51))
        self.stopButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.stopButton.setObjectName("stopButton")
        self.stopButton.clicked.connect(lambda: self.stopDrawing())

        # Rewind Button
        self.rewindButton = QPushButton("Rewind",self.centralwidget)
        self.rewindButton.setGeometry(QtCore.QRect(340, 480, 131, 51))
        self.rewindButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.rewindButton.setObjectName("rewindButton")
        self.rewindButton.clicked.connect(lambda: self.rewindDrawing())
        
        # Change Color Button
        self.changeGraphColor = QPushButton("Change Color",self.centralwidget)
        self.changeGraphColor.setGeometry(QtCore.QRect(800, 480, 131, 51))
        self.changeGraphColor.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.changeGraphColor.setObjectName("changeColor")
        self.changeGraphColor.clicked.connect(lambda: self.changeColor())
        
        # Speed Up Button
        self.increaseSpeed = QPushButton("Speed (+)",self.centralwidget)
        self.increaseSpeed.setGeometry(QtCore.QRect(510, 480, 131, 51))
        self.increaseSpeed.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.increaseSpeed.setObjectName("speedUp")
        self.increaseSpeed.clicked.connect(lambda: self.speedUp())


        # Speed Down Button
        self.decreaseSpeed = QPushButton("Speed (-)",self.centralwidget)
        self.decreaseSpeed.setGeometry(QtCore.QRect(650, 480, 131, 51))
        self.decreaseSpeed.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.decreaseSpeed.setObjectName("speedDown")
        self.decreaseSpeed.clicked.connect(lambda: self.speedDown())
        
        # Horizontal Slider
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(60, 440, 861, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        

        # Vertical Slider
        self.verticalSlider = QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(910, 109, 22, 311))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        
        # Side Buttons       
        self.widget = QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(950, 110, 331, 341))
        self.widget.setStyleSheet("""
        QWidget{
            background-color: white;
            border-radius: 10px;
            border: 2px solid black;
        }                          
        """)
        self.widget.setObjectName("sideButtonsWidget")
        # Show Button
        self.showButton = QPushButton("Show",self.widget)
        self.showButton.setGeometry(QtCore.QRect(30, 70, 131, 51))
        self.showButton.setStyleSheet("""
            QPushButton {
                background-color: #DBDBDB;
                border: 1px solid black;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }

            QPushButton::hover {
                background-color: white;
                border: 2px solid #000000;
                border-radius: 50px;
                box-shadow: inset 3px 3px 5px rgba(0, 0, 0, 0.5); /* Simulate an inset shadow */
            }

            QPushButton::pressed {
                background-color: darkgray;
                border: 2px solid #000000;
                border-radius: 50px;
                box-shadow: inset 3px 3px 8px rgba(0, 0, 0, 0.8); /* Stronger inset shadow when pressed */
            }
        """)
        self.showButton.setObjectName("show_button")
        self.showButton.clicked.connect(lambda: self.showGraph())
       
        # Hide Button
        self.hideButton = QPushButton("Hide",self.widget)
        self.hideButton.setGeometry(QtCore.QRect(180, 70, 131, 51))
        self.hideButton.setStyleSheet("""
            QPushButton {
                background-color: #DBDBDB;
                border: 1px solid black;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }

            QPushButton::hover {
                background-color: white;
                border: 2px solid #000000;
                border-radius: 50px;
                box-shadow: inset 3px 3px 5px rgba(0, 0, 0, 0.5); /* Simulate an inset shadow */
            }

            QPushButton::pressed {
                background-color: darkgray;
                border: 2px solid #000000;
                border-radius: 50px;
                box-shadow: inset 3px 3px 8px rgba(0, 0, 0, 0.8); /* Stronger inset shadow when pressed */
            }
        """)
        self.hideButton.setObjectName("hide_button")
        self.hideButton.clicked.connect(lambda: self.hideGraph())
        
        # Zoom out
        self.zoomGraphOut = QPushButton("-",self.widget)
        self.zoomGraphOut.setGeometry(QtCore.QRect(200, 170, 100, 100))
        self.zoomGraphOut.setStyleSheet("""
            QPushButton {
                background-color: #DBDBDB;
                border: 2px solid black;
                border-radius: 50px;
                font-size: 40px;
                font-weight: bold;
                padding: 10px;
            }

            QPushButton::hover {
                background-color: white;
                border: 2px solid #000000;
                border-radius: 50px;
                box-shadow: inset 3px 3px 5px rgba(0, 0, 0, 0.5); /* Simulate an inset shadow */
            }

            QPushButton::pressed {
                background-color: darkgray;
                border: 2px solid #000000;
                border-radius: 50px;
                box-shadow: inset 3px 3px 8px rgba(0, 0, 0, 0.8); /* Stronger inset shadow when pressed */
            }
        """)
        self.zoomGraphOut.setObjectName("zoomOut")
        self.zoomGraphOut.clicked.connect(lambda: self.zoomOut())

        # Zoom in
        self.zoomGraphIn = QPushButton("+",self.widget)
        self.zoomGraphIn.setGeometry(QtCore.QRect(40, 170, 100, 100))
        self.zoomGraphIn.setStyleSheet("""
            QPushButton {
                background-color: #DBDBDB;
                border: 2px solid black;
                border-radius: 50px;
                font-size: 40px;
                font-weight: bold;
                padding: 10px;
            }

            QPushButton::hover {
                background-color: white;
                border: 2px solid #000000;
                border-radius: 50px;
                box-shadow: inset 3px 3px 5px rgba(0, 0, 0, 0.5); /* Simulate an inset shadow */
            }

            QPushButton::pressed {
                background-color: darkgray;
                border: 2px solid #000000;
                border-radius: 50px;
                box-shadow: inset 3px 3px 8px rgba(0, 0, 0, 0.8); /* Stronger inset shadow when pressed */
            }
        """)
        self.zoomGraphIn.setObjectName("zoomIn")
        self.zoomGraphIn.clicked.connect(lambda: self.zoomIn())

        
        # Graph Widget
        self.graphWidget = QWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(50, 100, 860, 335))
        self.graphWidget.setObjectName("graph_widget")
        
        self.graph= pg.plot(title="Linked Signals")
        self.graphLayout= QHBoxLayout(self.graphWidget)
        self.graphLayout.addWidget(self.graph)

        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    
    def changeColor(self):
        color = QColorDialog.getColor()
        self.graphColor = color.name()



    def speedUp(self):
        currentInterval = self.timer.interval()  # Get the current interval in milliseconds
        if currentInterval > 100:  # Prevent it from going too fast
            newInterval = currentInterval - 100  # Decrease the interval to make it faster and don't make less than 
            if newInterval < 100:
                newInterval = 100
            self.timer.setInterval(newInterval)
            print(f"Speed increased. New interval: {newInterval} ms")


    def speedDown(self):
        currentInterval = self.timer.interval()  # Get the current interval in milliseconds
        newInterval = currentInterval + 100  # Increase the interval to make it slower
        self.timer.setInterval(newInterval)
        print(f"Speed decreased. New interval: {newInterval} ms")


    def startDrawing(self):
        if not self.timer.isActive():
            print("Drawing Started")
            self.timer.start()

    def stopDrawing(self):
        if self.timer.isActive():
            print("Drawing Stopped")
            self.timer.stop()

    def rewindDrawing(self):
        # Clear the old drawing
        self.graph.clear()
        self.timeData = []  # time values
        self.signalValues = []  # Signal Value List at specific time.
        # Stop the timer
        if self.timer.isActive():
            self.timer.stop()  # Stop the timer if it's running
        self.timeIndex = 0  # Reset the time index to the beginning

        # Start the simulation again from the beginning
        self.timer.start()
        print("Drawing Rewinded")


    def showGraph(self):
        self.graphWidget.show()

    def hideGraph(self):
        self.graphWidget.hide()

    def zoomIn(self):
        viewRange = self.graph.viewRange()
        self.graph.setXRange(viewRange[0][0] + 1, viewRange[0][1] - 1, padding=0)
        self.graph.setYRange(viewRange[1][0] + 1, viewRange[1][1] - 1, padding=0)

    def zoomOut(self):
        viewRange = self.graph.viewRange()
        self.graph.setXRange(viewRange[0][0] - 1, viewRange[0][1] + 1, padding=0)
        self.graph.setYRange(viewRange[1][0] - 1, viewRange[1][1] + 1, padding=0)

   
   
    def fetchData(self):
        self.graph.clear()  
        self.timeIndex = 0 

        # iam using list of values to make the continous function effect.
        self.timeData = []  # time values
        self.signalValues = []  # Signal Value List at specific time.
        
        self.timer.timeout.connect(self.slide_through_data)
        self.timer.start(200)  # 200 ms interval between each point


    def slide_through_data(self):
        signalData = self.getSignalData(self.timeIndex)  # Get data for current index

        # Append the current time index and corresponding signal data to lists
        self.timeData.append(self.timeIndex)
        self.signalValues.append(signalData)

        windowSize = 100  # Define window size

        # Plot the set of points
        self.graph.plot(self.timeData, self.signalValues, pen=self.graphColor)

        # Calculate the range of data to display (window)
        if self.timeIndex > windowSize:
            self.graph.setXRange(self.timeIndex - windowSize, self.timeIndex)
        else:
            self.graph.setXRange(0, windowSize)

        self.timeIndex += 1  # Increment the time index for next point


    def getSignalData(self, timeIndex):
        # Generate a sine wave signal
        sine_wave = np.sin(2 * np.pi * 0.05 * timeIndex)  # Sine wave with a specific frequency
        return sine_wave  # Return the sine wave signal





def main():
    app = QApplication(sys.argv)
    MainWindow = FetchApi_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
