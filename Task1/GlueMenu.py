import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QSlider, QLabel, QGroupBox, QVBoxLayout, QGridLayout
import pyqtgraph as pg


class Ui_GlueMenu(QMainWindow):
    def __init__(self, parent=None, signal_data1=None, signal_data2=None):
        super().__init__()
        self.setObjectName("GluMenu")
        self.setWindowTitle("Glue Menu")
        self.resize(800, 600)

        # Pass the loaded signal data
        self.signal_data1 = signal_data1
        self.signal_data2 = signal_data2
        self.signal_data1 = self.signal_data1[:, 1]
        self.signal_data2 = self.signal_data2[:, 1]
        self.setupUi()

        # Store initial offset values
        self.offset1 = 0
        self.offset2 = 0
        self.start1 = 0
        self.end1 = len(self.signal_data1)
        self.start2 = 0
        self.end2 = len(self.signal_data2)
        self.x_scale = 1.0  # Initial scale factor for the x-axis

        # Connect glue button to action
        self.glueButton.clicked.connect(self.glue_signals)

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Create a layout
        main_layout = QVBoxLayout(self.centralwidget)

        # Create a plot widget
        self.graphWidget = pg.PlotWidget(self.centralwidget)
        main_layout.addWidget(self.graphWidget)

        # Glue button
        self.glueButton = QtWidgets.QPushButton("Glue Signals", self.centralwidget)
        main_layout.addWidget(self.glueButton)

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

        # Add a slider for controlling the x-axis scale
        self.xScaleSlider = QSlider(QtCore.Qt.Horizontal)
        self.xScaleSlider.setMinimum(1)
        self.xScaleSlider.setMaximum(30)  # Maximum zoom level
        self.xScaleSlider.setValue(10)  # Initial value represents 1.0 scale (10 divided by 10)
        self.xScaleSlider.setTickInterval(1)
        self.xScaleSlider.setTickPosition(QSlider.TicksBelow)
        main_layout.addWidget(self.xScaleSlider)

        # Label for scale
        self.xScaleLabel = QLabel("X-Axis Scale: 1.0x", self)
        main_layout.addWidget(self.xScaleLabel)

        # Connect the sliders to update the graph positions
        self.slider1.valueChanged.connect(self.update_graph_positions)
        self.slider2.valueChanged.connect(self.update_graph_positions)
        self.start_slider1.valueChanged.connect(self.update_graph_positions)
        self.end_slider1.valueChanged.connect(self.update_graph_positions)
        self.start_slider2.valueChanged.connect(self.update_graph_positions)
        self.end_slider2.valueChanged.connect(self.update_graph_positions)
        self.xScaleSlider.valueChanged.connect(self.update_x_scale)

    def glue_signals(self):
        # Ensure signals exist
        if self.signal_data1 is None or self.signal_data2 is None:
            print("Missing signal data.")
            return

        # Generate time axes for both signals (assuming equal sampling rate)
        self.time_1 = np.linspace(0, len(self.signal_data1), len(self.signal_data1), endpoint=False)
        self.time_2 = np.linspace(0, len(self.signal_data2), len(self.signal_data2), endpoint=False)

        # Clear previous plots
        self.graphWidget.clear()

        # Plot both signals
        self.plot1 = self.graphWidget.plot(self.time_1, self.signal_data1, pen='r', name="Signal 1")
        self.plot2 = self.graphWidget.plot(self.time_2, self.signal_data2, pen='b', name="Signal 2")

        # Set an initial x-range suitable for the view
        initial_x_range = 1000  # Adjust this value as needed
        self.graphWidget.setXRange(0, initial_x_range, padding=0)

        # Enable panning
        self.graphWidget.setMouseEnabled(x=True, y=False)

        # Reset sliders to zero after plotting
        self.slider1.setValue(0)
        self.slider2.setValue(0)

        # Reset x-axis scale
        self.xScaleSlider.setValue(10)  # Resets scale to 1.0
        self.update_x_scale()  # Update positions based on the new scale

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

        # Apply scaling to the time axes by adjusting based on x_scale
        time_1_shifted = (self.time_1[self.start1:self.end1] + offset1) * self.x_scale
        time_2_shifted = (self.time_2[self.start2:self.end2] + offset2) * self.x_scale

        # Interpolate to handle conflicts and gaps
        combined_time = np.union1d(time_1_shifted, time_2_shifted)
        signal1_interpolated = np.interp(combined_time, time_1_shifted, self.signal_data1[self.start1:self.end1])
        signal2_interpolated = np.interp(combined_time, time_2_shifted, self.signal_data2[self.start2:self.end2])

        # Resolve conflicts by averaging the signals where they overlap
        combined_signal = np.where(np.isnan(signal1_interpolated), signal2_interpolated,
                                   np.where(np.isnan(signal2_interpolated), signal1_interpolated,
                                            (signal1_interpolated + signal2_interpolated) / 2))

        # Update the data of the plots
        self.plot1.setData(combined_time, signal1_interpolated)
        self.plot2.setData(combined_time, signal2_interpolated)

    def update_x_scale(self):
        """ Update the x-axis scale based on the slider. """
        # Get the scale factor from the slider (divide by 10 to get a floating point scale)
        self.x_scale = self.xScaleSlider.value() / 10.0

        # Update the label to reflect the current scale
        self.xScaleLabel.setText(f"X-Axis Scale: {self.x_scale:.1f}x")

        # Update the graph positions to apply the new scale
        self.update_graph_positions()