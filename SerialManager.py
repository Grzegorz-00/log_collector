import SerialReader
import FileAppender
import LedDriver
import time
from threading import Thread

class SerialManager:


    def __init__(self, serial_port, id, log_path, led_driver, led_port):
        self._serial_port = serial_port
        self._id = id
        self._is_working = False
        self._serial_reader = None
        self._file_appender = None
        self._log_path = log_path
        self._is_serial_working = False
        self._is_fs_working = False
        self._led_driver = led_driver
        self._led_port = led_port



    def start(self):
        self._file_appender = FileAppender.FileAppender(self._log_path, self._id, self._led_driver)
        self._is_working = True
        self._t = Thread(target=self.thread_body)
        self._t.start()

    def thread_body(self):
        while self._is_working:
            self._file_appender.check_fs()

            if not self._is_serial_working:
                try:
                    self._serial_reader = SerialReader.SerialReader(self._serial_port)
                    self._serial_reader.open()
                    self._is_serial_working = True
                    self._led_driver.led_on(self._led_port)
                except Exception as e:
                    pass
                time.sleep(0.1)
            else:
                line = self._serial_reader.read_line()
                if line:
                    self._led_driver.blink(self._led_port)
                    self._file_appender.append_text(line)
                else:
                    self._is_serial_working = False
                    self._led_driver.led_off(self._led_port)


    def is_working(self):
        return self._is_working

    def print_status(self):
        return f"logger: {self._id} serial: {self._is_serial_working} fs: {self._is_fs_working}"