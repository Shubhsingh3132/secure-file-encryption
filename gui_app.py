import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64, hashlib

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def process_file(action):
    file_path = filedialog.askopenfilename(title=f"Select file to {action}")
    password = password_entry.get()

    if not file_path or not password:
        messagebox.showerror("Error", "Please select a file and enter a password.")
        return

    key = generate_key(password)
    cipher = Fernet(key)

    try:
        with open(file_path, "rb") as file:
            data = file.read()

        if action == "encrypt":
            processed_data = cipher.encrypt(data)
            out_path = file_path + ".enc"
            msg = "File encrypted successfully! 🔒"
        else:
            processed_data = cipher.decrypt(data)
            out_path = file_path.replace(".enc", "") if file_path.endswith(".enc") else file_path + ".dec"
            msg = "File decrypted successfully! 🔓"

        with open(out_path, "wb") as file:
            file.write(processed_data)

        messagebox.showinfo("Success", msg)
        password_entry.delete(0, tk.END)

    except Exception:
        messagebox.showerror("Error", "Operation failed! Wrong password or corrupted file.")

def encrypt_file():
    process_file("encrypt")

def decrypt_file():
    process_file("decrypt")

# --- Modern GUI Setup ---
root = tk.Tk()
root.title("Secure File Encryption")
root.geometry("450x320")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# Fonts
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_SUBTITLE = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 11, "bold")
FONT_ENTRY = ("Segoe UI", 12)
FONT_BTN = ("Segoe UI", 11, "bold")

# Colors
BG_COLOR = "#1e1e2e"
TEXT_COLOR = "#cdd6f4"
MUTED_TEXT = "#a6adc8"
ENTRY_BG = "#313244"
ENTRY_FG = "#cdd6f4"
ACCENT_COLOR = "#89b4fa"
BTN_ENC_BG = "#a6e3a1"
BTN_ENC_HOVER = "#94cc90"
BTN_DEC_BG = "#f38ba8"
BTN_DEC_HOVER = "#d97c96"
BTN_FG_COLOR = "#11111b"

# Header
header_frame = tk.Frame(root, bg=BG_COLOR)
header_frame.pack(pady=(25, 15))

tk.Label(header_frame, text="SecureCrypt", font=FONT_TITLE, bg=BG_COLOR, fg=ACCENT_COLOR).pack()
tk.Label(header_frame, text="Encrypt and decrypt your files with ease", font=FONT_SUBTITLE, bg=BG_COLOR, fg=MUTED_TEXT).pack()

# Input Area
input_frame = tk.Frame(root, bg=BG_COLOR)
input_frame.pack(fill="x", padx=40, pady=10)

tk.Label(input_frame, text="Secret Password", font=FONT_LABEL, bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 5))

password_entry = tk.Entry(
    input_frame, 
    show="●", 
    font=FONT_ENTRY, 
    bg=ENTRY_BG, 
    fg=ENTRY_FG, 
    insertbackground=TEXT_COLOR,
    relief="flat", 
    highlightthickness=2, 
    highlightbackground=ENTRY_BG, 
    highlightcolor=ACCENT_COLOR
)
password_entry.pack(fill="x", ipady=6)

# Buttons Area
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(fill="x", padx=40, pady=20)

def create_button(parent, text, bg_col, hover_col, fg_col, command, side, padx):
    btn = tk.Button(
        parent, 
        text=text, 
        font=FONT_BTN, 
        bg=bg_col, 
        fg=fg_col, 
        activebackground=hover_col, 
        activeforeground=fg_col,
        relief="flat",
        cursor="hand2",
        command=command
    )
    btn.pack(side=side, fill="x", expand=True, padx=padx, ipady=8)
    
    # Hover Effects
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_col))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg_col))

create_button(btn_frame, "🔒 Encrypt", BTN_ENC_BG, BTN_ENC_HOVER, BTN_FG_COLOR, encrypt_file, tk.LEFT, (0, 5))
create_button(btn_frame, "🔓 Decrypt", BTN_DEC_BG, BTN_DEC_HOVER, BTN_FG_COLOR, decrypt_file, tk.RIGHT, (5, 0))

root.mainloop()
