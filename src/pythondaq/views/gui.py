import pyqtgraph as pq
from PySide6 import QtWidgets
import sys
from pythondaq.models.diode_experiment import DiodeExperiment, info
import pandas as pd
import numpy as np

pq.setConfigOption("background", "w")
pq.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.choose_menu()

    def choose_menu(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        vbox = QtWidgets.QVBoxLayout(central_widget)

        self.text = QtWidgets.QLabel()
        self.text.setText("Please select a device:")

        self.device = QtWidgets.QComboBox()
        self.device.addItems(info())
        
        self.initialise_button = QtWidgets.QPushButton("start interface")
        self.initialise_button.clicked.connect(self.try_device)

        vbox.addWidget(self.text)
        vbox.addWidget(self.device)
        vbox.addWidget(self.initialise_button)

    def try_device(self):
        try:
            DiodeExperiment(self.device.currentText())
            self.init()
            self.string_device = self.device.currentText()
            print(self.device.currentText())
        except:
            self.text.setText("device not available")


    def init(self):
        self.widgets()
        self.widget_layout()
        self.widget_addition()

    def widget_layout(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.vbox = QtWidgets.QVBoxLayout(central_widget)
        self.vbox.addWidget(self.plot_widget)

        self.hbox_buttons = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(self.hbox_buttons)
        

    def widgets(self):
        self.plot_widget = pq.PlotWidget()

        self.start_value = QtWidgets.QDoubleSpinBox()
        self.start_value.setRange(0, 3.3)
        self.start_value.setValue(0)
        
        self.stop_value = QtWidgets.QDoubleSpinBox()
        self.stop_value.setRange(0, 3.3)
        self.stop_value.setValue(0)

        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self.scanning)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)
    

    def widget_addition(self):
        self.hbox_buttons.addWidget(self.start_value)
        self.hbox_buttons.addWidget(self.stop_value)
        self.hbox_buttons.addWidget(self.start_button)
        self.hbox_buttons.addWidget(self.save_button)


    def init_attr(self):
        pass
    

    def scanning(self):
        experiment = DiodeExperiment(self.string_device)
        results = experiment.measurements(2, self.start_value.value(), self.stop_value.value())
        self.voltage = experiment.get_voltage()
        self.err_voltage = experiment.get_err_voltage()
        self.current = experiment.get_current()
        self.err_current = experiment.get_err_current()
        self.graph()


    def graph(self):
        errorbar = pq.ErrorBarItem(x=self.voltage, y=self.current, width = 2 * np.array(self.err_voltage), height = 2* np.array(self.err_current), pen={"color": "r"})
        self.plot_widget.plot(self.voltage, self.current, symbol = "o", symbolBrush = "r", symbolPen = 'r', symbolSize = 3, pen=None)
        self.plot_widget.addItem(errorbar)
        self.plot_widget.setLabel("left", "current [I]")
        self.plot_widget.setLabel("bottom", "voltage [V]")
    

    def save_data(self):
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