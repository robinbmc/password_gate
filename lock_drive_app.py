import tkinter as tk
from tkinter import messagebox
import hashlib
import os

# === SETTINGS ===
FOLDER_PATH = r"D:\MyPrivateStuff"
PASSWORD_FILE = "password.txt"

# === FUNCTIONS ===
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_password(password):
    with open(PASSWORD_FILE, "w") as f:
        f.write(hash_password(password))

def load_password():
    with open(PASSWORD_FILE, "r") as f:
        return f.read()

def password_exists():
    return os.path.exists(PASSWORD_FILE)

def open_folder(path):
    try:
        os.startfile(path)  # Windows only
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open: {e}")

# --- SETUP PASSWORD (First time only)
def setup_password():
    def save_new_password():
        p1 = entry1.get()
        p2 = entry2.get()
        if p1 != p2:
            messagebox.showerror("Error", "Passwords do not match!")
        elif p1 == "":
            messagebox.showerror("Error", "Password cannot be empty!")
        else:
            save_password(p1)
            messagebox.showinfo("Success", "Password set! Please restart the app.")
            setup.destroy()

    setup = tk.Tk()
    setup.title("Set Your Password")

    tk.Label(setup, text="Enter New Password:").pack(pady=5)
    entry1 = tk.Entry(setup, show="*", width=30)
    entry1.pack(pady=5)

    tk.Label(setup, text="Confirm Password:").pack(pady=5)
    entry2 = tk.Entry(setup, show="*", width=30)
    entry2.pack(pady=5)

    tk.Button(setup, text="Save Password", command=save_new_password).pack(pady=10)

    setup.mainloop()

# --- LOGIN WINDOW
def login_window():
    def check_password():
        entered = password_entry.get()
        stored = load_password()
        if hash_password(entered) == stored:
            messagebox.showinfo("Access Granted", "Welcome!")
            open_folder(FOLDER_PATH)
            login.destroy()
        else:
            messagebox.showerror("Access Denied", "Wrong password!")

    login = tk.Tk()
    login.title("Drive Access")

    tk.Label(login, text="Enter Password to Access Drive:").pack(pady=10)
    password_entry = tk.Entry(login, show="*", width=30)
    password_entry.pack(pady=5)
    tk.Button(login, text="Unlock", command=check_password).pack(pady=10)

    login.mainloop()

# === MAIN ===
if password_exists():
    login_window()
else:
    setup_password()
