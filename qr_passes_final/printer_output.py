import serial
import adafruit_thermal_printer
import grekinlogo.h



uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.00)

printer = ThermalPrinter(uart)
output = "This is a test"


def print_pass():
    global output
    printer.print(output)
    printer.feed(2)
    printer.print("Signature: __________________")
    printer.feed(5)
    
print_pass()