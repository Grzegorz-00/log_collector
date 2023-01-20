from pyA20.gpio import gpio
import time
from threading import Thread
from collections import defaultdict

LED_MEMORY_PORT = 0
LED_SERIAL1_PORT = 2
LED_SERIAL2_PORT = 3

class LedDriver:
    def __init__(self):
        gpio.init()
        gpio.setcfg(LED_MEMORY_PORT, gpio.OUTPUT)
        gpio.setcfg(LED_SERIAL1_PORT, gpio.OUTPUT)
        gpio.setcfg(LED_SERIAL2_PORT, gpio.OUTPUT)

        gpio.output(LED_MEMORY_PORT, gpio.HIGH)
        gpio.output(LED_SERIAL1_PORT, gpio.HIGH)
        gpio.output(LED_SERIAL2_PORT, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(LED_MEMORY_PORT, gpio.LOW)
        gpio.output(LED_SERIAL1_PORT, gpio.LOW)
        gpio.output(LED_SERIAL2_PORT, gpio.LOW)
        time.sleep(0.5)

        self._is_blinking_dict = {LED_MEMORY_PORT:False, LED_SERIAL1_PORT:False, LED_SERIAL2_PORT:False}

    def led_on(self, led_port):
        if not self._is_blinking_dict[led_port]:
            self.led_on_internal(led_port)

    def led_on_internal(self, led_port):
        gpio.output(led_port, gpio.HIGH)

    def led_off(self, led_port):
        if self._is_blinking_dict[led_port]:
            time.sleep(1)
        self.led_off_internal(led_port)

    def led_off_internal(self, led_port):
        gpio.output(led_port, gpio.LOW)

    def blink(self, led_port):
        if not self._is_blinking_dict[led_port]:
            self._is_blinking_dict[led_port] = True
            self._t = Thread(target=self.blink_thread_body, args=(led_port,))
            self._t.start()

    def blink_thread_body(self, led_port):
        self.led_off_internal(led_port)
        time.sleep(0.05)
        self.led_on_internal(led_port)
        time.sleep(0.05)
        self._is_blinking_dict[led_port] = False
