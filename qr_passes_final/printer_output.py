import serial
import adafruit_thermal_printer
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

buzzer = 23
GPIO.setup(buzzer,GPIO.OUT)



uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.00)

printer = ThermalPrinter(uart)
output = ""


def print_pass():
    global output
    printer.print("Hall Pass")
    printer.feed(2)
    printer.print(output)
    printer.feed(2)
    printer.print("This pass authorized by Mr. King")
    printer.feed(8)
    GPIO.output(buzzer,GPIO.HIGH)
    print("beep")
    sleep(0.5)
    GPIO.output(buzzer,GPIO.LOW)
    print("no beep")
        