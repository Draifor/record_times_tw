import tkinter as tk


# Create a register window
class ProcessWindow(tk.Frame):
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


