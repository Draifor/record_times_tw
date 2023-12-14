import tkinter as tk
from cryptography.fernet import Fernet


# Create a main window
class MainWindow(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        # Create a label
        self.label = tk.Label(self, text="Credenciales Teamwork")
        self.label.pack(side="top", fill="x", pady=10)

        # Create a username label
        self.username_label = tk.Label(self, text="Nombre de Usuario")
        self.username_label.pack(side="top", fill="x", pady=5)

        # Create a username entry
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(side="top", fill="x", padx=50, pady=5)

        # Create a password label
        self.password_label = tk.Label(self, text="Contraseña")
        self.password_label.pack(side="top", fill="x", pady=5)

        # Create a password entry
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(side="top", fill="x", padx=50, pady=5)

        # Create a login button
        self.login_button = tk.Button(self, text="Iniciar Proceso", command=self.login)
        self.login_button.pack(side="top", fill="x", padx=50, pady=5)

        # Create a register button
        self.register_button = tk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterWindow"))
        self.register_button.pack(side="top", fill="x", padx=50, pady=5)

    # Login function
    def login(self):
        # Get the username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username and password are correct
        if self.check_login(username, password):
            # Clear the username and password entries
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            # Show the main window
            self.controller.show_frame("MainWindow")
        else:
            # Clear the password entry
            self.password_entry.delete(0, tk.END)

    # Check if the username and password are correct
    def check_login(self, username, password):
        # Open the file containing the usernames and passwords
        with open("users.txt", "r") as file:
            # Loop through each line in the file
            for line in file:
                # Get the username and password from the line
                info = line.strip().split(",")
                file_username = info[0]
                file_password = info[1]

                # Check if the username and password are correct
                if username == file_username and password == file_password:
                    return True
        return False

    # Encrypt the password
    def encrypt_password(self, password):
        # Open the file containing the key
        with open("key.key", "rb") as file:
            key = file.read()

        # Encode the password
        encoded_password = password.encode()

        # Encrypt the password
        f = Fernet(key)
        encrypted_password = f.encrypt(encoded_password)

        return encrypted_password.decode()

    # Decrypt the password
    def decrypt_password(self, encrypted_password):
        # Open the file containing the key
        with open("key.key", "rb") as file:
            key = file.read()

        # Encode the password
        encoded_password = encrypted_password.encode()

        # Decrypt the password
        f = Fernet(key)
        decrypted_password = f.decrypt(encoded_password)

        return decrypted_password.decode()

# Create a register window
class RegisterWindow(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        # Create a label
        self.label = tk.Label(self, text="Register")
        self.label.pack(side="top", fill="x", pady=10)

        # Create a username label
        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack(side="top", fill="x", pady=5)

        # Create a username entry
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(side="top", fill="x", padx=50, pady=5)

        # Create a password label
        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack(side="top", fill="x", pady=5)

        # Create a password entry
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(side="top", fill="x", padx=50, pady=5)

        # Create a register button
        self.register_button = tk.Button(self, text="Register", command=self.register)
        self.register_button.pack(side="top", fill="x", padx=50, pady=5)

        # Create a back button
        self.back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("LoginWindow"))
        self.back_button.pack(side="top", fill="x", padx=50, pady=5)

    # Register function
    def register(self):
        # Get the username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username and password are valid
        if self.check_register(username, password):
            # Clear the username and password entries
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            # Show the login window
            self.controller.show_frame("LoginWindow")
        else:
            # Clear the password entry
            self.password_entry.delete(0, tk.END)

    # Check if the username and password are valid
    def check_register(self, username, password):
        # Check if the username is valid
        if self.check_username(username):
            # Check if the password is valid
            if self.check_password(password):
                # Encrypt the password
                encrypted_password = self.encrypt_password(password)

                # Open the file containing the usernames and passwords
                with open("users.txt", "a") as file:
                    # Write the username and password to the file
                    file.write(f"{username},{encrypted_password}\n")

                return True
        return False

    # Check if the username is valid
    def check_username(self, username):
        # Check if the username is at least 3 characters long
        if len(username) >= 3:
            # Check if the username is not already taken
            if not self.username_taken(username):
                return True
        return False

    # Check if the username is already taken
    def username_taken(self, username):
        # Open the file containing the usernames and passwords
        with open("users.txt", "r") as file:
            # Loop through each line in the file
            for line in file:
                # Get the username from the line
                info = line.strip().split(",")
                file_username = info[0]

                # Check if the username is already taken
                if username == file_username:
                    return True
        return False

    # Check if the password is valid
    def check_password(self, password):
        # Check if the password is at least 8 characters long
        if len(password) >= 8:
            return True
        return False

    # Encrypt the password
    def encrypt_password(self, password):
        # Open the file containing the key
        with open("key.key", "rb") as file:
            key = file.read()

        # Encode the password
        encoded_password = password.encode()

        # Encrypt the password
        f = Fernet(key)
        encrypted_password = f.encrypt(encoded_password)

        return encrypted_password.decode()

    # Decrypt the password
    def decrypt_password(self, encrypted_password):
        # Open the file containing the key
        with open("key.key", "rb") as file:
            key = file.read()

        # Encode the password
        encoded_password = encrypted_password.encode()

        # Decrypt the password
        f = Fernet(key)
        decrypted_password = f.decrypt(encoded_password)

        return decrypted_password.decode()


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
        for page in (MainWindow, RegisterWindow):
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

# Create the application
app = App()

# Run the application
app.mainloop()



