from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QSlider, QLabel, QGroupBox, QVBoxLayout, QGridLayout, QSpinBox, QComboBox, QDialog, QPushButton
from functions_graph import export_to_pdf_glued
import pyqtgraph as pg
import numpy as np


class GluedSignalPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Glued Signal")
        self.resize(800, 600)
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout(self)
        self.graphWidget_glued = pg.PlotWidget(self)
        layout.addWidget(self.graphWidget_glued)

        # Add sliders for panning control
        self.slider_label = QLabel("Pan:")
        layout.addWidget(self.slider_label)
        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickInterval(1)
        layout.addWidget(self.slider)

        # Connect slider to pan control method
        self.slider.valueChanged.connect(self.update_pan)

    def plot_glued_signal(self, time, signal):
        self.graphWidget_glued.clear()
        self.graphWidget_glued.plot(time, signal, pen='g')
        self.time = time
        self.signal = signal
        self.update_pan(self.slider.value())

    def update_pan(self, value):
        """ Update the view range based on the slider value. """
        range_width = 1000  # Adjust this value as needed
        center = (value / 100) * (self.time[-1] - self.time[0]) + self.time[0]
        self.graphWidget_glued.setXRange(center - range_width / 2, center + range_width / 2, padding=0)


class Ui_GlueMenu(QMainWindow):
    def __init__(self, parent=None, signal_data1=None, signal_data2=None):
        super().__init__()
        self.setObjectName("GluMenu")
        self.setWindowTitle("Glue Menu")
        self.resize(800, 600)

        # Pass the loaded signal data
        self.signal_data1 = signal_data1
        self.signal_data2 = signal_data2
        try:
            self.signal_data1 = self.signal_data1[:, 1]
            self.signal_data2 = self.signal_data2[:, 1]
        except:
            pass
        self.setupUi()

        # Store initial offset values
        self.offset1 = 0
        self.offset2 = 0
        self.start1 = 0
        self.end1 = len(self.signal_data1)
        self.start2 = 0
        self.end2 = len(self.signal_data2)

        # Connect glue button to action
        self.glueButton.clicked.connect(self.glue_signals)

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Create a layout
        main_layout = QVBoxLayout(self.centralwidget)

        # Create a plot widget for the original signals
        self.graphWidget1 = pg.PlotWidget(self.centralwidget)
        main_layout.addWidget(self.graphWidget1, stretch=3)

        self.graphWidget2 = pg.PlotWidget(self.centralwidget)
        main_layout.addWidget(self.graphWidget2, stretch=3)

        # Create a plot widget for the glued signal
        self.graphWidget_glued = pg.PlotWidget(self.centralwidget)
        main_layout.addWidget(self.graphWidget_glued, stretch=3)
        #hide the glued signal plot
        self.graphWidget_glued.hide()

        # Glue button
        self.glueButton = QtWidgets.QPushButton("Glue Signals", self.centralwidget)
        self.glueButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:#4CAF50;color:white;padding:10px;border-radius:5px;")
        main_layout.addWidget(self.glueButton)

        # Show glued signal button
        self.showGluedSignalButton = QtWidgets.QPushButton("Show Glued Signal", self.centralwidget)
        self.showGluedSignalButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:#2196F3;color:white;padding:10px;border-radius:5px;")
        main_layout.addWidget(self.showGluedSignalButton)
        self.showGluedSignalButton.clicked.connect(self.show_glued_signal_popup)

        # export pdf
        self.exportGluedSignalButton = QtWidgets.QPushButton("Export Glued Signal", self.centralwidget)
        self.exportGluedSignalButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:#FF5722;color:white;padding:10px;border-radius:5px;")
        main_layout.addWidget(self.exportGluedSignalButton)
        self.exportGluedSignalButton.clicked.connect(lambda: export_to_pdf_glued(self.graphWidget_glued, self.glued_signal))

        # Group box for Signal 1 controls
        group_box1 = QGroupBox("Signal 1 Controls")
        layout1 = QGridLayout()
        group_box1.setLayout(layout1)

        # Offset slider for Signal 1
        self.slider1_label = QLabel("Offset:")
        layout1.addWidget(self.slider1_label, 0, 0)
        self.slider1 = QSlider(QtCore.Qt.Horizontal)
        self.slider1.setMinimum(-len(self.signal_data1))
        self.slider1.setMaximum(len(self.signal_data1))
        self.slider1.setValue(0)
        self.slider1.setTickInterval(1)
        layout1.addWidget(self.slider1, 0, 1)

        # Start slider for Signal 1
        self.start_slider1_label = QLabel("Start:")
        layout1.addWidget(self.start_slider1_label, 1, 0)
        self.start_slider1 = QSlider(QtCore.Qt.Horizontal)
        self.start_slider1.setMinimum(0)
        self.start_slider1.setMaximum(len(self.signal_data1) - 1)
        self.start_slider1.setValue(0)
        self.start_slider1.setTickInterval(1)
        layout1.addWidget(self.start_slider1, 1, 1)

        # End slider for Signal 1
        self.end_slider1_label = QLabel("End:")
        layout1.addWidget(self.end_slider1_label, 2, 0)
        self.end_slider1 = QSlider(QtCore.Qt.Horizontal)
        self.end_slider1.setMinimum(0)
        self.end_slider1.setMaximum(len(self.signal_data1) - 1)
        self.end_slider1.setValue(len(self.signal_data1))
        self.end_slider1.setTickInterval(1)
        layout1.addWidget(self.end_slider1, 2, 1)

        main_layout.addWidget(group_box1)

        # Group box for Signal 2 controls
        group_box2 = QGroupBox("Signal 2 Controls")
        layout2 = QGridLayout()
        group_box2.setLayout(layout2)

        # Offset slider for Signal 2
        self.slider2_label = QLabel("Offset:")
        layout2.addWidget(self.slider2_label, 0, 0)
        self.slider2 = QSlider(QtCore.Qt.Horizontal)
        self.slider2.setMinimum(-len(self.signal_data2))
        self.slider2.setMaximum(len(self.signal_data2))
        self.slider2.setValue(0)
        self.slider2.setTickInterval(1)
        layout2.addWidget(self.slider2, 0, 1)

        # Start slider for Signal 2
        self.start_slider2_label = QLabel("Start:")
        layout2.addWidget(self.start_slider2_label, 1, 0)
        self.start_slider2 = QSlider(QtCore.Qt.Horizontal)
        self.start_slider2.setMinimum(0)
        self.start_slider2.setMaximum(len(self.signal_data2) - 1)
        self.start_slider2.setValue(0)
        self.start_slider2.setTickInterval(1)
        layout2.addWidget(self.start_slider2, 1, 1)

        # End slider for Signal 2
        self.end_slider2_label = QLabel("End:")
        layout2.addWidget(self.end_slider2_label, 2, 0)
        self.end_slider2 = QSlider(QtCore.Qt.Horizontal)
        self.end_slider2.setMinimum(0)
        self.end_slider2.setMaximum(len(self.signal_data2) - 1)
        self.end_slider2.setValue(len(self.signal_data2))
        self.end_slider2.setTickInterval(1)
        layout2.addWidget(self.end_slider2, 2, 1)

        main_layout.addWidget(group_box2)

        # Group box for Glue Parameters
        group_box_glue = QGroupBox("Glue Parameters")
        layout_glue = QGridLayout()
        group_box_glue.setLayout(layout_glue)

        # Gap/Overlap
        # self.gap_label = QLabel("Gap/Overlap:")
        # layout_glue.addWidget(self.gap_label, 0, 0)
        # self.gap_spinbox = QSpinBox()
        # self.gap_spinbox.setMinimum(-1000)
        # self.gap_spinbox.setMaximum(1000)
        # self.gap_spinbox.setValue(0)
        # layout_glue.addWidget(self.gap_spinbox, 0, 1)

        # Interpolation Order
        # self.interp_label = QLabel("Interpolation Order:")
        # layout_glue.addWidget(self.interp_label, 1, 0)
        # self.interp_combobox = QComboBox()
        # self.interp_combobox.addItems(["0", "1", "2", "3"])
        # layout_glue.addWidget(self.interp_combobox, 1, 1)

        main_layout.addWidget(group_box_glue)

        # Connect the sliders to update the graph positions and perform glue
        self.slider1.valueChanged.connect(self.update_graph_positions)
        self.slider2.valueChanged.connect(self.update_graph_positions)
        self.start_slider1.valueChanged.connect(self.update_graph_positions)
        self.end_slider1.valueChanged.connect(self.update_graph_positions)
        self.start_slider2.valueChanged.connect(self.update_graph_positions)
        self.end_slider2.valueChanged.connect(self.update_graph_positions)
        #self.gap_spinbox.valueChanged.connect(self.perform_glue)
        #self.interp_combobox.currentIndexChanged.connect(self.perform_glue)

    def glue_signals(self):
        # Ensure signals exist
        if self.signal_data1 is None or self.signal_data2 is None:
            print("Missing signal data.")
            return

        # Generate time axes for both signals (assuming equal sampling rate)
        self.time_1 = np.linspace(0, len(self.signal_data1), len(self.signal_data1), endpoint=False)
        self.time_2 = np.linspace(0, len(self.signal_data2), len(self.signal_data2), endpoint=False)

        # Clear previous plots
        self.graphWidget1.clear()
        self.graphWidget2.clear()
        self.graphWidget_glued.clear()

        # Plot both signals
        self.plot1 = self.graphWidget1.plot(self.time_1, self.signal_data1, pen='r', name="Signal 1")
        self.plot2 = self.graphWidget2.plot(self.time_2, self.signal_data2, pen='b', name="Signal 2")

        # Set an initial x-range suitable for the view
        initial_x_range = 1000  # Adjust this value as needed
        self.graphWidget1.setXRange(0, initial_x_range, padding=0)
        self.graphWidget2.setXRange(0, initial_x_range, padding=0)
        self.graphWidget_glued.setXRange(0, initial_x_range, padding=0)

        # Enable panning and zooming
        self.graphWidget1.setMouseEnabled(x=True, y=True)
        self.graphWidget2.setMouseEnabled(x=True, y=True)
        self.graphWidget_glued.setMouseEnabled(x=True, y=True)

        # Reset sliders to zero after plotting
        self.slider1.setValue(0)
        self.slider2.setValue(0)

        # Perform the glue operation
        self.perform_glue()



    def update_graph_positions(self):
        """ Update the position of the graphs based on the slider values. """
        # Get the current offset values from the sliders
        offset1 = self.slider1.value()
        offset2 = self.slider2.value()

        # Get the current start and end values from the sliders
        self.start1 = self.start_slider1.value()
        self.end1 = self.end_slider1.value()
        self.start2 = self.start_slider2.value()
        self.end2 = self.end_slider2.value()

        # Update the slider labels to reflect the current offset values
        self.slider1_label.setText(f"Signal 1 Offset: {offset1}")
        self.slider2_label.setText(f"Signal 2 Offset: {offset2}")

        # Apply the offsets and slice the signals
        time_1_shifted = self.time_1[self.start1:self.end1] + offset1
        time_2_shifted = self.time_2[self.start2:self.end2] + offset2

        # Update the data of the plots
        self.plot1.setData(time_1_shifted, self.signal_data1[self.start1:self.end1])
        self.plot2.setData(time_2_shifted, self.signal_data2[self.start2:self.end2])

        # Perform the glue operation
        self.perform_glue()

    def perform_glue(self):
        """ Perform the glue operation using interpolation. """
        # Clear the previous glued signal plot
        self.graphWidget_glued.clear()

        # Get the current offset values from the sliders
        offset1 = self.slider1.value()
        offset2 = self.slider2.value()

        # Get the current start and end values from the sliders
        start1 = self.start_slider1.value()
        end1 = self.end_slider1.value()
        start2 = self.start_slider2.value()
        end2 = self.end_slider2.value()

        # Get the gap/overlap value
        #gap = self.gap_spinbox.value()

        # Get the interpolation order
        # interp_order = int(self.interp_combobox.currentText())

        # Apply the offsets and slice the signals
        time_1_shifted = self.time_1[start1:end1] + offset1
        time_2_shifted = self.time_2[start2:end2] + offset2

        # Interpolate to handle conflicts and gaps
        combined_time = np.union1d(time_1_shifted, time_2_shifted)
        signal1_interpolated = np.interp(combined_time, time_1_shifted, self.signal_data1[start1:end1])
        signal2_interpolated = np.interp(combined_time, time_2_shifted, self.signal_data2[start2:end2])

        combined_signal = signal1_interpolated + signal2_interpolated


        # Plot the glued signal
        self.graphWidget_glued.plot(combined_time, combined_signal, pen='g', name="Glued Signal")

        # Store the glued signal data for the popup
        self.glued_time = combined_time
        self.glued_signal = combined_signal

    def show_glued_signal_popup(self):
        """ Show the glued signal in a popup window. """
        self.popup = GluedSignalPopup(self)
        self.popup.plot_glued_signal(self.glued_time, self.glued_signal)
        self.popup.exec_()
