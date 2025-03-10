import os
import tkinter as tk
from tkinter import ttk, messagebox
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PIL import Image, ImageTk

class PDFViewer:
    """A viewer for PDF documents."""
    def __init__(self, parent):
        self.pdf_frame = ttk.Frame(parent)
        self.pdf_frame.pack(fill="both", expand=True)

        # Create a header frame for the close button
        self.header_frame = ttk.Frame(self.pdf_frame)
        self.header_frame.pack(fill="x")
        
        # Create close button but don't show it initially
        self.close_button = ttk.Button(self.header_frame, text="X", command=self.close_pdf)
        # Don't pack the close button initially - it will be shown when a PDF is opened
        
        # Create navigation frame for page controls
        self.nav_frame = ttk.Frame(self.pdf_frame)
        self.nav_frame.pack(fill="x", side="bottom")
        
        # Create previous page button
        self.prev_button = ttk.Button(self.nav_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side="left", padx=5, pady=5)
        
        # Create page indicator label
        self.page_label = ttk.Label(self.nav_frame, text="Page: 0/0")
        self.page_label.pack(side="left", padx=5, pady=5)
        
        # Create next page button
        self.next_button = ttk.Button(self.nav_frame, text="Next", command=self.next_page)
        self.next_button.pack(side="left", padx=5, pady=5)
        
        # Create a frame for the canvas and scrollbars
        self.canvas_frame = ttk.Frame(self.pdf_frame)
        self.canvas_frame.pack(fill="both", expand=True)

        # Create canvas to display PDF pages
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)
            
        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        v_scrollbar.pack(side="right", fill="y")

        # Create horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(self.pdf_frame, orient="horizontal", command=self.canvas.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Configure canvas to work with scrollbars
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Initialize variables
        self.current_pdf_path = None
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.page_images = []
        self.current_image = None
        
        # Hide navigation frame initially
        self.nav_frame.pack_forget()
        
        # Bind resize event
        self.canvas.bind("<Configure>", self.on_resize)

    def open_pdf(self, path):
        """Opens the PDF document."""
        try:
            self.current_pdf_path = path
            self.pdf_document = PdfReader(path)
            self.total_pages = len(self.pdf_document.pages)
            self.current_page = 0
            
            # Show the close button and navigation frame
            self.close_button.pack(side="right")
            self.nav_frame.pack(fill="x", side="bottom")
            
            # Update page label
            self.update_page_label()
            
            # Load and display the first page
            self.load_page(0)
        except Exception as e:
            messagebox.showerror("Error", f"Error opening PDF: {str(e)}")
    
    def load_page(self, page_num):
        """Loads and displays a specific page."""
        if not self.pdf_document or page_num < 0 or page_num >= self.total_pages:
            return
        
        try:
            # Convert PDF page to image
            images = convert_from_path(
                self.current_pdf_path, 
                first_page=page_num+1, 
                last_page=page_num+1
            )
            
            if images:
                self.current_page = page_num
                self.display_page(images[0])
                self.update_page_label()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading page: {str(e)}")
    
    def display_page(self, page_image):
        """Displays the current page image on the canvas."""
        self.canvas.delete("all")
        
        # Resize image to fit canvas while maintaining aspect ratio
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 600
        
        img_width, img_height = page_image.size
        
        # Calculate scale factor to fit the image in the canvas
        scale = min(canvas_width / img_width, canvas_height / img_height)
        
        # Resize the image
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        resized_image = page_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage and display
        self.current_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(
            canvas_width // 2, canvas_height // 2,
            anchor="center", image=self.current_image
        )
        
        # Configure canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def update_page_label(self):
        """Updates the page indicator label."""
        self.page_label.config(text=f"Page: {self.current_page + 1}/{self.total_pages}")
    
    def next_page(self):
        """Navigates to the next page."""
        if self.current_page < self.total_pages - 1:
            self.load_page(self.current_page + 1)
    
    def prev_page(self):
        """Navigates to the previous page."""
        if self.current_page > 0:
            self.load_page(self.current_page - 1)
    
    def on_resize(self, event):
        """Handle window resize events."""
        if self.current_page is not None and 0 <= self.current_page < self.total_pages:
            # Reload the current page to resize it
            self.load_page(self.current_page)
    
    def close_pdf(self):
        """Closes the PDF document and resets the viewer."""
        self.canvas.delete("all")
        self.current_pdf_path = None
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.current_image = None
        
        # Hide the close button and navigation frame
        self.close_button.pack_forget()
        self.nav_frame.pack_forget()
        
        # Reset page label
        self.page_label.config(text="Page: 0/0")
    
    def on_closing(self):
        """Handles the window close event."""
        if self.current_pdf_path:
            response = messagebox.askyesnocancel("Close PDF", "Do you want to close the current PDF?")
            if response:  # Yes
                self.close_pdf()
                self.pdf_frame.master.destroy()
            elif response is None:  # Cancel
                return
            else:  # No
                self.pdf_frame.master.destroy()
        else:
            self.pdf_frame.master.destroy() 