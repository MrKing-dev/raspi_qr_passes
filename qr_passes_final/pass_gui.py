import tkinter as tk
import ttkbootstrap as ttkbs
from ttkbootstrap.constants import *
import threading
import qr_pass_generator as qr 

destinations = ["Guidance", "Library", "Office", "Auditorium", "Nurse", "Locker", "Restroom", "Classroom:___", "Other:_____"]



root = ttkbs.Window(themename="superhero")

main_frame = ttkbs.Frame(root)
main_frame.pack(pady=20)

button_frame = ttkbs.Frame(root)
button_frame.pack(pady=20)

bottom_frame = ttkbs.Frame(root)
bottom_frame.pack(pady=20)

#Name Label
name_label = ttkbs.Label(main_frame, bootstyle="info", text=qr.name, font=("Helvetica", 18))
name_label.pack()

#Scan QR Button
start_scan_btn = ttkbs.Button(main_frame, bootstyle="info-outline", text="Start Scan", command=lambda: threading.Thread(target=qr.qr_to_student).start())
start_scan_btn.pack(pady=15)

# create a 3x3 grid of buttons
for i in range(3):
    for j in range(3):
        index = i*3 + j
        if index < len(destinations):
            destination = destinations[index]
            b = ttkbs.Button(button_frame, text=destination, width=15, command=lambda x=destination: qr.update_destination(x))
            b.grid(row=i, column=j, padx=10, pady=10)

camera_feed_label = tk.Label(bottom_frame)
camera_feed_label.grid(row=0, column=0, padx=10, pady=10)

preview_pass_label = ttkbs.Label(bottom_frame, text=qr.output)
preview_pass_label.grid(row=0, column=1,  padx=10, pady=10)

print_pass_btn = ttkbs.Button(bottom_frame, text="Print Pass", width=12, bootstyle="success-outline", command=lambda: qr.print_pass())
print_pass_btn.grid(row=1, column=0, padx=10, pady=10)

reset_btn = ttkbs.Button(bottom_frame, text="Reset", width=12, bootstyle="danger-outline", command=lambda: qr.reset())
reset_btn.grid(row=1, column=1, padx=10, pady=10)

print("attempting to start camera")
qr.update_camera_feed(camera_feed_label)
root.mainloop()
