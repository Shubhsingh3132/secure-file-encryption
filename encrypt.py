from cryptography.fernet import Fernet
from key_manager import generate_key

password = input("Enter password for encryption: ")
key = generate_key(password)
cipher = Fernet(key)

file_name = input("Enter file name to encrypt: ")

with open(file_name, "rb") as file:
    data = file.read()

encrypted_data = cipher.encrypt(data)

with open(file_name + ".enc", "wb") as file:
    file.write(encrypted_data)

print("✅ File encrypted successfully!")
