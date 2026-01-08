# Text Editor Architecture

## Design Philosophy

**Vintage Terminal Aesthetic + Modern Features**

Inspired by GNU nano and classic terminal editors:
- Dark background with syntax-highlighted text
- Bottom status bar showing file info, position, shortcuts
- Monospace font throughout
- Color scheme: dark teal/cyan background, colored text
- Keyboard-centric workflow

## Project Structure

```
textedit-u0492257/
├── design/                  # Design documentation
│   └── architecture.md
├── src/                     # Source code
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── editor/              # Core editor components
│   │   ├── __init__.py
│   │   ├── text_editor.py   # Main editor widget
│   │   └── document.py      # Document model (file state, modified tracking)
│   ├── ui/                  # UI components
│   │   ├── __init__.py
│   │   ├── main_window.py   # Main application window
│   │   ├── menu_bar.py      # Menu bar setup
│   │   └── status_bar.py    # Status bar (cursor position, file info)
│   └── actions/             # Actions and shortcuts
│       ├── __init__.py
│       └── file_actions.py  # Open, Save, Save As, New
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_editor.py       # Editor widget tests
│   ├── test_document.py     # Document model tests
│   ├── test_file_actions.py # File operation tests
│   └── conftest.py          # pytest fixtures
├── requirements.txt
├── pytest.ini
└── README.md
```

## Core Components

### 1. MainWindow (`ui/main_window.py`)
- Top-level QMainWindow
- Contains menu bar, text editor, status bar
- Handles window title (shows filename, modified indicator)
- Manages application lifecycle

### 2. TextEditor (`editor/text_editor.py`)
- Subclass of QPlainTextEdit
- Core editing functionality (provided by Qt)
- Emits signals for cursor position changes
- Text selection handling

### 3. Document (`editor/document.py`)
- Tracks current file path
- Tracks modified state
- Handles file I/O (open, save, save as)
- Manages unsaved changes prompts

### 4. MenuBar (`ui/menu_bar.py`)
- File menu: New, Open, Save, Save As, Exit
- Edit menu: Undo, Redo, Cut, Copy, Paste, Select All
- Connects actions to keyboard shortcuts

### 5. StatusBar (`ui/status_bar.py`)
- Displays cursor position (line:column)
- Displays file encoding/info

## Keyboard Shortcuts

| Action     | Shortcut       |
|------------|----------------|
| New        | Ctrl+N         |
| Open       | Ctrl+O         |
| Save       | Ctrl+S         |
| Save As    | Ctrl+Shift+S   |
| Undo       | Ctrl+Z         |
| Redo       | Ctrl+Y         |
| Cut        | Ctrl+X         |
| Copy       | Ctrl+C         |
| Paste      | Ctrl+V         |
| Select All | Ctrl+A         |
| Exit       | Ctrl+Q         |

## Data Flow

```
User Input → TextEditor → Document (track changes)
                ↓
            MainWindow (update title)
                ↓
            StatusBar (update position)
```

## File Operations

### Open File
1. Check for unsaved changes → prompt if needed
2. Show file dialog
3. Read file contents
4. Load into TextEditor
5. Update Document state (path, clean state)
6. Update window title

### Save File
1. If no path → trigger Save As
2. Write TextEditor contents to file
3. Mark Document as clean
4. Update window title

### New File
1. Check for unsaved changes → prompt if needed
2. Clear TextEditor
3. Reset Document state
4. Update window title

## Testing Strategy

- **Unit tests**: Document model, file operations
- **Widget tests**: TextEditor behavior, signal emissions
- **Integration tests**: Full workflow (open, edit, save)
- Use `pytest-qt` for Qt widget testing with `qtbot` fixture
