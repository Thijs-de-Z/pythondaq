import pyqtgraph as pq
from PySide6 import QtWidgets
import sys
from pythondaq.models.diode_experiment import DiodeExperiment

pq.setConfigOption("background", "w")
pq.setConfigOption("foreground", "k")

class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.widgets()
        self.widget_layout()
        self.widget_addition()
        self.init_attr()

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
        experiment = DiodeExperiment("ASRL4::INSTR")
        results = experiment.measurements(1, self.start_value.value(), self.stop_value.value())
        self.graph(data=[experiment.get_voltage(), experiment.get_current()])


    def graph(self, data):
        self.plot_widget.plot(data[0], data[1], symbol = "o", symbolBrush = "r", symbolPen = 'r', symbolSize = 3, pen=None)
        self.plot_widget.setLabel("left", "current [I]")
        self.plot_widget.setLabel("bottom", "voltage [V]")
    

    def save_data(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")




def main():
    """Opens the program and user interface annd returns any errors found while running the program.
    """    
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()