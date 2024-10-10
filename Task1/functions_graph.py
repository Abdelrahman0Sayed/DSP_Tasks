# button_functions.py
from PyQt5.QtWidgets import QColorDialog
import numpy as np


def increase_speed(UI_MainWindow, isLinked, graphNum):
    if isLinked:
        current_interval = UI_MainWindow.timer_linked_graphs.interval()  # Get the current interval in milliseconds
        if current_interval > 100:  # Prevent it from going too fast
            new_interval = max(100, current_interval - 100)  # Decrease the interval to make it faster
            UI_MainWindow.timer_linked_graphs.setInterval(new_interval)
            print(f"Speed increased. New interval: {new_interval} ms")
    else:
        if graphNum == 1:
            current_interval = UI_MainWindow.timer_graph_1.interval()  # Get the current interval in milliseconds
            if current_interval > 100:  # Prevent it from going too fast
                new_interval = max(100, current_interval - 100)  # Decrease the interval to make it faster
                UI_MainWindow.timer_graph_1.setInterval(new_interval)
                print(f"Speed increased. New interval: {new_interval} ms")
        else:
            current_interval = UI_MainWindow.timer_graph_2.interval()  # Get the current interval in milliseconds
            if current_interval > 100:  # Prevent it from going too fast
                new_interval = max(100, current_interval - 100)  # Decrease the interval to make it faster
                UI_MainWindow.timer_graph_2.setInterval(new_interval)
                print(f"Speed increased. New interval: {new_interval} ms")



def decrease_speed(UI_MainWindow, isLinked, graphNum):
    if isLinked:
        current_interval = UI_MainWindow.timer_linked_graphs.interval()  # Get the current interval in milliseconds
        new_interval = current_interval + 100  # Increase the interval to make it slower
        UI_MainWindow.timer_linked_graphs.setInterval(new_interval)
        print(f"Speed decreased. New interval: {new_interval} ms")
    else:
        if graphNum == 1:
            current_interval = UI_MainWindow.timer_graph_1.interval()  # Get the current interval in milliseconds
            new_interval = current_interval + 100  # Increase the interval to make it slower
            UI_MainWindow.timer_graph_1.setInterval(new_interval)
            print(f"Speed decreased. New interval: {new_interval} ms")
        else:
            current_interval = UI_MainWindow.timer_graph_2.interval()  # Get the current interval in milliseconds
            new_interval = current_interval + 100  # Increase the interval to make it slower
            UI_MainWindow.timer_graph_2.setInterval(new_interval)
            print(f"Speed decreased. New interval: {new_interval} ms")



def start_simulation(UI_MainWindow, isLinked, graphNum):
    if isLinked:
        if not UI_MainWindow.timer_linked_graphs.isActive():
            UI_MainWindow.timer_linked_graphs.start()
            UI_MainWindow.timer_graph_1.start()
            UI_MainWindow.timer_graph_2.start()
            # Update limits for linked graphs (if needed)
            graph_1_h_slider_changed(UI_MainWindow,UI_MainWindow.graph_1_H_slider.value())
    else:
        if graphNum == 1:
            if not UI_MainWindow.timer_graph_1.isActive():
                UI_MainWindow.timer_graph_1.start()
                graph_1_h_slider_changed(UI_MainWindow,UI_MainWindow.graph_1_H_slider.value())
        else:
            if not UI_MainWindow.timer_graph_2.isActive():
                UI_MainWindow.timer_graph_2.start()


def stop_simulation(UI_MainWindow, isLinked, graphNum):
    if isLinked:
        if  UI_MainWindow.timer_linked_graphs.isActive():
            print("linked timer is active")
            UI_MainWindow.timer_graph_1.stop()
            UI_MainWindow.timer_graph_2.stop()
            UI_MainWindow.timer_linked_graphs.stop()
    else:
        if graphNum == 1:
            if  UI_MainWindow.timer_graph_1.isActive():
                print("graph1 timer is active")
                UI_MainWindow.timer_graph_1.stop()
        else:
            if  UI_MainWindow.timer_graph_2.isActive():
                print("graph2 timer is active")
                UI_MainWindow.timer_graph_2.stop()


def rewind(UI_MainWindow, isLinked , graphNum):
    # clear the graph
    if isLinked:
        UI_MainWindow.graph1.clear()
        UI_MainWindow.graph2.clear()
        if UI_MainWindow.timer_linked_graphs.isActive():
            UI_MainWindow.timer_linked_graphs.stop()  # Stop the timer if it's running
        UI_MainWindow.time_index_linked_graphs = 0  # Reset the time index to the beginning

        # Start the simulation again from the beginning
        UI_MainWindow.timer_linked_graphs.start()
    else:
        if graphNum == 1:
            UI_MainWindow.graph1.clear()
            if UI_MainWindow.timer_graph_1.isActive():
                UI_MainWindow.timer_graph_1.stop()
            UI_MainWindow.time_index_graph_1 = 0
            UI_MainWindow.timer_graph_1.start()     
        else:
            UI_MainWindow.graph2.clear()
            if UI_MainWindow.timer_graph_2.isActive():
                UI_MainWindow.timer_graph_2.stop()
            UI_MainWindow.time_index_graph_2 = 0
            UI_MainWindow.timer_graph_2.start()     


def zoom_in(UI_MainWindow, isLinked, graphNum):
    if isLinked :
        viewRangeGraph1 = UI_MainWindow.graph1.viewRange()
        UI_MainWindow.graph1.setXRange(viewRangeGraph1[0][0] + 1, viewRangeGraph1[0][1] - 1, padding=0)
        UI_MainWindow.graph1.setYRange(viewRangeGraph1[1][0] + 1, viewRangeGraph1[1][1] - 1, padding=0)

        viewRangeGraph2 = UI_MainWindow.graph2.viewRange()
        UI_MainWindow.graph2.setXRange(viewRangeGraph2[0][0] + 1, viewRangeGraph2[0][1] - 1, padding=0)
        UI_MainWindow.graph2.setYRange(viewRangeGraph2[1][0] + 1, viewRangeGraph2[1][1] - 1, padding=0)
    else:
        if graphNum == 1: 
            viewRangeGraph1 = UI_MainWindow.graph1.viewRange()
            UI_MainWindow.graph1.setXRange(viewRangeGraph1[0][0] + 1, viewRangeGraph1[0][1] - 1, padding=0)
            UI_MainWindow.graph1.setYRange(viewRangeGraph1[1][0] + 1, viewRangeGraph1[1][1] - 1, padding=0)
        else:
            viewRangeGraph2 = UI_MainWindow.graph2.viewRange()
            UI_MainWindow.graph2.setXRange(viewRangeGraph2[0][0] + 1, viewRangeGraph2[0][1] - 1, padding=0)
            UI_MainWindow.graph2.setYRange(viewRangeGraph2[1][0] + 1, viewRangeGraph2[1][1] - 1, padding=0)


def zoom_out(UI_MainWindow, isLinked, graphNum):
    if isLinked :
        viewRangeGraph1 = UI_MainWindow.graph1.viewRange()
        UI_MainWindow.graph1.setXRange(viewRangeGraph1[0][0] - 1, viewRangeGraph1[0][1] + 1, padding=0)
        UI_MainWindow.graph1.setYRange(viewRangeGraph1[1][0] - 1, viewRangeGraph1[1][1] + 1, padding=0)

        viewRangeGraph2 = UI_MainWindow.graph2.viewRange()
        UI_MainWindow.graph2.setXRange(viewRangeGraph2[0][0] - 1, viewRangeGraph2[0][1] + 1, padding=0)
        UI_MainWindow.graph2.setYRange(viewRangeGraph2[1][0] - 1, viewRangeGraph2[1][1] + 1, padding=0)
    else:
        if graphNum == 1: 
            viewRangeGraph1 = UI_MainWindow.graph1.viewRange()
            UI_MainWindow.graph1.setXRange(viewRangeGraph1[0][0] - 1, viewRangeGraph1[0][1] + 1, padding=0)
            UI_MainWindow.graph1.setYRange(viewRangeGraph1[1][0] - 1, viewRangeGraph1[1][1] + 1, padding=0)
        else:
            viewRangeGraph2 = UI_MainWindow.graph2.viewRange()
            UI_MainWindow.graph2.setXRange(viewRangeGraph2[0][0] - 1, viewRangeGraph2[0][1] + 1, padding=0)
            UI_MainWindow.graph2.setYRange(viewRangeGraph2[1][0] - 1, viewRangeGraph2[1][1] + 1, padding=0)


def hide_graph(UI_MainWindow, isLinked, graphNum):
    if isLinked:
        UI_MainWindow.Graph1.hide()
        UI_MainWindow.Graph2.hide()
    else:
        if graphNum == 1:
            UI_MainWindow.Graph1.hide()
        else:
            UI_MainWindow.Graph2.hide()

def show_graph(UI_MainWindow, isLinked, graphNum):
    if isLinked:
        UI_MainWindow.Graph1.show()
        UI_MainWindow.Graph2.show()
    else:
        if graphNum == 1:
            UI_MainWindow.Graph1.show()
        else:
            UI_MainWindow.Graph2.show()


def change_color(UI_MainWindow, isLinked ,graphNum):
    # open a color dialog to choose a color
    color = QColorDialog.getColor()
    if isLinked:
        if color.isValid():
            UI_MainWindow.linked_graphs_color = color.name()
    else:

        if color.isValid():
            if graphNum == 1:
                UI_MainWindow.graph1_color  = color.name()
            else:
                UI_MainWindow.graph2_color = color.name()

def graph_1_h_slider_changed(self, value):
    """Handles changes in the horizontal slider to move the graph window horizontally."""
    if self.signal_data1 is not None:
        # Get the total length of the signal (x-axis values)
        total_length = len(self.signal_data1[0])  # Assuming signal_data1 is 2D

        # Define the window size (number of data points visible at once)
        window_size = 100  # Adjust this based on the visible range you want

        # Ensure the window size doesn't exceed the signal length
        if window_size > total_length:
            window_size = total_length

        # Get the min and max x-values based on the signal data
        data_min = 0  # Assuming x-values start at index 0
        data_max = total_length - window_size  # Adjusted to account for the window size

        # Calculate the new x-axis range based on the slider's value
        max_slider_value = self.graph_1_H_slider.maximum()
        x_min = int((value / max_slider_value) * (data_max - data_min))  # Shift based on slider value
        x_max = x_min + window_size  # Maintain the window size

        # Ensure new limits do not exceed the actual data range
        x_min = max(x_min, data_min)
        x_max = min(x_max, total_length)

        # Adjust the x-axis range on the graph
        self.graph1.setXRange(x_min, x_max, padding=0)

def graph_2_h_slider_changed(self, value):
    """Handles changes in the horizontal slider to move the graph window horizontally."""
    if self.signal_data2 is not None:
        # Get the total length of the signal (x-axis values)
        total_length = len(self.signal_data2[0])  # Assuming signal_data2 is 2D

        # Define the window size (number of data points visible at once)
        window_size = 100  # Adjust this based on the visible range you want

        # Ensure the window size doesn't exceed the signal length
        if window_size > total_length:
            window_size = total_length

        # Get the min and max x-values based on the signal data
        data_min = 0  # Assuming x-values start at index 0
        data_max = total_length - window_size  # Adjusted to account for the window size

        # Calculate the new x-axis range based on the slider's value
        max_slider_value = self.graph_2_H_slider.maximum()
        x_min = int((value / max_slider_value) * (data_max - data_min))  # Shift based on slider value
        x_max = x_min + window_size  # Maintain the window size

        # Ensure new limits do not exceed the actual data range
        x_min = max(x_min, data_min)
        x_max = min(x_max, total_length)

        # Adjust the x-axis range on the graph
        self.graph2.setXRange(x_min, x_max, padding=0)


def graph_1_v_slider_changed(self, value):
    """Handles changes in the vertical slider to move the graph window vertically."""
    if self.signal_data1 is not None:
        # Get the current y-values of the signal (y-axis range)
        current_y_min, current_y_max = self.graph1.viewRange()[1]
        
        # Get the total range of the y-axis based on the signal data
        data_min = np.min(self.signal_data1)
        data_max = np.max(self.signal_data1)

        print(data_max)
        print(data_min)
        
        # Calculate the current y-range
        current_y_range = current_y_max - current_y_min
        
        # Determine the amount to shift the view based on the slider's value
        # Scale the slider value to the range of y data
        max_slider_value = self.graph_1_V_slider.maximum()
        shift_amount = (value / max_slider_value) * (data_max - data_min)

        # Calculate new y-limits based on the shift
        new_y_min = data_min + shift_amount - (current_y_range / 2)
        new_y_max = data_min + shift_amount + (current_y_range / 2)

        # Ensure the new limits do not exceed the data limits
        new_y_min = max(new_y_min, data_min)
        new_y_max = min(new_y_max, data_max)

        # Adjust the y-axis range on the graph
        self.graph1.setYRange(new_y_min, new_y_max, padding=0)


def graph_2_v_slider_changed(self, value):
    """Handles changes in the vertical slider to move the graph window vertically."""
    if self.signal_data2 is not None:
        # Get the current y-values of the signal (y-axis range)
        current_y_min, current_y_max = self.graph2.viewRange()[1]
        
        # Get the total range of the y-axis based on the signal data
        data_min = np.min(self.signal_data2)
        data_max = np.max(self.signal_data2)

        print(data_max)
        print(data_min)
        
        # Calculate the current y-range
        current_y_range = current_y_max - current_y_min
        
        # Determine the amount to shift the view based on the slider's value
        # Scale the slider value to the range of y data
        max_slider_value = self.graph_2_V_slider.maximum()
        shift_amount = (value / max_slider_value) * (data_max - data_min)

        # Calculate new y-limits based on the shift
        new_y_min = data_min + shift_amount - (current_y_range / 2)
        new_y_max = data_min + shift_amount + (current_y_range / 2)

        # Ensure the new limits do not exceed the data limits
        new_y_min = max(new_y_min, data_min)
        new_y_max = min(new_y_max, data_max)

        # Adjust the y-axis range on the graph
        self.graph2.setYRange(new_y_min, new_y_max, padding=0)

