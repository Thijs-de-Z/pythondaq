# controller of an arduino used for measurement of voltage of a LED
import pyvisa

# listing of devices
def list_devices():
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()

# getting the information of the plugged-in devices
def info_devices():
    rm = pyvisa.ResourceManager("@py")
    for i, j in enumerate(rm.list_resources()):

        # if information of device can not be requested, device will be unknown
        try:
            print(f'{i}. {j}, information:', rm.open_resource(str(j), read_termination = "\n\r", write_termination = "\n").query("*IDN?"))
        except:
            print(f'{i}. {j}, device unknown')              # raises an userwarning

    return rm.list_resources()

# communication with arduino
class ArduinoVISADevice:
    
    # opening and initialising of device
    def __init__(self, port):
        self.output = 0
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(port, read_termination = "\r\n", write_termination = "\n")

    # measuring of a channel
    def channel_value(self, channel):
        return self.device.query(f"MEAS:CH{channel}?")

    # asking for identification
    def get_identification(self):
        return self.device.query("*IDN?")

    # setting output of a channel
    def set_output_value(self, value, channel):
        self.output = value
        self.device.query(f"OUT:CH{channel} {value}")

    # requesting of set output
    def get_output_value(self):
        return self.output

    # requesting of channel value
    def get_input_value(self, channel):
        self.value = self.channel_value(channel = channel) 
        return self.value

    # closing of device
    def close_device(self):
        self.set_output_value(value = 0, channel = 0)
        self.device.close()
