# password_gate
This Python project is a lightweight graphical utility that allows users to protect access to a specific folder on their system using a password. The application provides a simple GUI where the user sets a password on first run, which is then required to access the folder on subsequent runs.

Features
- Password protection for folder access
- SHA-256 hashed password storage
- Windows-based GUI using tkinter
- Automatic folder opening on successful login
- Minimal setup and no external dependencies required

A fix was implemented to hide password.txt using the Windows attrib +h command. The fix involved:
- Adding a helper function hide_file() that runs the attrib +h system command
- Updating save_password() to automatically hide the file after creation
- This approach makes the file invisible to typical users in Windows Explorer and adds a layer of obscurity, preventing casual discovery or manipulation.

