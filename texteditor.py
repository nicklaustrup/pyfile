import os
import tkinter as tk
from tkinter import ttk, Text, messagebox

class TextEditor:
    """
    A simple text editor class that provides functionalities to create, open, save, and close text files.
    """
    def __init__(self, parent):
        self.text_frame = ttk.Frame(parent)
        self.text_frame.grid(row=0, column=1, sticky="nsew")

        self.close_button = ttk.Button(self.text_frame, text="X", command=self.close_file)
        self.close_button.grid(row=0, column=1, sticky="ne")

        self.text_widget = Text(self.text_frame, wrap="none")
        self.text_widget.grid(row=1, column=0, sticky="nsew")

        text_v_scrollbar = ttk.Scrollbar(self.text_frame, orient="vertical", command=self.text_widget.yview)
        text_v_scrollbar.grid(row=1, column=1, sticky="ns")

        text_h_scrollbar = ttk.Scrollbar(self.text_frame, orient="horizontal", command=self.text_widget.xview)
        text_h_scrollbar.grid(row=2, column=0, sticky="ew")

        self.text_widget.configure(yscrollcommand=text_v_scrollbar.set, xscrollcommand=text_h_scrollbar.set)

        self.text_frame.grid_rowconfigure(1, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        self.current_file_path = None

    def open_file(self, path):
        """Opens the file within the program."""
        self.current_file_path = path
        self.text_widget.delete("1.0", "end")
        with open(path, "r") as file:
            self.text_widget.insert("1.0", file.read())

    def save_file(self, path=None):
        """Saves the current file."""
        if path is None:
            path = self.current_file_path
        if path:
            with open(path, "w") as file:
                file.write(self.text_widget.get("1.0", "end"))

    def close_file(self):
        """Closes the file and resets the text widget."""
        if self.text_widget.edit_modified():
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before closing?")
            if response:  # Yes
                self.save_file()
            elif response is None:  # Cancel
                return
        self.text_widget.delete("1.0", "end")
        self.current_file_path = None
        self.text_widget.edit_modified(False)

    def on_closing(self):
        """Handles the window close event."""
        if self.text_widget.edit_modified():
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before closing?")
            if response:  # Yes
                self.save_file()
                self.text_widget.edit_modified(False)
                self.text_frame.master.destroy()
            elif response is None:  # Cancel
                return
            else:  # No
                self.text_frame.master.destroy()
        else:
            self.text_frame.master.destroy()
