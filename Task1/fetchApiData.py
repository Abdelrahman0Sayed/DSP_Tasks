

import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider
from PyQt5.QtGui import QIcon , QFont, QPixmap # Package to set an icon , fonts and images
from PyQt5.QtCore import Qt , QTimer  # used for alignments.
from PyQt5.QtWidgets import QLayout , QVBoxLayout , QHBoxLayout, QGridLayout ,QWidget, QFileDialog, QPushButton
import pyqtgraph as pg
from functions_graph import zoom_in, zoom_out, show_graph, hide_graph, increase_speed, decrease_speed, start_simulation, stop_simulation, rewind, change_color


class FetchApi_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName("Link Window")
        self.setWindowTitle("Link Signals")
        self.resize(1303, 595)
        self.setupUiElements()
        self.setStyleSheet("Background-color:#F0F0F0;")
        self.timer = QTimer(self) # Used primarly for cine mode
        self.time_index = 0 # For Cine Mode Scrolling
        settings = RTIMU.Settings("RTIMULib")
        self.imu = RTIMU.RTIMU(settings)
        self.imu.IMUInit()

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

        # Stop Button
        self.stopButton = QPushButton("Pause", self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(200, 480, 131, 51))
        self.stopButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.stopButton.setObjectName("stopButton")
        
        # Rewind Button
        self.rewindButton = QPushButton("Rewind",self.centralwidget)
        self.rewindButton.setGeometry(QtCore.QRect(340, 480, 131, 51))
        self.rewindButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.rewindButton.setObjectName("rewindButton")
        
        # Change Color Button
        self.changeColor = QPushButton("Change Color",self.centralwidget)
        self.changeColor.setGeometry(QtCore.QRect(800, 480, 131, 51))
        self.changeColor.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.changeColor.setObjectName("changeColor")
        
        # Speed Up Button
        self.speedUp = QPushButton("Speed (+)",self.centralwidget)
        self.speedUp.setGeometry(QtCore.QRect(510, 480, 131, 51))
        self.speedUp.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.speedUp.setObjectName("speedUp")
        
        # Speed Down Button
        self.speedDown = QPushButton("Speed (-)",self.centralwidget)
        self.speedDown.setGeometry(QtCore.QRect(650, 480, 131, 51))
        self.speedDown.setStyleSheet("font-weight:bold;font-size:16px;background-color:white")
        self.speedDown.setObjectName("speedDown")
        
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
        self.show_button = QPushButton("Show",self.widget)
        self.show_button.setGeometry(QtCore.QRect(30, 70, 131, 51))
        self.show_button.setStyleSheet("""
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
        self.show_button.setObjectName("show_button")
        # Hide Button
        self.hide_button = QPushButton("Hide",self.widget)
        self.hide_button.setGeometry(QtCore.QRect(180, 70, 131, 51))
        self.hide_button.setStyleSheet("""
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
        self.hide_button.setObjectName("hide_button")
        # Zoom out
        self.zoomOut = QPushButton("-",self.widget)
        self.zoomOut.setGeometry(QtCore.QRect(200, 170, 100, 100))
        self.zoomOut.setStyleSheet("""
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
        self.zoomOut.setObjectName("zoomOut")
        # Zoom in
        self.zoomIn = QPushButton("+",self.widget)
        self.zoomIn.setGeometry(QtCore.QRect(40, 170, 100, 100))
        self.zoomIn.setStyleSheet("""
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
        self.zoomIn.setObjectName("zoomIn")
        
        # Graph Widget
        self.graphWidget = QWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(50, 100, 860, 335))
        self.graphWidget.setObjectName("graph_widget")
        
        self.graph= pg.plot(title="Linked Signals")
        self.graph_layout= QHBoxLayout(self.graphWidget)
        self.graph_layout.addWidget(self.graph)

        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)


    def fetchData(self):
        print("Fetching Data....")


    def slide_through_data(self, signalData):
        # Ensure the data is valid
        windowSize= 100
        if signalData is None or len(signalData) == 0:
            print("No signal data to slide.")
            return
        
        # Calculate the range of data to display (window)
        if self.time_index + windowSize <= len(signalData):
            # Adjust the x-axis range to simulate sliding effect
            self.graph.setXRange(self.time_index, self.time_index + windowSize, padding=0)
            
            # Increment the time index by step size for the next frame
            self.time_index += 1
        else:
            # Stop when reaching the end of the signal
            self.timer.stop()
            print("Finished sliding through the entire signal.")


def main():
    app = QApplication(sys.argv)
    MainWindow = FetchApi_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
