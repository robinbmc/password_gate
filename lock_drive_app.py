import tkinter as tk
from tkinter import messagebox, filedialog
import hashlib
import os
import subprocess
from cryptography.fernet import Fernet

# === SETTINGS ===
PASSWORD_FILE = "password.txt"
KEY_FILE = "key.key"

# === FUNCTIONS ===
def hide_file(filepath):
    try:
        subprocess.run(["attrib", "+h", filepath], check=True)
    except Exception as e:
        print(f"Failed to hide {filepath}: {e}")

def save_password(password):
    with open(PASSWORD_FILE, "w") as f:
        f.write(hash_password(password))
    hide_file(PASSWORD_FILE)

def save_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    hide_file(KEY_FILE)

def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_file(filepath, key):
    with open(filepath, 'rb') as f:
        data = f.read()
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)
    with open(filepath + '.enc', 'wb') as f:
        f.write(encrypted_data)
    os.remove(filepath)

def decrypt_file(filepath, key):
    with open(filepath, 'rb') as f:
        encrypted_data = f.read()
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)
    original_path = filepath[:-4]  # Strip '.enc'
    with open(original_path, 'wb') as f:
        f.write(decrypted_data)
    os.remove(filepath)

def encrypt_folder(folder_path, key):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath) and not filename.endswith('.enc'):
            encrypt_file(filepath, key)

def decrypt_folder(folder_path, key):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath) and filename.endswith('.enc'):
            decrypt_file(filepath, key)
def check_password():
    entered = password_entry.get()
    stored = load_password()
    if hash_password(entered) == stored:
        try:
            key = load_key()
            decrypt_folder(FOLDER_PATH, key)
            messagebox.showinfo("Access Granted", "Files decrypted and folder unlocked!")
            open_folder(FOLDER_PATH)
            login.destroy()
            logged_in_window()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt files: {e}")
    else:
        messagebox.showerror("Access Denied", "Wrong password!")

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
        try:
            key = load_key()
            decrypt_folder(FOLDER_PATH, key)
            messagebox.showinfo("Access Granted", "Files decrypted and folder unlocked!")
            open_folder(FOLDER_PATH)
            login.destroy()
            logged_in_window()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt files: {e}")
    else:
        messagebox.showerror("Access Denied", "Wrong password!")

    login = tk.Tk()
    login.title("Drive Access")

    tk.Label(login, text="Enter Password to Access Drive:").pack(pady=10)
    password_entry = tk.Entry(login, show="*", width=30)
    password_entry.pack(pady=5)
    tk.Button(login, text="Unlock", command=check_password).pack(pady=10)

    login.mainloop()

def logged_in_window():
    def lock_drive():
        try:
            key = load_key()
            encrypt_folder(FOLDER_PATH, key)
            messagebox.showinfo("Locked", "Files encrypted successfully.")
            logged_in.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt files: {e}")

    def change_password():
        def attempt_change():
            current = current_entry.get()
            new1 = new_entry.get()
            new2 = confirm_entry.get()
            if hash_password(current) != load_password():
                messagebox.showerror("Error", "Current password is incorrect!")
            elif new1 != new2:
                messagebox.showerror("Error", "New passwords do not match!")
            elif new1 == "":
                messagebox.showerror("Error", "New password cannot be empty!")
            else:
                save_password(new1)
                messagebox.showinfo("Success", "Password changed successfully.")
                change.destroy()

        change = tk.Toplevel()
        change.title("Change Password")

        tk.Label(change, text="Current Password:").pack(pady=5)
        current_entry = tk.Entry(change, show="*", width=30)
        current_entry.pack(pady=5)

        tk.Label(change, text="New Password:").pack(pady=5)
        new_entry = tk.Entry(change, show="*", width=30)
        new_entry.pack(pady=5)

        tk.Label(change, text="Confirm New Password:").pack(pady=5)
        confirm_entry = tk.Entry(change, show="*", width=30)
        confirm_entry.pack(pady=5)

        tk.Button(change, text="Change Password", command=attempt_change).pack(pady=10)

    logged_in = tk.Tk()
    logged_in.title("Drive Opened")

    tk.Label(logged_in, text="Folder is now unlocked.").pack(pady=10)
    tk.Button(logged_in, text="Lock Again", command=lock_drive).pack(pady=10)
    tk.Button(logged_in, text="Change Password", command=change_password).pack(pady=10)

    logged_in.mainloop()

# === MAIN ===
def select_folder():
    folder_selected = filedialog.askdirectory(title="Select Folder to Lock/Unlock")
    if not folder_selected:
        messagebox.showerror("Error", "No folder selected. Exiting.")
        exit()
    return folder_selected

if os.path.exists(PASSWORD_FILE) and os.path.exists(KEY_FILE):
    FOLDER_PATH = select_folder()
    login_window()
else:
    setup_password()

