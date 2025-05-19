# password_gate
This Python project is a lightweight graphical utility that allows users to protect access to a specific folder on their system using a password. The application provides a simple GUI where the user sets a password on first run, which is then required to access the folder on subsequent runs.

A fix was implemented to hide password.txt using the Windows attrib +h command. The fix involved:
- Adding a helper function hide_file() that runs the attrib +h system command
- Updating save_password() to automatically hide the file after creation
- This approach makes the file invisible to typical users in Windows Explorer and adds a layer of obscurity, preventing casual discovery or manipulation.

