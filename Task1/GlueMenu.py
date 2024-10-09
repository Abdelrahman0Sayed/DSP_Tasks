from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider
from PyQt5.QtGui import QIcon , QFont, QPixmap # Package to set an icon , fonts and images
from PyQt5.QtCore import Qt , QTimer  # used for alignments.
from PyQt5.QtWidgets import QLayout , QVBoxLayout , QHBoxLayout, QGridLayout ,QWidget, QFileDialog, QPushButton
import pyqtgraph as pg
from fetchApiData import FetchApi_MainWindow
from functions_graph import zoom_in, zoom_out, show_graph, hide_graph, increase_speed, decrease_speed, start_simulation, stop_simulation, rewind, change_color


class Ui_GlueMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("GluMenu")
        self.setWindowTitle("Glue Menu")
        self.resize(635, 303)
        self.setupUi()


    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 641, 261))
        self.widget.setObjectName("widget")
        self.signalsList1 = QtWidgets.QComboBox(self.widget)
        self.signalsList1.setGeometry(QtCore.QRect(480, 60, 81, 31))
        self.signalsList1.setObjectName("signalsList1")
        self.signal1From = QtWidgets.QLineEdit(self.widget)
        self.signal1From.setGeometry(QtCore.QRect(100, 60, 91, 31))
        self.signal1From.setStyleSheet("font-size:15px;")
        self.signal1From.setText("")
        self.signal1From.setObjectName("signal1From")
        self.glueButton = QtWidgets.QPushButton(self.widget)
        self.glueButton.setGeometry(QtCore.QRect(480, 220, 141, 41))
        self.glueButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.glueButton.setStyleSheet("font-size:16px;font-weight:bold;background-color:white;s")
        self.glueButton.setObjectName("glueButton")
        self.signalsList2 = QtWidgets.QComboBox(self.widget)
        self.signalsList2.setGeometry(QtCore.QRect(480, 130, 81, 31))
        self.signalsList2.setObjectName("signalsList2")
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_GlueMenu()
    ui.show()
    sys.exit(app.exec_())
