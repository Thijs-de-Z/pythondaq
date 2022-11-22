# model for measuring and computing charachteristics of electronic devices
from pythondaq.controllers.arduino_device import ArduinoVISADevice, info_devices, list_devices
import numpy as np
import math
from rich import progress_bar


def init(device):
    """Requesting of information of device(s). Uses an optional argument to request all devices

    Args:
        device (bool, list, str): Device(s) to request information of. Defaults to "true".

    Returns:
        list, str: Returns information of device(s)
    """
    if device == "true":
        return info_devices()

    else: 
        return info_devices(device)


def info():
    """Requests identification of devices

    Returns:
        list: Identification of all visible devices
    """
    return list_devices()


def adc(volts, max_volts, max_bits):
    """converts an analog voltage value to a digital value

    Args:
        volts (float): Analog value in volts
        max_volts (float): Maximum voltage the device can output
        max_bits (int): Maximum amount of bits the device can handle

    Returns:
        int: digital signal corresponding with the input voltage
    """    
    return int(volts / max_volts * max_bits)


def dac_volt(bits, max_bits, max_volts):
    """Converts a digital voltage value to an analog value
        The calculation assumes a linear dispersion of the analog voltage along the digital values

    Args:
        bits (int): Digital value in bits
        max_bits (int): Maximum amount of bits the device can handle
        max_volts (float): Maximum voltage the device can output

    Returns:
        float: Analog voltage value of the digital value
    """        
    return int(bits) / max_bits * max_volts


class DiodeExperiment:
    """Experiment for the I,U characteristics of a diode by measuring the voltages a LED and resistor
        The experiment uses 2^10 bits
    """    

    def __init__(self, port):
        """Initialising of experiment by opening the device with the given port

        Args:
            port (string): Identification string of the device to use
        """        
        self.device = ArduinoVISADevice(port = port)


    def scan(self, start, stop):
        """Measurement of of the voltage and current over the LED between a given start and stop value in bits

        Args:
            start (int): Starting value of measurement in bits
            stop (int): Stopping value of measurement in bits

        Returns:
            list: A list of 2 lists containg the voltage and current over and through the LED
        """        
        max_bits = 2 ** 10
        max_volts = 3.3
        voltage_led, current_led = [], []
        resistance = 220

        # converts start and stop values to bits if the given value is a float
        if isinstance(start, float):
            start = adc(start, max_volts, max_bits)

        if isinstance(stop, float):
            stop = adc(stop, max_volts, max_bits)

        for i in range(start, stop):
            self.device.set_output_value(value = i, channel = 0)
            volt_total = dac_volt(self.device.get_input_value(channel = 1), max_bits, max_volts)
            volt_resistance = dac_volt(self.device.get_input_value(channel = 2), max_bits, max_volts)

            volt_led = volt_total - volt_resistance
            i_led = volt_resistance / resistance

            voltage_led.append(volt_led)
            current_led.append(i_led)

        return voltage_led, current_led


    def measurements(self, N, start, stop):
        """Measures and calculates the voltage, current and error(if N > 1) N times for a given start and stop value.
            Results are given to self variables so these can be requested seperatly if needed.

        Args:
            N (int): amount of times the experiment has to run
            start (int): Starting value of measurement in bits
            stop (int): Stopping value of measurement in bits
        """        
        measured_currents, measured_voltages,  = [], []

        for i in range(N):
            measured = self.scan(start, stop)
            measured_currents.append(measured[1])
            measured_voltages.append(measured[0])

        transposed_current = np.array(measured_currents).T
        transposed_voltage = np.array(measured_voltages).T
        
        self.current_average = np.average(transposed_current, axis = 1)
        self.voltage_average = np.average(transposed_voltage, axis = 1)
        
        self.c_err = [np.std(i) / math.sqrt(N) for i in transposed_current]
        self.v_err = [np.std(i) / math.sqrt(N) for i in transposed_voltage]
        self.device.close_device()
    

    def get_current(self):        
        """Request the averages of the currents after the measurements

        Returns:
            list: Average current of the experiments conducted
        """        
        return self.current_average


    def get_voltage(self):
        """Request the averages of the voltages after the measurements

        Returns:
            list: Average voltages of the experiments conducted
        """            
        return self.voltage_average


    def get_err_current(self):
        """Request errors on the current after the measurements

        Returns:
            list: Erros on the current of the experiments conducted
        """            
        return self.c_err


    def get_err_voltage(self):
        """Request errors on the voltage after the measurements

        Returns:
            list: Errors on the voltage of the experiments conducted
        """             
        return self.v_err


    def identification(self):
        """Requesting of identification of the used device

        Returns:
            string: Identification of device
        """        
        return self.device.get_identification