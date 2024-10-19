# button_functions.py
from PyQt5.QtWidgets import QColorDialog
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import datetime

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
                adjust_graph_2_slider_max(UI_MainWindow)


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
    if self.loadSignalData(self.graph_1_files[-1]) is not None:
        total_length = len(self.loadSignalData(self.graph_1_files[-1]))  # Get the signal length
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
    if self.loadSignalData(self.graph_2_files[-1]) is not None:
        total_length = len(self.loadSignalData(self.graph_2_files[-1]))  # Get the signal length
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
    if self.loadSignalData(self.graph_1_files[-1]) is not None:
        # Get the current y-values of the signal (y-axis range)
        current_y_min, current_y_max = self.graph1.viewRange()[1]
        
        # Get the total range of the y-axis based on the signal data
        data_min = np.min(self.loadSignalData(self.graph_1_files[-1]))
        data_max = np.max(self.loadSignalData(self.graph_1_files[-1]))

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
    if self.loadSignalData(self.graph_2_files[-1]) is not None:
        # Get the current y-values of the signal (y-axis range)
        current_y_min, current_y_max = self.graph2.viewRange()[1]
        
        # Get the total range of the y-axis based on the signal data
        data_min = np.min(self.loadSignalData(self.graph_2_files[-1]))
        data_max = np.max(self.loadSignalData(self.graph_2_files[-1]))

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
    if self.loadSignalData(self.graph_1_files[-1], 1) is not None:
        total_length = len(self.loadSignalData(self.graph_1_files[-1], 1))  # Get the length of the signal
        window_size = 100  # The size of the visible window (you can adjust this)

        # Calculate the maximum slider value based on the total signal length
        max_slider_value = max(0, total_length - window_size)
    
        # Set the maximum value for the horizontal slider
        self.graph_1_H_slider.setMaximum(max_slider_value)
    
        print(f"Graph 1 Slider Max Value Set to: {max_slider_value}")


def adjust_graph_2_slider_max(self):
    """Adjusts the maximum value of the graph 2 horizontal slider based on signal length."""
    if self.loadSignalData(self.graph_2_files[-1], 2) is not None:
        total_length = len(self.loadSignalData(self.graph_2_files[-1], 2))  # Get the length of the signal
        window_size = 100  # The size of the visible window (you can adjust this)

        # Calculate the maximum slider value based on the total signal length
        max_slider_value = max(0, total_length - window_size)
    
        # Set the maximum value for the horizontal slider
        self.graph_2_H_slider.setMaximum(max_slider_value)
    
        print(f"Graph 2 Slider Max Value Set to: {max_slider_value}")


def setup_graph_widget(graph_widget):
    """ Set up the graph widget with panning and zooming enabled. """
    graph_widget.setMouseEnabled(x=True, y=True)
    graph_widget.showGrid(x=True, y=True)
    graph_widget.addLegend()

def update_graph_data(graph_widget, x_data, y_data, pen='r'):
    """ Update the graph widget with new data. """
    graph_widget.clear()
    graph_widget.plot(x_data, y_data, pen=pen)


def capture_signal_screenshot(graph_widget):
    """Capture a screenshot of the signal plot and save it as an image."""
    img_path = f"signal_screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    
    # Grab the widget's content
    screenshot = graph_widget.grab()
    
    # Save the screenshot to a file
    screenshot.save(img_path, "PNG")
    
    return img_path





def export_to_pdf(UI_MainWindow, isLinked, graphNum):
    # Create a PDF document
    report_name = f"Signal_Report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    pdf = SimpleDocTemplate(report_name, pagesize=A4)

    elements = []

    title = Paragraph(f"<b>Signal Report</b>", getSampleStyleSheet()['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    if isLinked:
        elements.append(Paragraph(f"<b>Linked Graphs Report</b>", getSampleStyleSheet()['Heading2']))
        elements.append(Paragraph(f"<b>Graph 1 Signal Report</b>", getSampleStyleSheet()['Heading2']))
        img1_path = capture_signal_screenshot(UI_MainWindow.graph1)  # Use the correct attribute
        elements.append(Image(img1_path, width=400, height=200))
        elements.append(create_stats_table(UI_MainWindow.loadSignalData(UI_MainWindow.graph_1_files[-1]), "Graph 1 Signal"))
        elements.append(Paragraph(f"<b>Graph 2 Signal Report</b>", getSampleStyleSheet()['Heading2']))
        img2_path = capture_signal_screenshot(UI_MainWindow.graph2)  # Use the correct attribute
        elements.append(Image(img2_path, width=400, height=200))
        elements.append(create_stats_table(UI_MainWindow.loadSignalData(UI_MainWindow.graph_2_files[-1]), "Graph 2 Signal"))

    else:
        if graphNum == 1:
            elements.append(Paragraph(f"<b>Graph 1 Signal Report</b>", getSampleStyleSheet()['Heading2']))
            img1_path = capture_signal_screenshot(UI_MainWindow.graph1)  # Use the correct attribute
            elements.append(Image(img1_path, width=400, height=200))
            elements.append(create_stats_table(UI_MainWindow.loadSignalData(UI_MainWindow.graph_1_files[-1]), "Graph 1 Signal"))
        else:
            elements.append(Paragraph(f"<b>Graph 2 Signal Report</b>", getSampleStyleSheet()['Heading2']))
            img2_path = capture_signal_screenshot(UI_MainWindow.graph2)  # Use the correct attribute
            elements.append(Image(img2_path, width=400, height=200))
            elements.append(create_stats_table(UI_MainWindow.loadSignalData(UI_MainWindow.graph_2_files[-1]), "Graph 2 Signal"))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", getSampleStyleSheet()['Normal']))

    pdf.build(elements)
    print(f"Report generated: {report_name}")

def export_to_pdf_glued(glued_graph, glued_data):
    # Create a PDF document
    report_name = f"Signal_Report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    pdf = SimpleDocTemplate(report_name, pagesize=A4)

    elements = []

    title = Paragraph(f"<b>Signal Report</b>", getSampleStyleSheet()['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Graph 1 Signal Report</b>", getSampleStyleSheet()['Heading2']))
    img1_path = capture_signal_screenshot(glued_graph)  # Use the correct attribute
    elements.append(Image(img1_path, width=400, height=200))
    elements.append(create_stats_table(glued_data, "Graph 1 Signal"))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", getSampleStyleSheet()['Normal']))

    pdf.build(elements)
    print(f"Report generated: {report_name}")

def create_stats_table(signal_data, graph_label):
    """Create a table for signal statistics such as mean, std, min, max, and duration."""
    
    if signal_data is None:
        return Paragraph(f"No data available for {graph_label}", getSampleStyleSheet()['Normal'])
    
    # Calculate statistics
    mean_val = np.mean(signal_data)
    std_val = np.std(signal_data)
    min_val = np.min(signal_data)
    max_val = np.max(signal_data)
    duration = len(signal_data)  # Assuming each point represents a time unit

    # Create a table with stats
    data = [
        ["Statistic", "Value"],
        ["Mean", f"{mean_val:.2f}"],
        ["Standard Deviation", f"{std_val:.2f}"],
        ["Min Value", f"{min_val:.2f}"],
        ["Max Value", f"{max_val:.2f}"],
        ["Duration", f"{duration} points"]
    ]


    # Format the table
    table = Table(data, colWidths=[250, 150])  # Set column widths to fit within the PDF layout
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all cells to center
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Background for body
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid
        ('TOPPADDING', (0, 0), (-1, -1),10),  # Add padding above the table
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # Add padding below the table
    ]))

    return table


# Define the function to remove a signal from the graph
def remove_signal(UI_MainWindow, isLinked, graphNum, signal_identifier):
    """
    Remove a signal from the specified graph.
    
    Parameters:
    - UI_MainWindow: The main window object containing the graphs.
    - isLinked: Boolean indicating if the graphs are linked.
    - graphNum: The graph number (1 or 2) if not linked.
    - signal_identifier: The identifier for the signal to be removed.
    """
    if isLinked:
        # Remove signal from both linked graphs
        remove_signal_from_graph(UI_MainWindow.graph1, signal_identifier, UI_MainWindow.graph_1_files)
        remove_signal_from_graph(UI_MainWindow.graph2, signal_identifier, UI_MainWindow.graph_1_files)
    else:
        if graphNum == 1:
            remove_signal_from_graph(UI_MainWindow.graph1, signal_identifier, UI_MainWindow.graph_1_files)
        else:
            remove_signal_from_graph(UI_MainWindow.graph2, signal_identifier, UI_MainWindow.graph_2_files)

def remove_signal_from_graph(graph, signal_identifier, graph_files):
    """
    Remove a signal from a specific graph.
    
    Parameters:
    - graph: The graph object from which to remove the signal.
    - signal_identifier: The identifier for the signal to be removed.
    """
    # Assuming signals are stored in a list within the graph object
    signals = graph.listDataItems()
    print(signals)
    for i , signal in enumerate(signals):
        # read the signal object in readable format

        print(signal_identifier)
        if graph_files[i] == signal_identifier:
            graph.removeItem(signal)
            print(f"Signal '{signal_identifier}' removed from the graph.")
            break
    else:
        print(f"Signal '{signal_identifier}' not found in the graph.")

# Example usage:
# remove_signal(UI_MainWindow, isLinked=True, graphNum=1, signal_identifier="Signal 1")
