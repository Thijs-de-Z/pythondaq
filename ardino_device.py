import pyvisa

# listing of devices
def list_devices(rm):
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()

# getting the information of the plugged-in devices
def info_devices():
    rm = pyvisa.ResourceManager("@py")
    for i in rm.list_resources():

        # if information of device can not be requested, device will be unknown
        try:
            print(f'{i}, information:', rm.open_resource(str(i), read_termination = "\n\r", write_termination = "\n").query("*IDN?"))
        except:
            print(f'{i}, device unknown')

# 
class ArduinoVISADevice:
    
    def __init__(self, port):
        self.output = 0
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(f"{port}", read_termination = "\r\n", write_termination = "\n")

    def channel_value(self, channel):
        return self.device.query(f"MEAS:CH{channel}?")

    def get_identification(self):
        return self.device.query("*IDN?")

    def set_output_value(self, value):
        self.output = value
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self):
        return self.output

    def get_input_value(self, channel):
        self.value = self.channel_value(channel = channel) 
        return self.value

    def close_device(self):
        self.set_output_value(value = 0)
        self.device.close()
