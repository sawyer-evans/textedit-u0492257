# textedit-u0492257

to run, "python3 run.py"

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


## R3

### Automatic indentation and bracket and quote matching
When typing left brackets, parentheses, or quotes, right side automatically goes to the right of the cursor. Pressing tab while cursor is to the left of the right bracket, or similar element, causes the cursor to jump to the right side of the right bracket. Additionally, when hitting return after a bracket or left parenthesis, the line is automatically indented. Additionally, if the user types a left element and immediately deletes it, the right element is also deleted, but not if the user selects the left element and deletes. While support to detect a specific language is not enabled, these features make coding in the text editor more natural for most programming languages.
<img width="269" height="58" alt="Screenshot 2026-01-21 at 1 54 32 PM" src="https://github.com/user-attachments/assets/5291308b-4729-4616-b1ac-f6d8a144d486" />

### Split Screen Reworked
I reprompted the code for split screen to get rid of previous bugs. Now, drag and drop equally divides the screen, and deleting tabs where that tab is the only one in a split-view causes the tabs on the other side of the split to take up the full window.


