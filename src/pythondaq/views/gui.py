import pyqtgraph as pq
from PySide6 import QtWidgets, QtCore
import sys
from pythondaq.models.diode_experiment import DiodeExperiment, info
import pandas as pd
import numpy as np

pq.setConfigOption("background", "w")
pq.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        """Initialises the class.
        """        
        super().__init__()
        self.widgets()
        self.widget_layout()
        self.widget_addition()
        self.init_attr()

    def widget_layout(self):
        """Creates widget layout of the userinterface.
        """        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.vbox = QtWidgets.QVBoxLayout(central_widget)
        self.vbox.addWidget(self.plot_widget)

        self.hbox_buttons = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(self.hbox_buttons)
        

    def widgets(self):
        """Creates all widgets needed to run the userinterface.
        """        
        self.plot_widget = pq.PlotWidget()

        self.start_value = QtWidgets.QDoubleSpinBox()
        self.start_value.setRange(0, 3.3)
        self.start_value.setValue(0)
        
        self.stop_value = QtWidgets.QDoubleSpinBox()
        self.stop_value.setRange(0, 3.3)
        self.stop_value.setValue(0)

        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self.start_scanning)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)
    

    def widget_addition(self):
        """Adds a selected amount of widgets to the made layout.
        """        
        self.hbox_buttons.addWidget(self.start_value)
        self.hbox_buttons.addWidget(self.stop_value)
        self.hbox_buttons.addWidget(self.start_button)
        self.hbox_buttons.addWidget(self.save_button)


    def init_attr(self):
        """Initialising attributes of the class that are needed to run the program
        """        
        self.string_device = "ASRL4::INSTR"
        self.experiment = DiodeExperiment(self.string_device)

    
    def start_scanning(self):
        """Starts a thread and creates a timer which calls the function to replot the data every 100ms.
        """        
        self.plot_timer = QtCore.QTimer()
        self.plot_timer.timeout.connect(self.graph)
        self.plot_timer.start(100)
        self.start_button.clicked.connect(None)

        self.experiment.start_measurements(4, self.start_value.value(), self.stop_value.value())


    def graph(self):
        """Function which is called every 100ms to plot a graph with the new data added. If the thread is finished it will show the final results.
        """        
        self.plot_widget.clear()
        self.plot_widget.plot(self.experiment.voltage_led, self.experiment.current_led, symbl="o", symbolSize=3, symbolPen="r", symbolBrush="r", pen=None)
        self.plot_widget.setLabel("left", "current [I]")
        self.plot_widget.setLabel("bottom", "voltage [V]")
        self.plot_widget.setXRange(0, 2)
        self.plot_widget.setYRange(-0.0005, 0.006)

        if not self.experiment._scan_thread.is_alive():
            self.plot_timer.stop()
            self.voltage = self.experiment.get_voltage()
            self.err_voltage = self.experiment.get_err_voltage()
            self.current = self.experiment.get_current()
            self.err_current = self.experiment.get_err_current()
            self.start_button.clicked.connect(self.start_scanning)
            self.end_graph()


    def end_graph(self):
        """Plotting of the final results of the measurements
        """        
        self.plot_widget.clear()
        errorbar = pq.ErrorBarItem(x=self.voltage, y=self.current, width = 2 * np.array(self.err_voltage), height = 2* np.array(self.err_current), pen={"color": "r"})
        self.plot_widget.plot(self.voltage, self.current, symbol = "o", symbolBrush = "r", symbolPen = 'r', symbolSize = 3, pen=None)
        self.plot_widget.addItem(errorbar)
        self.plot_widget.setLabel("left", "current [I]")
        self.plot_widget.setLabel("bottom", "voltage [V]")
        self.plot_widget.setXRange(0, 2)
        self.plot_widget.setYRange(-0.0005, 0.006)
    

    def save_data(self):
        """Saving of the data to a csv file. This file has the directory chosen by the user. It saves the voltage and current and their errors.
        """        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        df = {"voltage": self.voltage,
              "error_voltage": self.err_voltage,  
              "current": self.current,
              "error_current": self.err_current}
        df = pd.DataFrame(df)
        df.to_csv(filename, index = False, sep = ',')




def main():
    """Opens the program and user interface annd returns any errors found while running the program.
    """    
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()