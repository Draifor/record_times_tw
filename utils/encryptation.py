from cryptography.fernet import Fernet


# Encrypt string
def encrypt_string(path_key, string):
    # Open the file containing the key
    with open(path_key, "rb") as file:
        key = file.read()

    # Encode the string
    encoded_string = string.encode()

    # Encrypt the string
    f = Fernet(key)
    encrypted_string = f.encrypt(encoded_string)

    return encrypted_string

# Decrypt the string
def decrypt_string(path_key, encrypted_string):
    # Open the file containing the key
    with open(path_key, "rb") as file:
        key = file.read()

    # Decrypt the string
    f = Fernet(key)
    decrypted_string = f.decrypt(encrypted_string)

    return decrypted_string.decode()

# Generate a key
def generate_key(path_key):
    key = Fernet.generate_key()

    # Save the key to a file
    with open(path_key, "wb") as path_key:
        path_key.write(key)
