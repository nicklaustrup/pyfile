import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, parent):
        self.image_frame = ttk.Frame(parent)
        self.image_frame.grid(row=0, column=1, sticky="nsew")

        self.close_button = ttk.Button(self.image_frame, text="X", command=self.close_image)
        self.close_button.grid(row=0, column=1, sticky="ne")

        self.canvas = tk.Canvas(self.image_frame, bg="white")
        self.canvas.grid(row=1, column=0, sticky="nsew")
            
        v_scrollbar = ttk.Scrollbar(self.image_frame, orient="vertical", command=self.canvas.yview)
        v_scrollbar.grid(row=1, column=1, sticky="ns")

        h_scrollbar = ttk.Scrollbar(self.image_frame, orient="horizontal", command=self.canvas.xview)
        h_scrollbar.grid(row=2, column=0, sticky="ew")
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.image_frame.grid_rowconfigure(1, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.current_image_path = None
        self.current_image = None

    def open_image(self, path):
        """Opens the image within the program."""
        self.current_image_path = path
        self.current_image = Image.open(path)
        self.display_image()

    def display_image(self):
        """Displays the current image on the canvas."""
        self.canvas.delete("all")
        img_width, img_height = self.current_image.size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Resize image to fit canvas while maintaining aspect ratio
        if img_width > canvas_width or img_height > canvas_height:
            ratio = min(canvas_width / img_width, canvas_height / img_height)
            img_width = int(img_width * ratio)
            img_height = int(img_height * ratio)
            self.current_image = self.current_image.resize((img_width, img_height), Image.Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(self.current_image)
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=self.tk_image)

    def close_image(self):
        """Closes the image and resets the canvas."""
        self.canvas.delete("all")
        self.current_image_path = None
        self.current_image = None

    def on_closing(self):
        """Handles the window close event."""
        if self.current_image_path:
            response = messagebox.askyesnocancel("Close Image", "Do you want to close the current image?")
            if response:  # Yes
                self.close_image()
                self.image_frame.master.destroy()
            elif response is None:  # Cancel
                return
            else:  # No
                self.image_frame.master.destroy()
        else:
            self.image_frame.master.destroy()