from datetime import datetime
import os.path
import csv
import time
import printer_output
import tkinter as tk
import ttkbootstrap as ttkbs
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
import threading
import class_lists as cl
from PIL import ImageTk, Image


signout_path = './SignoutList2022.csv'
output = []
class_displayed = "Period 1"
class_name = "period_1"
current_frame = 0


name = "Your Name Here"
destination = "Please Select a Destination"
origin = "Mr. King Room 53"
now = None
timestamp = "Timestamp Printed Here"
output = "Preview Here"


def update_output_label():
    output_label.config(text=output)
    
def switch_class(class_name):
    switcher = {
        "Period 1": "period_1",
        "Period 2": "period_2",
        "Period 3": "period_3",
        "Period 4": "period_4",
        "Period 5": "period_5",
        "Period 6": "period_6",
        "PRO CERT": "pro_cert",
        "Homeroom": "homeroom"
    }
    return switcher.get(class_name, "Invalid class")
    

def reset():
    global name
    global output
    global class_displayed
    
    output="Preview Here"
    update_output_label()
    destroy_widgets_in_frame(id_frame)
        
    class_displayed = "Period 1"
    name = "Your Name Here"
    output = "Preview Here"

def get_current_timestamp():
    global now
    now=datetime.now()
    timestamp = now.strftime("%B %d, %Y %H:%M:%S")
    return timestamp

def print_pass():
    global timestamp
    global output

    timestamp = get_current_timestamp()
    pass_info = f'''Name: {name}
Destination: {destination}
Origin: {origin}
Timestamp: {timestamp}'''
    printer_output.output = pass_info
    printer_output.print_pass()
    output = [timestamp, name, destination, origin, "OUT"]
    with open(signout_path, 'a', newline='') as csv_file:
        my_writer = csv.writer(csv_file, delimiter=',')
        my_writer.writerow(output)
    reset()

def number_to_student(student_number, signout_path):
    found = False

    if os.path.isfile(signout_path) == False:
        with open(signout_path, 'w', newline='') as csv_file:
            my_writer = csv.writer(csv_file, delimiter=',')
            my_writer.writerow(['Time Out', 'Name', 'Destination', 'Origin', 'Time In'])

    with open('StudentList2022.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:  # Iterate over csv_data list instead of csv_reader
            print(f"Checking row {row}")
            print(student_number)
            print(row[0])
            if row[0] == str(student_number):
                print("Match found!")
                name=row[2] + ' ' + row[1]
                print(f"name variable set correctly - {name}")
                found = True
                
                # Check if "Time In" is "OUT" and update it if needed
                with open(signout_path, 'r', newline='') as signout_file:
                    signout_reader = csv.reader(signout_file, delimiter=',')
                    signout_data = list(signout_reader)
                    for signout_row in signout_data:
                        if signout_row[1] == name and signout_row[4] == "OUT":
                            signout_row[4] = get_current_timestamp()                                    

                            with open(signout_path, 'w', newline='') as signout_file:
                                signout_writer = csv.writer(signout_file, delimiter=',')
                                signout_writer.writerows(signout_data)
                                toast = ToastNotification(title="Signing Back In", message=f"{name} signed back in at {get_current_timestamp()}", duration=3000)
                                toast.show_toast()

                                reset()
                return name
        
        


###USER INTERFACE CODE BELOW###
                    
destinations = ["Guidance", "Library", "Office", "Auditorium", "Nurse", "Locker", "Restroom", "Classroom:___", "Other:_____"]
classes = ["Period 1", "Period 2", "Period 3", "Period 4", "Period 5", "Period 6", "PRO CERT", "Homeroom"]

root = ttkbs.Window(title="Mr. King's Signout Page", themename="superhero", scaling=3.0)

period_frame = ttkbs.Frame(root)
id_frame = ttkbs.Frame(root)
dest_frame = ttkbs.Frame(root)
output_frame = ttkbs.Frame(root)
period_frame.pack(pady=10)
id_frame.pack(pady=10)
dest_frame.pack(pady=10)
output_frame.pack(pady=10)

###FUNCTION DEFINITIONS FOR BUTTONS###

def update_class(x, btn):
    global class_name
    global class_displayed
    
    if btn.bootstyle == "success-outline":
        btn.configure(bootstyle="success")
    else:
        btn.configure(bootstyle="success-outline")
    
    class_displayed = x
    class_name = switch_class(x)
    create_id_grid()
    print(f"Input={x}")
    print(class_displayed)
    print(class_name)

def update_student(x, btn):
    global name
    
    if btn.bootstyle == "primary-outline":
        btn.configure(bootstyle="primary")
    else:
        btn.configure(bootstyle="primary-outline")
    
    new_name = number_to_student(x, signout_path)
    name = new_name
    print(x)
    print(new_name)
    print(name)

def update_destination(dest, btn):
    global destination
    global output
    
    if btn.bootstyle == "light-outline":
        btn.configure(bootstyle="light")
    else:
        btn.configure(bootstyle="light-outline")
    
    destination = dest
    output = f'''Name: {name}
Destination: {destination}
Origin: {origin}'''
    update_output_label()
    print(dest)
    print(output)

#create a grid of buttons for the class periods
for i in range(2):
    for j in range(4):
        index = i*4 + j
        
        class_name = classes[index]
        b = ttkbs.Button(period_frame, text=class_name, width=15, bootstyle="success-outline", command=lambda x=class_name: update_class(x))
        b.grid(row=i, column=j, padx=10, pady=10)
            
#create 4x5 grid of buttons with student numbers
def create_id_grid():
    for i in range(3):
        for j in range(7):
            index = i*7 + j
            if index < len(getattr(cl, class_name)):
                b = ttkbs.Button(id_frame, text=getattr(cl, class_name)[index], width=10, bootstyle="primary-outline", command=lambda x=getattr(cl, class_name)[index]: update_student(x))
                b.grid(row=i, column=j, padx=10, pady=10)

def destroy_widgets_in_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
   

# create a 3x3 grid of buttons for the destinations
for i in range(2):
    for j in range(5):
        index = i*5 + j
        if index < len(destinations):
            destination = destinations[index]
            b = ttkbs.Button(dest_frame, text=destination, width=15, bootstyle="light-outline", command=lambda x=destination: update_destination(x))
            b.grid(row=i, column=j, padx=10, pady=10)
        
output_label = ttkbs.Label(output_frame, text=output, bootstyle="info")
output_label.pack(pady=20)
print_pass_btn = ttkbs.Button(output_frame, text="Print Pass", width=12, bootstyle ="warning", command=lambda: print_pass())
print_pass_btn.pack(padx=10, pady=10)
reset_btn = ttkbs.Button(output_frame, text="Reset", width=12, bootstyle ="danger", command=lambda: reset())
reset_btn.pack(padx=10, pady=10)



root.mainloop()

