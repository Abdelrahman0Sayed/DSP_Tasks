import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider
from PyQt5.QtGui import QIcon , QFont, QPixmap # Package to set an icon , fonts and images
from PyQt5.QtCore import Qt , QTimer  # used for alignments.
from PyQt5.QtWidgets import QLayout , QVBoxLayout , QHBoxLayout, QGridLayout ,QWidget, QFileDialog, QPushButton
import pyqtgraph as pg


class Ui_GlueMenu(QMainWindow):
    def __init__(self, parent=None, graph1_files=None, graph2_files=None, signal_data1=None, signal_data2=None):
        super().__init__()
        self.setObjectName("GluMenu")
        self.setWindowTitle("Glue Menu")
        self.resize(635, 303)
        
        # Pass the loaded signal data
        self.signal_data1 = signal_data1
        self.signal_data2 = signal_data2
        self.graph1_files = graph1_files
        self.graph2_files = graph2_files
        self.setupUi()

        # Connect glue button to action
        self.glueButton.clicked.connect(self.glue_signals)

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 641, 261))
        self.widget.setObjectName("widget")
        self.signalsList1 = QtWidgets.QComboBox(self.widget)
        self.signalsList1.setGeometry(QtCore.QRect(480, 60, 81, 31))
        self.signalsList1.setObjectName("signalsList1")
        for signal in self.graph1_files:
            self.signalsList1.addItem(signal)
        self.signal1From = QtWidgets.QLineEdit(self.widget)
        self.signal1From.setGeometry(QtCore.QRect(100, 60, 91, 31))
        self.signal1From.setStyleSheet("font-size:15px;")
        self.signal1From.setText("")
        self.signal1From.setObjectName("signal1From")
        self.glueButton = QtWidgets.QPushButton(self.widget)
        self.glueButton.setGeometry(QtCore.QRect(480, 220, 141, 41))
        self.glueButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.glueButton.setStyleSheet("font-size:16px;font-weight:bold;background-color:white;")
        self.glueButton.setObjectName("glueButton")
        self.signalsList2 = QtWidgets.QComboBox(self.widget)
        self.signalsList2.setGeometry(QtCore.QRect(480, 130, 81, 31))
        self.signalsList2.setObjectName("signalsList2")
        for signal in self.graph2_files:
            self.signalsList2.addItem(signal)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(40, 60, 51, 21))
        self.label.setStyleSheet("font-size:20px;font-weight:bold")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(40, 130, 51, 21))
        self.label_2.setStyleSheet("font-size:20px;font-weight:bold")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(220, 70, 31, 16))
        self.label_3.setStyleSheet("font-size:20px;font-weight:bold")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(220, 140, 31, 16))
        self.label_4.setStyleSheet("font-size:20px;font-weight:bold")
        self.label_4.setObjectName("label_4")
        self.signal1From_2 = QtWidgets.QLineEdit(self.widget)
        self.signal1From_2.setGeometry(QtCore.QRect(250, 60, 91, 31))
        self.signal1From_2.setStyleSheet("font-size:15px;")
        self.signal1From_2.setText("")
        self.signal1From_2.setObjectName("signal1From_2")
        self.signal1From_3 = QtWidgets.QLineEdit(self.widget)
        self.signal1From_3.setGeometry(QtCore.QRect(250, 130, 91, 31))
        self.signal1From_3.setStyleSheet("font-size:15px;")
        self.signal1From_3.setText("")
        self.signal1From_3.setObjectName("signal1From_3")
        self.signal1From_4 = QtWidgets.QLineEdit(self.widget)
        self.signal1From_4.setGeometry(QtCore.QRect(100, 130, 91, 31))
        self.signal1From_4.setStyleSheet("font-size:15px;")
        self.signal1From_4.setText("")
        self.signal1From_4.setObjectName("signal1From_4")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(400, 60, 71, 31))
        self.label_5.setStyleSheet("font-size:20px;font-weight:bold")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(400, 130, 71, 31))
        self.label_6.setStyleSheet("font-size:20px;font-weight:bold")
        self.label_6.setObjectName("label_6")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 635, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, GluMenu):
        _translate = QtCore.QCoreApplication.translate
        GluMenu.setWindowTitle(_translate("GluMenu", "MainWindow"))
        self.glueButton.setText(_translate("GluMenu", "Glue Signals"))
        self.label.setText(_translate("GluMenu", "From"))
        self.label_2.setText(_translate("GluMenu", "From"))
        self.label_3.setText(_translate("GluMenu", "To"))
        self.label_4.setText(_translate("GluMenu", "To"))
        self.label_5.setText(_translate("GluMenu", "Signal"))
        self.label_6.setText(_translate("GluMenu", "Signal"))

    def glue_signals(self):
        from_1 = int(self.signal1From.text())
        to_1 = int(self.signal1From_2.text())

        # Get values for the second signal
        from_2 = int(self.signal1From_4.text())
        to_2 = int(self.signal1From_3.text())

        # Ensure signals exist
        if self.signal_data1 is None or self.signal_data2 is None:
            print("Missing signal data.")
            return

        # Validate range
        if to_1 > len(self.signal_data1) or to_2 > len(self.signal_data2):
            print("Invalid range for one of the signals.")
            return
        
        # flatten the signals (2d to 1d)
        # self.signal_data1 = np.ravel(self.signal_data1)
        # self.signal_data2 = np.ravel(self.signal_data2)

        # use another way to flatten the signals 
        self.signal_data1 = self.signal_data1[:,1]
        self.signal_data2 = self.signal_data2[:,1]


        # Slice the signals
        sliced_signal_1 = self.signal_data1[from_1:to_1]
        sliced_signal_2 = self.signal_data2[from_2:to_2]

        # Pad the shorter signal with zeros to match the length of the longer one
        # max_length = max(len(sliced_signal_1), len(sliced_signal_2))
        # sliced_signal_1 = np.pad(sliced_signal_1, (0, max_length - len(sliced_signal_1)), mode='constant')
        # sliced_signal_2 = np.pad(sliced_signal_2, (0, max_length - len(sliced_signal_2)), mode='constant')

        # Generate time axes for both signals (assuming equal sampling rate)
        time_1 = np.linspace(from_1, to_1, len(sliced_signal_1), endpoint=False)
        time_2 = np.linspace(to_1, to_1 + (to_2 - from_2), len(sliced_signal_2), endpoint=False)

        # Glue the signals together along the first axis
        glued_signal = np.concatenate((sliced_signal_1, sliced_signal_2), axis=0)
        # Generate the time axis for the glued signal

        glued_time = np.concatenate((time_1, time_2))

        # Open a new window to display the glued signal
        self.openGluedSignalTab(glued_time, glued_signal)



    def openGluedSignalTab(self, glued_time, glued_signal):
        # Create a new graph for the glued signal
        self.glued_graph = pg.PlotWidget()
        self.glued_graph.setTitle("Glued Signal", color="w", size="15pt")

        # Plot the glued signal with the correct time axis
        self.glued_graph.plot(glued_time, glued_signal, pen='r')

        # Create a new window to show the glued graph
        self.new_window = QMainWindow()
        self.new_window.setCentralWidget(self.glued_graph)
        self.new_window.resize(600, 400)
        self.new_window.setWindowTitle("Glued Signal Display")
        self.new_window.show()

