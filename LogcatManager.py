import time

import FileAppender
import subprocess
import threading

class LogcatManager:
    def __init__(self, id, log_path, led_driver):
        self._id = id
        self._log_path = log_path
        self._is_working = False
        self._is_logcat = False
        self._led_driver = led_driver

    def start(self):
        self._file_appender = FileAppender.FileAppender(self._log_path, self._id, self._led_driver)
        self._is_working = True
        self._t = threading.Thread(target=self.thread_body)
        self._t.start()

    def thread_body(self):
        while self._is_working:
            process0 = subprocess.Popen(["adb", "logcat", "-c"], stdout=subprocess.PIPE)
            time.sleep(1)
            process = subprocess.Popen(["adb", "logcat", "*:I"], stdout=subprocess.PIPE)

            for line in iter(process.stdout.readline, ''):
                _is_logcat = True
                if len(line) < 2:
                    break
                if self._file_appender.check_fs():
                    try:
                        self._file_appender.append_text(line.decode("ascii"))
                    except Exception:
                        pass
            _is_logcat = False
            time.sleep(1)


    def print_status(self):
        return f"logger: {self._id} logat: {self._is_logcat}"

