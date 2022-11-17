# controller of an arduino used for measurement of voltage of a LED
import pyvisa

def list_devices():
    """Requesting the identification of visible devices

    Returns:
        list: List of device identities
    """    
    rm = pyvisa.ResourceManager("@py")
    return list(rm.list_resources())


def info_devices(device = False):
    """Requests and gives information of the device(s). If no argument is given it will give information of all devices.

    Args:
        device (str, list, optional): Device(s) for information to be requested from if no argument is given print information of all devices.
        Defaults to False.
    """    
    rm = pyvisa.ResourceManager("@py")
    if not device:
        for i, j in enumerate(list_devices()):
            try:
                print(f'{i}. {j}, information:', rm.open_resource(j, read_termination = "\n\r", write_termination = "\n").query("*IDN?"))
            except:
                print(f'{i}. {j}, device unknown')              # raises an userwarning

    else:
        try:
            print(f'{device}, information:', rm.open_resource(device, read_termination = "\n\r", write_termination = "\n").query("*IDN?"))
        except:
            print(f'{device}, device unknown')                  # raises an userwarning
    return


class ArduinoVISADevice:
    """Communucation with arduino.

    """
    
    def __init__(self, port):
        """Initialsing of device

        Args:
            port (string): Identification of the device to use
        """    

        self.output = 0
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(port, read_termination = "\r\n", write_termination = "\n")


    def channel_value(self, channel):
        """Measurement of a channel value

        Args:
            channel (int): The channel to be measured

        Returns:
            int: Channel value measured in bits
        """    

        return self.device.query(f"MEAS:CH{channel}?")

    def get_identification(self):
        """Requesting of identification of the used device

        Returns:
            string: Identification of device
        """   

        return self.device.query("*IDN?")

    def set_output_value(self, value, channel):
        """Setting the output value of a given channel

        Args:
            value (int): Value to output in bits
            channel (int): Channel for the value output from
        """    

        self.output = value
        self.device.query(f"OUT:CH{channel} {value}")

    def get_output_value(self):
        """Requesting of the last output value

        Returns:
            int: Output value in bits
        """        
        return self.output

    def get_input_value(self, channel):
        """Requesting of the value being recieved by a channel

        Args:
            channel (int): Channel to measure the input

        Returns:
            int: Channel value in bits
        """        
        self.value = self.channel_value(channel = channel) 
        return self.value

    def close_device(self):
        """Sets output value to 0 and closes the device
        """        
        self.set_output_value(value = 0, channel = 0)
        self.device.close()
