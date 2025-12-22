from cryptography.fernet import Fernet
from key_manager import generate_key

password = input("Enter password for decryption: ")
key = generate_key(password)
cipher = Fernet(key)

file_name = input("Enter encrypted file name: ")

with open(file_name, "rb") as file:
    encrypted_data = file.read()

try:
    decrypted_data = cipher.decrypt(encrypted_data)
    original_name = file_name.replace(".enc", "")

    with open(original_name, "wb") as file:
        file.write(decrypted_data)

    print("✅ File decrypted successfully!")

except:
    print("❌ Incorrect password or corrupted file")
