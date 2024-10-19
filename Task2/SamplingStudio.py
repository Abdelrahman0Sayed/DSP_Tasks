from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider
from PyQt5.QtGui import QIcon , QFont, QPixmap, QColor # Package to set an icon , fonts and images
from PyQt5.QtCore import Qt , QTimer  # used for alignments.
from PyQt5.QtWidgets import QLayout , QVBoxLayout , QHBoxLayout, QGridLayout ,QWidget, QFileDialog, QPushButton, QColorDialog, QInputDialog, QComboBox, QDialog
import pyqtgraph as pg
import random


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """ Set Icons """
        startIcon = QIcon("images/play.png")
        stopIcon = QIcon("images/pause.png")
        rewindIcon = QIcon("images/rewind.png")

        self.setObjectName("MainWindow")
        self.resize(1200, 950)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setMinimumSize(900,700)
        # Creating layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Top widget (widget)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.graph1Layout = QHBoxLayout(self.widget)
        self.graph1 = pg.PlotWidget(title="Original Signal")
        self.graph1Layout.addWidget(self.graph1)

        # Horizontal layout for buttons
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Buttons
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("pushButton_4")
        self.startButton.setStyleSheet("""
            QPushButton{
                border: 2px solid black;
                border-radius: 10px;
                font-weight:bold;
                font-size:15px;
                padding: 5px 5px;
                background-color:white;
            }  
            QPushButton:hover{
                background-color:#d1d1d1;
            }                                  
        """)
        self.startButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startButton.setMinimumSize(40,40)
        self.startButton.setIcon(startIcon)
        self.startButton.setIconSize(QtCore.QSize(32,32))
        self.horizontalLayout.addWidget(self.startButton)

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setObjectName("pushButton_5")
        self.stopButton.setStyleSheet("""
            QPushButton{
                border: 2px solid black;
                border-radius: 10px;
                font-weight:bold;
                font-size: 15px;
                padding: 5px 5px;
                background-color:white;
            }
            QPushButton:hover{
                background-color:#d1d1d1;
            }                                    
        """)
        self.stopButton.setIcon(stopIcon)
        self.stopButton.setIconSize(QtCore.QSize(32,32))
        self.stopButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stopButton.setMinimumSize(40,40)
        self.horizontalLayout.addWidget(self.stopButton)

        self.rewindButton = QtWidgets.QPushButton(self.centralwidget)
        self.rewindButton.setObjectName("pushButton_6")
        self.rewindButton.setStyleSheet("""
            QPushButton{
                border: 2px solid black;
                border-radius: 10px;
                font-weight:bold;
                font-size:15px;             
                padding: 5px 5px;
                background-color:white;
            }                          
            QPushButton:hover{
                background-color:#d1d1d1;
            }     
        """)
        self.rewindButton.setIcon(rewindIcon)
        self.rewindButton.setIconSize(QtCore.QSize(32,32))
        self.rewindButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.rewindButton.setMinimumSize(40,40)
        self.horizontalLayout.addWidget(self.rewindButton)

        # Replacing ComboBox with QLineEdit
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Enter value")  # Placeholder for input
        self.lineEdit.setStyleSheet("font-size:16px;font-weight:bold;border:1px solid black;")
        self.lineEdit.setMinimumSize(100, 30)  # Set minimum size
        self.lineEdit.setMaximumSize(120, 40)  # Set maximum size
        self.horizontalLayout.addWidget(self.lineEdit)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setStyleSheet("font-weight:bold;font-size:16px")
        self.horizontalLayout.addWidget(self.label)

        self.mixerButton = QtWidgets.QPushButton(self.centralwidget)
        self.mixerButton.setObjectName("pushButton_2")
        self.mixerButton.setStyleSheet("""
            QPushButton{
                border: 2px solid black;
                border-radius: 10px;
                font-weight:bold;
                font-size:15px;             
                padding: 5px 5px;
                background-color:white;
            }                          
            QPushButton:hover{
                background-color:#d1d1d1;
            }                             
        """)
        self.mixerButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mixerButton.setMinimumSize(40,40)
        self.horizontalLayout.addWidget(self.mixerButton)

        self.browseFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseFileButton.setObjectName("pushButton")
        self.browseFileButton.setStyleSheet("""
            QPushButton{
                border: 2px solid black;
                border-radius: 10px;
                font-weight:bold;
                font-size:15px;             
                padding: 5px 5px;
                background-color:white;
            }                          
            QPushButton:hover{
                background-color:#d1d1d1;
            }                                
        """)
        self.browseFileButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browseFileButton.setMinimumSize(40,40)
        self.horizontalLayout.addWidget(self.browseFileButton)


        self.testSampling = QtWidgets.QPushButton(self.centralwidget)
        self.testSampling.setObjectName("pushButton")
        self.testSampling.setStyleSheet("""
            QPushButton{
                border: 2px solid black;
                border-radius: 10px;
                font-weight:bold;
                font-size:15px;             
                padding: 5px 5px;
                background-color:white;
            }                          
            QPushButton:hover{
                background-color:#d1d1d1;
            }                                
        """)
        self.testSampling.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.testSampling.setMinimumSize(40,40)
        self.horizontalLayout.addWidget(self.testSampling)


        # Adding signal display widgets
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout.addWidget(self.widget_2)
        self.graph2Layout = QHBoxLayout(self.widget_2)
        self.graph2 = pg.PlotWidget(title="Reconstructed Single")
        self.graph2Layout.addWidget(self.graph2)
        
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout.addWidget(self.widget_3)
        self.graph3Layout = QHBoxLayout(self.widget_3)
        self.graph3 = pg.PlotWidget(title="Signals Difference")
        self.graph3Layout.addWidget(self.graph3)


        self.widget_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout.addWidget(self.widget_4)
        self.graph4Layout = QHBoxLayout(self.widget_4)
        self.graph4 = pg.PlotWidget(title="Frequency Domain")
        self.graph4Layout.addWidget(self.graph4)


        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Sampling Studio"))
        self.browseFileButton.setText(_translate("MainWindow", "Browse File"))
        self.mixerButton.setText(_translate("MainWindow", "Mixer / Composer"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Pause"))
        self.rewindButton.setText(_translate("MainWindow", "Rewind"))
        self.testSampling.setText(_translate("MainWindow", "Test Sampling"))
        self.label.setText(_translate("MainWindow", "x Fmax"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
