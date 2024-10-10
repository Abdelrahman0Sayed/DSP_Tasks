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
            adjust_graph_1_slider_max(UI_MainWindow)
            adjust_graph_2_slider_max(UI_MainWindow)
    else:
        if graphNum == 1:
            if not UI_MainWindow.timer_graph_1.isActive():
                UI_MainWindow.timer_graph_1.start()
                adjust_graph_1_slider_max(UI_MainWindow)
        else:
            if not UI_MainWindow.timer_graph_2.isActive():
                UI_MainWindow.timer_graph_2.start()
                adjust_graph_2_slider_max(UI_MainWindow)


def stop_simulation(UI_MainWindow, isLinked, graphNum):
    if isLinked:
        if  UI_MainWindow.timer_linked_graphs.isActive():
            print("linked timer is active")
            UI_MainWindow.timer_graph_1.stop()
            UI_MainWindow.timer_graph_2.stop()
            UI_MainWindow.timer_linked_graphs.stop()
            adjust_graph_1_slider_max(UI_MainWindow)
    else:
        if graphNum == 1:
            if  UI_MainWindow.timer_graph_1.isActive():
                print("graph1 timer is active")
                UI_MainWindow.timer_graph_1.stop()
                adjust_graph_1_slider_max(UI_MainWindow)
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
        total_length = len(self.signal_data1)  # Get the signal length
        window_size = 100  # Visible window size
        
        # Adjust if the window size is greater than total length
        if window_size > total_length:
            window_size = total_length

        # Compute the maximum range for the x-axis
        data_min = 0
        data_max = total_length - window_size

        # Calculate the current position based on the slider value
        max_slider_value = self.graph_1_H_slider.maximum()  # Make sure this is updated
        x_min = int((value / max_slider_value) * data_max)  # Scale based on slider
        x_max = x_min + window_size

        # Set the graph's x-axis range
        self.graph1.setXRange(x_min, x_max, padding=0)

        # Debugging print statements to check calculations
        

def graph_2_h_slider_changed(self, value):
    """Handles changes in the horizontal slider to move the graph window horizontally."""
    if self.signal_data2 is not None:
        total_length = len(self.signal_data2)  # Get the signal length
        window_size = 100  # Visible window size
        
        # Adjust if the window size is greater than total length
        if window_size > total_length:
            window_size = total_length

        # Compute the maximum range for the x-axis
        data_min = 0
        data_max = total_length - window_size

        # Calculate the current position based on the slider value
        max_slider_value = self.graph_2_H_slider.maximum()  # Make sure this is updated
        x_min = int((value / max_slider_value) * data_max)  # Scale based on slider
        x_max = x_min + window_size

        # Set the graph's x-axis range
        self.graph2.setXRange(x_min, x_max, padding=0)

        # Debugging print statements to check calculations
        


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

def adjust_graph_1_slider_max(self):
    if self.signal_data1 is not None:
        total_length = len(self.signal_data1)  # Get the length of the signal
        window_size = 100  # The size of the visible window (you can adjust this)

        # Calculate the maximum slider value based on the total signal length
        max_slider_value = max(0, total_length - window_size)
        
        # Set the maximum value for the horizontal slider
        self.graph_1_H_slider.setMaximum(max_slider_value)
        
        print(f"Graph 1 Slider Max Value Set to: {max_slider_value}")


def adjust_graph_2_slider_max(self):
    """Adjusts the maximum value of the graph 2 horizontal slider based on signal length."""
    if self.signal_data2 is not None:
        total_length = len(self.signal_data2[0])  # Assuming signal_data2 is 2D
        window_size = 100  # Adjust as needed
        max_slider_value = max(0, total_length - window_size)
        
        # Set the slider maximum dynamically and print it for debugging
        self.graph_2_H_slider.setMaximum(max_slider_value)
        print(f"Graph 2 Max Slider Value Set to: {max_slider_value}")

