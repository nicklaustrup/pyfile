import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, parent):
        self.image_frame = ttk.Frame(parent)
        self.image_frame.pack(fill="both", expand=True)

        # Create a header frame for the close button
        self.header_frame = ttk.Frame(self.image_frame)
        self.header_frame.pack(fill="x")
        
        # Create close button but don't show it initially
        self.close_button = ttk.Button(self.header_frame, text="X", command=self.close_image)
        # Don't pack the close button initially - it will be shown when an image is opened

        # Create a frame for the canvas and scrollbars
        self.canvas_frame = ttk.Frame(self.image_frame)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)
            
        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        v_scrollbar.pack(side="right", fill="y")

        # Create horizontal scrollbar
        h_scrollbar_frame = ttk.Frame(self.image_frame)
        h_scrollbar_frame.pack(side="bottom", fill="x")
        
        h_scrollbar = ttk.Scrollbar(h_scrollbar_frame, orient="horizontal", command=self.canvas.xview)
        h_scrollbar.pack(fill="x")
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.current_image_path = None
        self.current_image = None
        self.tk_image = None
        self.image_id = None
        
        # Bind resize event
        self.canvas.bind("<Configure>", self.on_resize)
        
        # Add zoom functionality
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)  # Windows
        self.canvas.bind("<Button-4>", self.on_mousewheel)    # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_mousewheel)    # Linux scroll down
        
        self.zoom_factor = 1.0

    def open_image(self, path):
        """Opens the image within the program."""
        self.current_image_path = path
        self.current_image = Image.open(path)
        self.original_image = self.current_image.copy()
        self.zoom_factor = 1.0
        
        # Show the close button when an image is opened
        self.close_button.pack(side="right")
        
        self.display_image()

    def display_image(self):
        """Displays the current image on the canvas."""
        if not self.current_image:
            return
            
        self.canvas.delete("all")
        img_width, img_height = self.current_image.size
        canvas_width = self.canvas.winfo_width() or 800  # Default if not yet rendered
        canvas_height = self.canvas.winfo_height() or 600  # Default if not yet rendered

        # Resize image to fit canvas while maintaining aspect ratio
        if img_width > canvas_width or img_height > canvas_height:
            ratio = min(canvas_width / img_width, canvas_height / img_height)
            img_width = int(img_width * ratio)
            img_height = int(img_height * ratio)
            self.current_image = self.original_image.resize(
                (img_width, img_height), Image.Resampling.LANCZOS
            )

        self.tk_image = ImageTk.PhotoImage(self.current_image)
        self.image_id = self.canvas.create_image(
            canvas_width // 2, canvas_height // 2, 
            anchor="center", image=self.tk_image
        )
        
        # Configure canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_resize(self, event):
        """Handle window resize events."""
        if self.current_image and self.original_image:
            # Reset zoom factor on resize
            self.zoom_factor = 1.0
            self.current_image = self.original_image.copy()
            self.display_image()
    
    def on_mousewheel(self, event):
        """Handle mouse wheel events for zooming."""
        if not self.current_image:
            return
            
        # Determine zoom direction
        if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
            # Zoom in
            self.zoom_factor *= 1.1
        elif event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):
            # Zoom out
            self.zoom_factor *= 0.9
        
        # Apply zoom
        new_width = int(self.original_image.width * self.zoom_factor)
        new_height = int(self.original_image.height * self.zoom_factor)
        
        if new_width > 10 and new_height > 10:  # Prevent too small images
            self.current_image = self.original_image.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )
            
            # Update display
            self.canvas.delete("all")
            self.tk_image = ImageTk.PhotoImage(self.current_image)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            self.image_id = self.canvas.create_image(
                canvas_width // 2, canvas_height // 2, 
                anchor="center", image=self.tk_image
            )
            
            # Update scrollregion
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def close_image(self):
        """Closes the image and resets the canvas."""
        self.canvas.delete("all")
        self.current_image_path = None
        self.current_image = None
        self.original_image = None
        self.tk_image = None
        self.image_id = None
        self.zoom_factor = 1.0
        
        # Hide the close button when image is closed
        self.close_button.pack_forget()

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