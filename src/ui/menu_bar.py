"""Menu bar setup."""

from PyQt6.QtGui import QAction, QKeySequence


def setup_menu_bar(main_window, file_actions):
    """Configure the menu bar with File and Edit menus."""
    menu_bar = main_window.menuBar()
    
    # File menu
    file_menu = menu_bar.addMenu("&File")
    
    new_action = QAction("&New", main_window)
    new_action.setShortcut(QKeySequence.StandardKey.New)
    new_action.triggered.connect(file_actions.new_file)
    file_menu.addAction(new_action)
    
    open_action = QAction("&Open...", main_window)
    open_action.setShortcut(QKeySequence.StandardKey.Open)
    open_action.triggered.connect(lambda: file_actions.open_file())
    file_menu.addAction(open_action)
    
    file_menu.addSeparator()
    
    save_action = QAction("&Save", main_window)
    save_action.setShortcut(QKeySequence.StandardKey.Save)
    save_action.triggered.connect(file_actions.save_file)
    file_menu.addAction(save_action)
    
    save_as_action = QAction("Save &As...", main_window)
    save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
    save_as_action.triggered.connect(file_actions.save_file_as)
    file_menu.addAction(save_as_action)
    
    file_menu.addSeparator()
    
    exit_action = QAction("E&xit", main_window)
    exit_action.setShortcut(QKeySequence.StandardKey.Quit)
    exit_action.triggered.connect(main_window.close)
    file_menu.addAction(exit_action)
    
    return {
        "new": new_action,
        "open": open_action,
        "save": save_action,
        "save_as": save_as_action,
        "exit": exit_action,
    }
