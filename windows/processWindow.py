import tkinter as tk


# Create a register window
class ProcessWindow(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        # Create a label
        self.label = tk.Label(self, text="Ya te estoy registrando los tiempos.\nTu relájate y disfruta.")
        self.label.pack(side="top", fill="x", pady=10)

        # Create a username label
        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack(side="top", fill="x", pady=5)

        # Create a password label
        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack(side="top", fill="x", pady=5)

