import tkinter as tk
from windows.mainWindow import MainWindow
from windows.processWindow import ProcessWindow


# Create a class for the application
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Set the title
        self.title("Registrar Tiempos Teamwork")

        # Set the window size
        self.geometry("400x400")

        # Create a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Set the grid configuration
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a dictionary to store the frames
        self.frames = {}

        # Loop through each page
        for page in (MainWindow, ProcessWindow):
            # Create the frame
            frame = page(container, self)

            # Add it to the frames dictionary
            self.frames[page.__name__] = frame

            # Set the grid for the frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the main window
        self.show_frame("MainWindow")

    # Show a frame
    def show_frame(self, page):
        # Get the frame from the frames dictionary
        frame = self.frames[page]

        # Show the frame
        frame.tkraise()
