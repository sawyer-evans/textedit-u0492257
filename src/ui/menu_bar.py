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
    
    # Edit menu
    edit_menu = menu_bar.addMenu("&Edit")
    
    # Use lambdas to get the current editor dynamically
    def get_editor():
        return main_window.editor
    
    undo_action = QAction("&Undo", main_window)
    undo_action.setShortcut(QKeySequence.StandardKey.Undo)
    undo_action.triggered.connect(lambda: get_editor() and get_editor().undo())
    edit_menu.addAction(undo_action)
    
    redo_action = QAction("&Redo", main_window)
    redo_action.setShortcut(QKeySequence.StandardKey.Redo)
    redo_action.triggered.connect(lambda: get_editor() and get_editor().redo())
    edit_menu.addAction(redo_action)
    
    edit_menu.addSeparator()
    
    cut_action = QAction("Cu&t", main_window)
    cut_action.setShortcut(QKeySequence.StandardKey.Cut)
    cut_action.triggered.connect(lambda: get_editor() and get_editor().cut())
    edit_menu.addAction(cut_action)
    
    copy_action = QAction("&Copy", main_window)
    copy_action.setShortcut(QKeySequence.StandardKey.Copy)
    copy_action.triggered.connect(lambda: get_editor() and get_editor().copy())
    edit_menu.addAction(copy_action)
    
    paste_action = QAction("&Paste", main_window)
    paste_action.setShortcut(QKeySequence.StandardKey.Paste)
    paste_action.triggered.connect(lambda: get_editor() and get_editor().paste())
    edit_menu.addAction(paste_action)
    
    edit_menu.addSeparator()
    
    select_all_action = QAction("Select &All", main_window)
    select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
    select_all_action.triggered.connect(lambda: get_editor() and get_editor().selectAll())
    edit_menu.addAction(select_all_action)
    
    # View menu
    view_menu = menu_bar.addMenu("&View")
    
    toggle_explorer_action = QAction("Toggle &Explorer", main_window)
    toggle_explorer_action.setShortcut("Ctrl+B")
    toggle_explorer_action.triggered.connect(main_window.toggle_file_explorer)
    view_menu.addAction(toggle_explorer_action)
    
    return {
        "new": new_action,
        "open": open_action,
        "save": save_action,
        "save_as": save_as_action,
        "exit": exit_action,
        "undo": undo_action,
        "redo": redo_action,
        "cut": cut_action,
        "copy": copy_action,
        "paste": paste_action,
        "select_all": select_all_action,
        "toggle_explorer": toggle_explorer_action,
    }
