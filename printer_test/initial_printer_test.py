import serial
import adafruit_thermal_printer


uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.00)

printer = ThermalPrinter(uart)
output = ""


def print_user_input():
    global output
    output = input("Enter something to print!")
    printer.print(output)
    printer.feed(5)
    
while output != "EXIT":
    print_user_input()