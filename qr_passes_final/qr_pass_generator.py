from datetime import datetime
import os.path
import csv
import cv2
import time
import printer_output
import tkinter as tk
import ttkbootstrap as ttkbs
from ttkbootstrap.constants import *
import threading
from PIL import ImageTk, Image

vid = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

path = './SignoutList2022.csv'
output = []


name = "Your Name Here"
destination = "Please Select a Destination"
origin = "Mr. King Room 53"
now = None
timestamp = "Timestamp Printed Here"
output = "Preview Here"

def update_name_label():
    name_label.config(text=name)

def update_output_label():
    preview_pass_label.config(text=output)

def update_camera_feed():
    ret, frame = vid.read()    
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((320, 240))  # Resize the image to fit in the UI
        img = ImageTk.PhotoImage(img)
        camera_feed_label.config(image=img)
        camera_feed_label.image = img
        camera_feed_label.after(10, update_camera_feed)  # Update the camera feed every 10 milliseconds

# Define a callback function to update the "destination" variable
def update_destination(dest):
    global destination
    global output
    
    destination = dest
    output = f'''Name: {name}
Destination: {destination}
Origin: {origin}'''
    update_output_label()

def reset():
    global name
    global output
    
    name = "Your Name Here"
    output = "Preview Here"
    #destination_var.set("Destination")  # Set destination dropdown to default value
    update_name_label()
    update_output_label()

def get_current_timestamp():
    global now
    now=datetime.now()
    timestamp = now.strftime("%B %d, %Y %H:%M:%S")
    return timestamp

def print_pass():
    global now
    global timestamp
    global output

    timestamp = get_current_timestamp()
    pass_info = f'''Name: {name}
Destination: {destination}
Origin: {origin}
Timestamp: {timestamp}'''
    update_output_label()
    printer_output.output = pass_info
    printer_output.print_pass()
    output = [timestamp, name, destination, origin, "OUT"]
    with open(path, 'a', newline='') as csv_file:
        my_writer = csv.writer(csv_file, delimiter=',')
        my_writer.writerow(output)
    reset()

def qr_to_student():
    global name
    global destination
    global output
    global path
    
    name="Scanning..."
    update_name_label()
    
    if os.path.isfile(path) == False:
        with open(path, 'w', newline='') as csv_file:
            my_writer = csv.writer(csv_file, delimiter=',')
            my_writer.writerow(['Time Out', 'Name', 'Destination', 'Origin', 'Time In'])

    with open('StudentList2022.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_data = list(csv_reader)  # Convert csv_reader to a list

        while True:
            ret, frame = vid.read()
            if not ret:
                print("Failed to read frame from camera")
                return

            data, bbox, straight_qrcode = detector.detectAndDecode(frame)
            if len(data) > 0:
                student_number = data.strip()
                found = False
                for row in csv_data:  # Iterate over csv_data list instead of csv_reader
                    if row[0] == student_number:
                        name = f'{row[2]} {row[1]}'
                        found = True
                        update_name_label()
                        
                        # Check if "Time In" is "OUT" and update it if needed
                        with open(path, 'r', newline='') as signout_file:
                            signout_reader = csv.reader(signout_file, delimiter=',')
                            signout_data = list(signout_reader)
                            for signout_row in signout_data:
                                if signout_row[1] == name and signout_row[4] == "OUT":
                                    output = f"Signing {name} Back In"
                                    update_output_label()
                                    time.sleep(2)
                                    signout_row[4] = get_current_timestamp()                                    

                                    with open(path, 'w', newline='') as signout_file:
                                        signout_writer = csv.writer(signout_file)
                                        signout_writer.writerows(signout_data)
                                        reset()
                                        break

                            
                            
                        break

                if found:
                    break
                else:
                    name = "Student not found"
                    update_name_label()
                    csv_file.seek(0)


###USER INTERFACE CODE BELOW###
                    
destinations = ["Guidance", "Library", "Office", "Auditorium", "Nurse", "Locker", "Restroom", "Classroom:___", "Other:_____"]



root = ttkbs.Window(themename="darkly")

main_frame = ttkbs.Frame(root)
main_frame.pack(pady=20)

button_frame = ttkbs.Frame(root)
button_frame.pack(pady=20)

bottom_frame = ttkbs.Frame(root)
bottom_frame.pack(pady=20)

#Name Label
name_label = ttkbs.Label(main_frame, bootstyle="info", text=name, font=("Helvetica", 18))
name_label.pack()

#Scan QR Button
start_scan_btn = ttkbs.Button(main_frame, bootstyle="info-outline", text="Start Scan", command=lambda: threading.Thread(target=qr_to_student).start())
start_scan_btn.pack(pady=15)

# create a 3x3 grid of buttons
for i in range(3):
    for j in range(3):
        index = i*3 + j
        if index < len(destinations):
            destination = destinations[index]
            b = ttkbs.Button(button_frame, text=destination, width=15, command=lambda x=destination: update_destination(x))
            b.grid(row=i, column=j, padx=10, pady=10)

camera_feed_label = tk.Label(bottom_frame)
camera_feed_label.pack(padx=10, pady=10)

preview_pass_label = ttkbs.Label(bottom_frame, text=output)
preview_pass_label.pack(padx=10, pady=10)

print_pass_btn = ttkbs.Button(bottom_frame, text="Print Pass", width=12, bootstyle="success-outline", command=lambda: print_pass())
print_pass_btn.pack(padx=10, pady=10)

reset_btn = ttkbs.Button(bottom_frame, text="Reset", width=12, bootstyle="danger-outline", command=lambda: reset())
reset_btn.pack(padx=10, pady=10)

print("attempting to start camera")
update_camera_feed()

root.mainloop()

     

# Release the video capture object
vid.release()
cv2.destroyAllWindows()
