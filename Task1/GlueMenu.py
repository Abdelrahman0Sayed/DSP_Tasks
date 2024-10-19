from PyQt5.QtCore import Qt, QTimer  # used for alignments.
from PyQt5.QtWidgets import QMainWindow, QSlider, QLabel, QGroupBox, QVBoxLayout, QGridLayout, QSpinBox, QComboBox, QPushButton
from functions_graph import export_to_pdf_glued
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from scipy.interpolate import interp1d

class Ui_GlueMenu(QMainWindow):
    def __init__(self, parent=None, signal_data1=None, signal_data2=None):
        super().__init__()
        self.setObjectName("GluMenu")
        self.setWindowTitle("Glue Menu")
        self.resize(1200, 800)  # Increase the window size

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

        # Timer for live updating the glued signal
        self.timer_glued_signal = QTimer(self)
        self.time_index_glued_signal = 0  # For Cine Mode Scrolling
        self.update_interval = 200  # Initial update interval (ms)

        # Connect glue button to action
        self.glueButton.clicked.connect(self.glue_signals)

    def setupUi(self):
        self.update_interval = 200  # Initial update interval (ms)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Create a layout
        main_layout = QGridLayout(self.centralwidget)

        # Create a plot widget for the original signals
        self.graphWidget1 = pg.PlotWidget(self.centralwidget)
        main_layout.addWidget(self.graphWidget1, 0, 0, 1, 2)
        main_layout.setRowStretch(0, 1)
        main_layout.setColumnStretch(0, 2)

        self.graphWidget2 = pg.PlotWidget(self.centralwidget)
        main_layout.addWidget(self.graphWidget2, 1, 0, 1, 2)
        main_layout.setRowStretch(1, 1)
        main_layout.setColumnStretch(0, 2)

        # Create a plot widget for the glued signal
        self.graphWidget_glued = pg.PlotWidget(self.centralwidget)
        main_layout.addWidget(self.graphWidget_glued, 2, 0, 1, 2)
        main_layout.setRowStretch(2, 2)
        main_layout.setColumnStretch(0, 2)

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

        main_layout.addWidget(group_box1, 0, 2, 1, 1)

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

        main_layout.addWidget(group_box2, 1, 2, 1, 1)

        # Group box for Glue Parameters
        group_box_glue = QGroupBox("Glue Parameters")
        layout_glue = QGridLayout()
        group_box_glue.setLayout(layout_glue)

        # Interpolation Order
        self.interp_label = QLabel("Interpolation Order:")
        layout_glue.addWidget(self.interp_label, 0, 0)
        self.interp_combobox = QComboBox()
        self.interp_combobox.addItems(["0", "1", "2", "3"])
        layout_glue.addWidget(self.interp_combobox, 0, 1)
        self.interp_combobox.currentIndexChanged.connect(self.perform_glue)

        main_layout.addWidget(group_box_glue, 2, 2, 1, 2)

        # Speed controller
        self.speed_label = QLabel("Speed:")
        layout_glue.addWidget(self.speed_label, 1, 0)
        self.speed_slider = QSlider(QtCore.Qt.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setValue(self.update_interval)
        self.speed_slider.setTickInterval(50)
        layout_glue.addWidget(self.speed_slider, 1, 1)
        self.speed_slider.valueChanged.connect(self.update_speed)

        # Rewind button
        self.rewind_button = QPushButton("Rewind", self.centralwidget)
        layout_glue.addWidget(self.rewind_button, 2, 0, 1, 2)
        self.rewind_button.clicked.connect(self.rewind_glued_signal)

        # Horizontal slider for glued signal
        self.glue_h_slider = QSlider(QtCore.Qt.Horizontal)
        self.glue_h_slider.setMinimum(0)
        self.glue_h_slider.setMaximum(1000)  # Placeholder; will update based on the signal length
        self.glue_h_slider.setValue(0)
        self.glue_h_slider.setTickInterval(1)
        main_layout.addWidget(self.glue_h_slider, 3, 0, 1, 2)
        self.glue_h_slider.valueChanged.connect(self.update_glued_signal_position)

        # Vertical slider for glued signal
        self.glue_v_slider = QSlider(QtCore.Qt.Vertical)
        self.glue_v_slider.setMinimum(0)
        self.glue_v_slider.setMaximum(1000)  # Placeholder; will update based on the signal length
        self.glue_v_slider.setValue(0)
        self.glue_v_slider.setTickInterval(1)
        main_layout.addWidget(self.glue_v_slider, 2, 3, 1, 1)
        self.glue_v_slider.valueChanged.connect(self.update_glued_signal_position)

        # Glue button
        self.glueButton = QtWidgets.QPushButton("Glue Signals", self.centralwidget)
        self.glueButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:#4CAF50;color:white;padding:10px;border-radius:5px;")
        main_layout.addWidget(self.glueButton, 4, 0, 1, 2)

        # Export PDF button
        self.exportGluedSignalButton = QtWidgets.QPushButton("Export Glued Signal", self.centralwidget)
        self.exportGluedSignalButton.setStyleSheet("font-weight:bold;font-size:16px;background-color:#FF5722;color:white;padding:10px;border-radius:5px;")
        main_layout.addWidget(self.exportGluedSignalButton, 5, 0, 1, 2)
        self.exportGluedSignalButton.clicked.connect(lambda: export_to_pdf_glued(self.graphWidget_glued, self.glued_signal))

        # Connect the sliders to update the graph positions and perform glue
        self.slider1.valueChanged.connect(self.update_graph_positions)
        self.slider2.valueChanged.connect(self.update_graph_positions)
        self.start_slider1.valueChanged.connect(self.update_graph_positions)
        self.end_slider1.valueChanged.connect(self.update_graph_positions)
        self.start_slider2.valueChanged.connect(self.update_graph_positions)
        self.end_slider2.valueChanged.connect(self.update_graph_positions)

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

        # Ensure the sliders do not move outside the signal range
        self.start1 = max(0, min(self.start1, len(self.signal_data1) - 1))
        self.end1 = max(self.start1 + 1, min(self.end1, len(self.signal_data1)))
        self.start2 = max(0, min(self.start2, len(self.signal_data2) - 1))
        self.end2 = max(self.start2 + 1, min(self.end2, len(self.signal_data2)))

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

        # Ensure the sliders do not move outside the signal range
        start1 = max(0, min(start1, len(self.signal_data1) - 1))
        end1 = max(start1 + 1, min(end1, len(self.signal_data1)))
        start2 = max(0, min(start2, len(self.signal_data2) - 1))
        end2 = max(start2 + 1, min(end2, len(self.signal_data2)))

        # Get the interpolation order
        interp_order = int(self.interp_combobox.currentText())

        # Apply the offsets and slice the signals
        time_1_shifted = self.time_1[start1:end1] + offset1
        time_2_shifted = self.time_2[start2:end2] + offset2

        # Interpolate to handle conflicts and gaps
        combined_time = np.union1d(time_1_shifted, time_2_shifted)
        if interp_order == 0:
            signal1_interpolated = np.interp(combined_time, time_1_shifted, self.signal_data1[start1:end1])
            signal2_interpolated = np.interp(combined_time, time_2_shifted, self.signal_data2[start2:end2])
        
        elif interp_order == 1:
            f1 = interp1d(time_1_shifted, self.signal_data1[start1:end1], kind='linear')
            f2 = interp1d(time_2_shifted, self.signal_data2[start2:end2], kind='linear')
            signal1_interpolated = f1(combined_time)
            signal2_interpolated = f2(combined_time)
        
        elif interp_order == 2:
            f1 = interp1d(time_1_shifted, self.signal_data1[start1:end1], kind='quadratic')
            f2 = interp1d(time_2_shifted, self.signal_data2[start2:end2], kind='quadratic')
            signal1_interpolated = f1(combined_time)
            signal2_interpolated = f2(combined_time)
        
        elif interp_order == 3:
            f1 = interp1d(time_1_shifted, self.signal_data1[start1:end1], kind='cubic')
            f2 = interp1d(time_2_shifted, self.signal_data2[start2:end2], kind='cubic')
            signal1_interpolated = f1(combined_time)
            signal2_interpolated = f2(combined_time)

        combined_signal = signal1_interpolated + signal2_interpolated

        # Store the glued signal data
        self.glued_time = combined_time
        self.glued_signal = combined_signal

        # Update the sliders' maximum values based on the glued signal length
        self.glue_h_slider.setMaximum(len(self.glued_signal) - 1)
        self.glue_v_slider.setMaximum(len(self.glued_signal) - 1)

        # Start the timer for live updating
        self.time_index_glued_signal = 0
        self.timer_glued_signal.timeout.connect(self.update_glued_signal)
        self.timer_glued_signal.start(self.update_interval)

    def update_glued_signal(self):
        """ Update the glued signal plot incrementally. """
        if self.glued_signal is None or len(self.glued_signal) == 0:
            print("There's no glued signal data.")
            return

        # Plot the glued signal incrementally
        self.graphWidget_glued.clear()
        self.graphWidget_glued.plot(self.glued_time[:self.time_index_glued_signal + 1], self.glued_signal[:self.time_index_glued_signal + 1], pen='g')

        if self.time_index_glued_signal > 200:
            self.graphWidget_glued.setXRange(self.time_index_glued_signal - 200 + 1, self.time_index_glued_signal + 1)
        else:
            self.graphWidget_glued.setXRange(0, 200)

        self.time_index_glued_signal += 5
        if self.time_index_glued_signal >= len(self.glued_signal):
            self.timer_glued_signal.stop()

    def update_speed(self, value):
        """ Update the speed of the live updating. """
        self.update_interval = value
        self.timer_glued_signal.setInterval(self.update_interval)

    def rewind_glued_signal(self):
        """ Rewind the glued signal to the beginning. """
        self.time_index_glued_signal = 0
        self.timer_glued_signal.start(self.update_interval)

    def update_glued_signal_position(self):
        """ Update the position of the glued signal based on the slider values. """
        h_value = self.glue_h_slider.value()
        v_value = self.glue_v_slider.value()

        # Update the x-range and y-range of the glued signal based on the slider values
        self.graphWidget_glued.setXRange(h_value, h_value + 200, padding=0)
        self.graphWidget_glued.setYRange(v_value, v_value + 200, padding=0)
