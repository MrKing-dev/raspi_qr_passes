import serial
import adafruit_thermal_printer

uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.00)
printer = ThermalPrinter(uart)
output = ""

def print_pass():
    global output
    printer.print(output)
    printer.feed(5)

if __name__ == "__main__":
    # Get pass data from POST request
    pass_data = os.environ["QUERY_STRING"]
    # Call the print_pass() function with pass data
    output = pass_data
    print_pass()
    output = ""
    # Return success message
    print("Content-type: text/html\n")
    print("Pass printed successfully!")
