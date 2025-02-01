import os
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from PIL import Image, ImageTk, ImageOps  # Import Pillow modules

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
        file_menu.add_command(label="New", command=lambda: self.execute_callback('dummy', 'New'))
        file_menu.add_command(label="Open", command=lambda: self.execute_callback('open'))
        file_menu.add_command(label="Save", command=lambda: self.execute_callback('save'))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: self.execute_callback('close'))

        # Add Edit menu
        edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=lambda: self.execute_callback('dummy', 'Undo'))
        edit_menu.add_command(label="Redo", command=lambda: self.execute_callback('dummy', 'Redo'))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.execute_callback('dummy', 'Cut'))
        edit_menu.add_command(label="Copy", command=lambda: self.execute_callback('dummy', 'Copy'))
        edit_menu.add_command(label="Paste", command=lambda: self.execute_callback('dummy', 'Paste'))

        # Add FTP menu
        ftp_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="FTP", menu=ftp_menu)
        ftp_menu.add_command(label="Connect", command=lambda: self.execute_callback('dummy', 'Connect'))
        ftp_menu.add_command(label="Disconnect", command=lambda: self.execute_callback('dummy', 'Disconnect'))
        ftp_menu.add_command(label="Upload", command=lambda: self.execute_callback('dummy', 'Upload'))
        ftp_menu.add_command(label="Download", command=lambda: self.execute_callback('dummy', 'Download'))

        # Add Tools menu
        tools_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Options", command=lambda: self.execute_callback('dummy', 'Options'))

        # Add Settings menu
        settings_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Preferences", command=lambda: self.execute_callback('dummy', 'Preferences'))

def dummy_command(button_name):
    """Displays the name of the button being clicked."""
    print(f"Button clicked: {button_name}")