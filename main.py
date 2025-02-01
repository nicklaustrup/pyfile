import os
import tkinter as tk
from tkinter import ttk
from menu import AppMenu
from treeview import FileTreeView
from texteditor import TextEditor
from imageviewer import ImageViewer

class Pylinq:
    def __init__(self, root):
        self.root = root
        self.root.title("PyLinq -- File Exploration App")
        self.current_path = os.path.expanduser("~")

        # Create a PanedWindow to hold the Treeview and another PanedWindow
        self.main_paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_paned_window.pack(fill="both", expand=True)

        # Create a frame for the Treeview
        self.file_tree_frame = ttk.Frame(self.main_paned_window)
        self.main_paned_window.add(self.file_tree_frame, stretch="always")

        # Create a PanedWindow to hold the TextEditor and ImageViewer
        self.editor_paned_window = tk.PanedWindow(self.main_paned_window, orient=tk.HORIZONTAL)
        self.main_paned_window.add(self.editor_paned_window, stretch="always")

        # Initialize the Treeview, TextEditor, and ImageViewer
        self.file_tree = FileTreeView(self.file_tree_frame, self.open_file)
        self.text_editor = TextEditor(self.editor_paned_window)
        self.image_viewer = ImageViewer(self.editor_paned_window)

        # Add the TextEditor and ImageViewer to the PanedWindow
        self.editor_paned_window.add(self.text_editor.text_frame, stretch="always")
        self.editor_paned_window.add(self.image_viewer.image_frame, stretch="always")

        # Initially show the TextEditor and hide the ImageViewer
        self.show_text_editor()

        self.menu = AppMenu(root, self.execute_callback)

        self.callbacks = {}
        self.register_callbacks()
        
        root.bind('<Control-s>', self.save_file)

    def register_callbacks(self):
        """Register all callbacks."""
        self.callbacks['save'] = self.save_file
        self.callbacks['open'] = self.open_file
        self.callbacks['close'] = self.on_closing
        self.callbacks['dummy'] = self.dummy_command

    def execute_callback(self, callback_name, *args, **kwargs):
        """Execute the callback based on the callback name."""
        if callback_name in self.callbacks:
            self.callbacks[callback_name](*args, **kwargs)
        else:
            print(f"No callback found for: {callback_name}")

    def open_file(self, path):
        self.current_path = path
        if path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            self.show_image_viewer()
            self.image_viewer.open_image(path)
        else:
            self.show_text_editor()
            self.text_editor.open_file(path)

    def save_file(self, event=None):
        if self.current_path:
            try:
                self.text_editor.save_file(self.current_path)
            except IOError as e:
                print(f"Error saving file: {e}")

    def on_closing(self):
        self.text_editor.on_closing()
        self.image_viewer.on_closing()

    def dummy_command(self, button_name):
        print(f"Button clicked: {button_name}")

    def show_text_editor(self):
        """Show the text editor and hide the image viewer."""
        self.text_editor.text_frame.grid(row=0, column=1, sticky="nsew")
        self.image_viewer.image_frame.grid_forget()

    def show_image_viewer(self):
        """Show the image viewer and hide the text editor."""
        self.image_viewer.image_frame.grid(row=0, column=1, sticky="nsew")
        self.text_editor.text_frame.grid_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = Pylinq(root)
    root.mainloop()