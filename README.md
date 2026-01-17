# textedit-u0492257

## R1

### Opening and Saving Files
User can use the file system to create new files, open files, save files, or use save as. Clicking "open" or "new" prompts the user to save the current file if the file is currently not saved. However, there is no way to create, rename, or open files within the application's window as of now. The logic for this feature is handled in file_actions.py, and connected to the menu in menu_bar.py. These features were tested both by running the application and testing that documents were saved correctly and that the logic works as intended, and by running unit tests using pytests in test_file_acitons.py. 

### Keyboard Shortcuts
<img width="194" height="297" alt="Screenshot 2026-01-09 at 3 17 02 PM" src="https://github.com/user-attachments/assets/87668451-3ce8-49b5-8a22-900bc96ce806" />

Undo, Redo, Cut, Copy, Paste, and Select All were added as keyboard shortcuts, as well as to the edit menu. However, in the future I would like to add Ctrl+F to search for text, as well as other common shortcuts. These are handled in menu_bar.py. These shortcuts were all manually tested. 

### Editing and Selecting

This is handled by QPlainTextEdit from Qt, which allows the program to detect mouse movement, clicks, text input, etc. This feature was also manually tested.


## R2

### Multiple Tabs
User can now double click on the file explorer to open multiple tabs in the window, clicking on one to bring it to the front, and dragging them to reorder. Tabs can be closed until there is one left, and closing the final tab opens a new, empty, text file. Unit tests were added to check the functionality of closing and opening new tabs, and UI was tested manually.

### Split-Screen View
Current feature I am still in progress of working on. User can drag and drop tabs into different areas of the screen to automatically create a divided, split-screen view. Right now, there are some bugs with closing tabs, equally dividing the screen size, but the basic functionality is there and just needs a few tweaks. In the process of adding more tests to fix these bugs.



