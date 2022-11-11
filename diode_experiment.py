# Thijs de Zeeuw
# 8-11-2022
# model for measuring and computing charachteristics of electronic devices

from ardino_device import ArduinoVISADevice, info_devices
import numpy as np
import math

class DiodeExperiment:

    # requesting and asking for what device to use for input
    def __init__(self):
        print('devices to choose from')
        info_devices()
        self.device = ArduinoVISADevice(port = f"{input('What device would you like to use? ')}")

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
            self.device.set_output_value(value = i)
            volt_total = self.dac_volt(self.device.get_input_value(channel = 1), max_bits, max_volts)
            volt_resistance = self.dac_volt(self.device.get_input_value(channel = 2), max_bits, max_volts)

            # calculating
            volt_led = volt_total - volt_resistance
            i_led = volt_resistance / resistance

            voltage_led.append(volt_led)
            current_led.append(i_led)

        return voltage_led, current_led

    def measurements(self, N, start, stop):
        voltage_lists, current_lists = [], []

        for i in range(N):
            None

        return None 