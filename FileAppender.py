from datetime import datetime
import os

import LedDriver


class FileAppender:
    def __init__(self, path, id, led_driver):
        self._path = path
        self._id = id
        self._led_on = False
        self._led_driver = led_driver
        self._current_filename = self.create_filename()
        self._file = False

    def create_filename(self):
        time_now = datetime.now()
        current_date_time = time_now.strftime("%Y-%m-%d_%H")
        return f"log_{self._id}_{current_date_time}.txt"

    def create_line_timestamp(self):
        time_now = datetime.now()
        return time_now.strftime("%Y-%m-%d %H:%M:%S.%f")

    def check_fs(self):
        is_ok = os.path.ismount(self._path)
        if is_ok:
            self._led_driver.led_on(LedDriver.LED_MEMORY_PORT)
        else:
            self._led_driver.led_off(LedDriver.LED_MEMORY_PORT)
        return is_ok

    def append_text(self, text):
        if not self.check_fs():
            self._file = False
            return False

        if self.create_filename() != self._current_filename and self._file:
            self._file.close()
            self._file = False

        if not self._file:
            filepath = self._path + self.create_filename()
            self._file = open(filepath, "a")

        try:
            text_line = f"{self.create_line_timestamp()}: {text.rstrip()}\r\n"
            self._file.write(text_line)
            self._led_driver.blink(LedDriver.LED_MEMORY_PORT)
            return True
        except Exception as ex:
            print(ex)
            self._file.close()
            self._file = False
            return False

