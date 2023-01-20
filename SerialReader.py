import serial

class SerialReader:
    def __init__(self, port):
        self._port = port
        self._serial = None
    def open(self):
        self._serial = serial.Serial(self._port, 115200)

    def read_line(self):
        if self._serial:
            try:
                return self._serial.readline().decode("ascii")
            except Exception as ex:
                return None
        return None