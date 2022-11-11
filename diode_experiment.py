# model for measuring and computing charachteristics of electronic devices

from pythondaq.arduino_device import ArduinoVISADevice, info_devices, list_devices
import numpy as np

# asking devices and their information
def init():
    return info_devices()

class DiodeExperiment:

    # requesting and asking for what device to use for input
    def __init__(self, port):
        self.device = ArduinoVISADevice(port = str(list_devices()[int(port)]))

    # converting of digital to analog for voltage
    def dac_volt(self, bits, max_bits, max_volts):
        return int(bits) / max_bits * max_volts

    # measuring and calculating the u,i characteristics of a diode
    def scan(self, start, stop):
        max_bits = 2**10
        max_volts = 3.3
        voltage_led, current_led = [], []
        resistance = 220

        # requesting, converting and calculating of voltage and current and error
        for i in range(start, stop):

            # request and converting
            self.device.set_output_value(value = i, channel = 0)
            volt_total = self.dac_volt(self.device.get_input_value(channel = 1), max_bits, max_volts)
            volt_resistance = self.dac_volt(self.device.get_input_value(channel = 2), max_bits, max_volts)

            # calculating
            volt_led = volt_total - volt_resistance
            i_led = volt_resistance / resistance

            voltage_led.append(volt_led)
            current_led.append(i_led)

        return voltage_led, current_led

    # calculations of errors and average of multiple measurements
    def measurements(self, N, start, stop):
        current_lists, voltage_lists,  = [], []

        # measuring and calculating voltage and current 
        for i in range(N):
            measured = self.scan(start, stop)
            current_lists.append(measured[1])
            voltage_lists.append(measured[0])

        # transposing of the array of arrays to get the first, second, ... value of every array into a single array
        transposed_current = np.array(current_lists).T
        transposed_voltage = np.array(voltage_lists).T
        
        # averaging all values of the transposed array
        self.current_average = np.average(transposed_current, axis = 1)
        self.voltage_average = np.average(transposed_voltage, axis = 1)
        
        # calculating erros of all measurements
        self.c_err = [np.std(i) for i in transposed_current]
        self.v_err = [np.std(i) for i in transposed_voltage]

        self.device.close_device()
    
    # requesting of different measured values
    def get_current(self):
        return self.current_average

    def get_voltage(self):
        return self.voltage_average

    def get_err_current(self):
        return self.c_err

    def get_err_voltage(self):
        return self.v_err