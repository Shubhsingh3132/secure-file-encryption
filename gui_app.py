import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64, hashlib

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_file():
    file_path = filedialog.askopenfilename()
    password = password_entry.get()

    if not file_path or not password:
        messagebox.showerror("Error", "Select file and enter password")
        return

    key = generate_key(password)
    cipher = Fernet(key)

    with open(file_path, "rb") as file:
        data = file.read()

    encrypted = cipher.encrypt(data)

    with open(file_path + ".enc", "wb") as file:
        file.write(encrypted)

    messagebox.showinfo("Success", "File encrypted successfully!")

def decrypt_file():
    file_path = filedialog.askopenfilename()
    password = password_entry.get()

    if not file_path or not password:
        messagebox.showerror("Error", "Select file and enter password")
        return

    key = generate_key(password)
    cipher = Fernet(key)

    try:
        with open(file_path, "rb") as file:
            data = file.read()

        decrypted = cipher.decrypt(data)
        original = file_path.replace(".enc", "")

        with open(original, "wb") as file:
            file.write(decrypted)

        messagebox.showinfo("Success", "File decrypted successfully!")

    except:
        messagebox.showerror("Error", "Wrong password or corrupted file")

# GUI Window
root = tk.Tk()
root.title("Secure File Encryption System")
root.geometry("400x250")

tk.Label(root, text="Secure File Encryption", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Enter Password").pack()
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)

tk.Button(root, text="Encrypt File", width=20, command=encrypt_file).pack(pady=5)
tk.Button(root, text="Decrypt File", width=20, command=decrypt_file).pack(pady=5)

root.mainloop()
