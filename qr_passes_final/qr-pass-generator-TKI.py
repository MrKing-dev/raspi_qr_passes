from datetime import datetime
import os.path
import csv
import cv2
import threading
import time
import tkinter as tk
import printer_output
from tkinter import ttk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
from utils import destinations  # Import destinations list from utils.py


vid = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

path = './SignoutList2022.csv'
output = []


name = "Your Name Here"
destination = "Please Select a Destination"
origin = "Room 53"
now = None
timestamp = "Timestamp Printed Here"
output = "Info"

def update_name_label():
    name_label.config(text=name)

def update_timestamp_label():
    timestamp_label.config(text=timestamp)

def update_output_label():
    output_label.config(text=output)

def update_camera_feed():
    ret, frame = vid.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((640, 480))  # Resize the image to fit in the UI
        img = ImageTk.PhotoImage(img)
        camera_feed_label.config(image=img)
        camera_feed_label.image = img
        camera_feed_label.after(10, update_camera_feed)  # Update the camera feed every 10 milliseconds

# Define a callback function to update the "destination" variable
def update_destination(*args):
    global destination
    destination = destination_var.get()

def reset():
    global name
    global timestamp
    global output
    name = "Your Name Here"
    timestamp = "Timestamp Printed Here"
    output = "Info"
    destination_var.set("Destination")  # Set destination dropdown to default value
    update_name_label()
    update_timestamp_label()
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
    update_timestamp_label()
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
    
    name="Scanning..."
    update_name_label()

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



if os.path.isfile(path) == False:
    with open(path, 'w', newline='') as csv_file:
        my_writer = csv.writer(csv_file, delimiter=',')
        my_writer.writerow(['Time Out', 'Name', 'Destination', 'Origin', 'Time In'])

# Create tkinter window
root = tk.Tk()
root.title("QR Code Scanner")
root.configure(bg="#333333")  # Set background color

# Set ttk style
style = ttk.Style()
style.theme_use("clam")  # Choose a ttk theme (e.g., 'clam', 'winnative', 'vista', etc.)
style.configure(".", background="#333333", foreground="white")  # Set default background and foreground color
style.configure("TLabel", font=("Helvetica", 24))  # Set font for labels
style.configure("TCombobox", font=("Helvetica", 18), width=20)  # Set font and width for combobox
style.configure("TCombobox.OptionMenu", padding=10, background="#555555", foreground="white")  # Set background and foreground color for dropdown options
style.map("TCombobox.OptionMenu", fieldbackground=[("readonly", "#555555")], background=[("readonly", "#555555")])  # Set background color for read-only state
style.map("TCombobox.OptionMenu.Label", foreground=[("readonly", "white")])  # Set foreground color for read-only state


# Create custom TButton style with hover and click indications
style.configure("TButton",
                background="#555555",  # Set background color
                foreground="white",  # Set foreground color
                padding=10,  # Add padding
                width=20,  # Set width
                bordercolor="#333333",  # Set border color
                focuscolor="#666666",  # Set focus color
                lightcolor="#999999",  # Set light color
                darkcolor="#111111",  # Set dark color
                )

style.map("TButton",
         background=[("active", "#777777"), ("pressed", "#888888")],  # Set background color for active and pressed state
         foreground=[("active", "white"), ("pressed", "white")],  # Set foreground color for active and pressed state
         bordercolor=[("active", "#666666"), ("pressed", "#666666")],  # Set border color for active and pressed state
         )

# Top text display
name_label = ttk.Label(root, text="Name", style="TLabel")
name_label.pack(pady=10)  # Add margin

# QR Code Scan button
qr_button = ttk.Button(root, text="Scan QR Code", style="TButton", command=lambda: threading.Thread(target=qr_to_student).start())
qr_button.pack(pady=10)

# Destination selection dropdown
destination_var = tk.StringVar()
destination_var.set("Destination")
destination_var.trace('w', update_destination)  # Add a trace to detect changes in the dropdown
destination_dropdown = ttk.Combobox(root, textvariable=destination_var, values=destinations, style="TCombobox")
destination_dropdown.pack(pady=10)

# Timestamp display
timestamp_label = ttk.Label(root, text="Timestamp Printed Here", style="TLabel")
timestamp_label.pack(pady=10)

# Output display
output_label = ttk.Label(root, text="Pass Printed Here", style="TLabel", wraplength=600)
output_label.pack(pady=10)

# Camera feed display
camera_feed_label = ttk.Label(root)
camera_feed_label.pack()

# Print pass button
print_button = ttk.Button(root, text="Print Pass", style="TButton", command=print_pass)
print_button.pack(pady=10)

# Reset button
reset_button = ttk.Button(root, text="Reset", style="TButton", command=reset)
reset_button.pack(pady=10)
# Start updating the camera feed
update_camera_feed()

root.mainloop()



# Release the video capture object
vid.release()
cv2.destroyAllWindows()
