import SerialManager
import LogcatManager
import argparse
import time
import LedDriver

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("log_path")
    args = parser.parse_args()
    led_driver = LedDriver.LedDriver()

    sm0 = SerialManager.SerialManager("/dev/ttyUSB0", "USB0", args.log_path, led_driver, LedDriver.LED_SERIAL1_PORT)
    sm0.start()
    sm1 = SerialManager.SerialManager("/dev/ttyUSB1", "USB1", args.log_path, led_driver, LedDriver.LED_SERIAL2_PORT)
    sm1.start()
    lm0 = LogcatManager.LogcatManager("LOGCAT", args.log_path, led_driver)
    lm0.start()


    while sm0.is_working() or sm1.is_working():
        print(sm0.print_status())
        print(sm1.print_status())
        print(lm0.print_status())
        time.sleep(1)