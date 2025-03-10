import tkinter as tk
from tkinter import ttk
from tkinter import Menu

class AppMenu:
    def __init__(self, root, execute_callback):
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)
        self.execute_callback = execute_callback
        self.create_menus()

    def create_menus(self):
        # Add File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: self.execute_callback('dummy', 'New'), accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=lambda: self.execute_callback('open_dialog'), accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=lambda: self.execute_callback('save'), accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=lambda: self.execute_callback('dummy', 'Save As'), accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: self.execute_callback('close'), accelerator="Ctrl+Q")

        # Add Edit menu
        edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=lambda: self.execute_callback('dummy', 'Undo'), accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=lambda: self.execute_callback('dummy', 'Redo'), accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.execute_callback('dummy', 'Cut'), accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=lambda: self.execute_callback('dummy', 'Copy'), accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=lambda: self.execute_callback('dummy', 'Paste'), accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", command=lambda: self.execute_callback('dummy', 'Find'), accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace...", command=lambda: self.execute_callback('dummy', 'Replace'), accelerator="Ctrl+H")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=lambda: self.execute_callback('dummy', 'Select All'), accelerator="Ctrl+A")

        # Add View menu
        view_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=lambda: self.execute_callback('dummy', 'Zoom In'), accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=lambda: self.execute_callback('dummy', 'Zoom Out'), accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom", command=lambda: self.execute_callback('dummy', 'Reset Zoom'), accelerator="Ctrl+0")
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Line Numbers", command=lambda: self.execute_callback('dummy', 'Toggle Line Numbers'))
        view_menu.add_command(label="Toggle Word Wrap", command=lambda: self.execute_callback('dummy', 'Toggle Word Wrap'))

        # Add Tools menu
        tools_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="File Search", command=lambda: self.execute_callback('dummy', 'File Search'), accelerator="Ctrl+Shift+F")
        tools_menu.add_command(label="Directory Search", command=lambda: self.execute_callback('dummy', 'Directory Search'))
        tools_menu.add_separator()
        tools_menu.add_command(label="Options", command=lambda: self.execute_callback('dummy', 'Options'))

        # Add Help menu
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=lambda: self.execute_callback('dummy', 'Documentation'), accelerator="F1")
        help_menu.add_command(label="Keyboard Shortcuts", command=lambda: self.execute_callback('dummy', 'Keyboard Shortcuts'))
        help_menu.add_separator()
        help_menu.add_command(label="About", command=lambda: self.show_about_dialog())
    
    def show_about_dialog(self):
        """Show the about dialog."""
        about_window = tk.Toplevel()
        about_window.title("About PyLinq")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        # Make the window modal
        about_window.transient(about_window.master)
        about_window.grab_set()
        
        # Add content
        ttk.Label(
            about_window, 
            text="PyLinq File Explorer", 
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        ttk.Label(
            about_window, 
            text="A simple file explorer application built with Python and Tkinter."
        ).pack(pady=5)
        
        ttk.Label(
            about_window, 
            text="Version 1.0.0"
        ).pack(pady=5)
        
        ttk.Label(
            about_window, 
            text="© 2023 PyLinq Team"
        ).pack(pady=5)
        
        # Close button
        ttk.Button(
            about_window, 
            text="Close", 
            command=about_window.destroy
        ).pack(pady=20)
        
        # Center the window
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Wait for the window to be closed
        about_window.wait_window()

def dummy_command(button_name):
    """Displays the name of the button being clicked."""
    print(f"Button clicked: {button_name}")