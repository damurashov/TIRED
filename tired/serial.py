import serial


class SerialStream:
    def __init__(self, dev, rate):
        self.socket = serial.Serial()
        self.socket.port     = dev
        self.socket.baudrate = rate
        self.socket.parity   = 'N'
        self.socket.rtscts   = False
        self.socket.xonxoff  = False
        self.socket.timeout  = 0.01
        self.version = sys.version_info[0]
        try:
            self.socket.open()
        except serial.SerialException:
            print('Could not open serial port {:s}'.format(self.socket.portstr))
            exit()

    def __del__(self):
        self.socket.close()

    def close(self):
        self.socket.close()

    def open(self):
        self.socket.open()

    def flush(self):
        self.socket.reset_input_buffer()
        self.socket.reset_output_buffer()

    def read(self):
        try:
            data = self.socket.read()
            return bytearray(data) if self.version == 2 else data
        except serial.SerialException:
            print('Serial port error')
            exit()

    def write(self, data):
        self.socket.write(data)


def get_all_serial_devices():
    import serial.tools
    import serial.tools.list_ports
    return serial.tools.list_ports.comports()


def get_all_serial_device_names():
    return map(lambda device: device.device, get_all_serial_devices())
