import tkinter as tk
from ttkbootstrap import Style
from tkinter import ttk

class ExampleFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # Create a notebook widget
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Create the first tab containing the grid of buttons
        self.tab_names = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_names, text='Names')
        self.create_name_buttons()

        # Create the second tab containing the grid of locations
        self.tab_locations = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_locations, text='Locations')
        self.create_location_buttons()

    def create_name_buttons(self):
        # TODO: Create grid of buttons with names
        pass

    def create_location_buttons(self):
        # TODO: Create grid of buttons with locations
        pass

root = tk.Tk()
style = Style()
frame = ExampleFrame(root)
frame.pack(fill='both', expand=True)
root.mainloop()
