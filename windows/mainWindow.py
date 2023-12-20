import os.path
import tkinter as tk
import tkinter.messagebox as msg
import utils.encryptation as encrypt
from playwright_process.main import startProcess


# Create a main window
class MainWindow(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        # Create a label
        self.label = tk.Label(self, text="Credenciales Teamwork")
        self.label.pack(side="top", fill="x", pady=10)

        # Create a username label
        self.username_label = tk.Label(self, text="Correo electrónico")
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

        # Create a start process button
        self.start_process_button = tk.Button(self, text="Iniciar Proceso", command=self.start_process)
        self.start_process_button.pack(side="top", fill="x", padx=50, pady=5)

        # Create a register button
        self.register_button = tk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterWindow"))
        self.register_button.pack(side="top", fill="x", padx=50, pady=5)

        # Validate saved credentials
        credentials = self.read_saved_credentials()

        if credentials:
            self.username_entry.insert(0, credentials[0])
            self.password_entry.insert(0, credentials[1])

    # Start process function
    def start_process(self):
        # Get the username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Save credentials
        self.save_credentials(username, password)

        # Clear the username and password entries
        # self.username_entry.delete(0, tk.END)
        # self.password_entry.delete(0, tk.END)

        # Show the process window
        self.controller.show_frame("ProcessWindow")

        # Start the process
        msg.showinfo("Iniciando Proceso", "El proceso de registro de tiempos está iniciando.\nPor favor, espere...")
        try:
            startProcess(username, password)
            msg.showinfo("Proceso terminado", "Los tiempos se han registrado correctamente.")
        except Exception as e:
            message = f"El proceso ha fallado por el siguiente motivo:\n{e}"
            print(message)
            msg.showerror("Error en el proceso", message)

        self.controller.show_frame("MainWindow")


    # Save credentials on a file
    def save_credentials(self, username, password):
        key_path = "data/key.key"
        credentials = "data/credentials.bin"
        data_to_encrypt = f"{username}:{password}"

        if not os.path.exists(key_path):
            encrypt.generate_key(key_path)

        encrypt_data = encrypt.encrypt_string(key_path, data_to_encrypt)

        with open(credentials, "wb") as file:
            file.write(encrypt_data)

    # Read saved credentials
    def read_saved_credentials(self):
        key_path = "data/key.key"
        credentials = "data/credentials.bin"

        if not os.path.exists(key_path):
            return None

        with open(credentials, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = encrypt.decrypt_string(key_path, encrypted_data)
        username, password = decrypted_data.split(":")

        return username, password