import os
import tkinter as tk
from tkinter import ttk, messagebox
from menu import AppMenu
from treeview import FileTreeView
from texteditor import TextEditor
from imageviewer import ImageViewer
from pdfviewer import PDFViewer
from docxviewer import DocxViewer
import mimetypes

class Pylinq:
    def __init__(self, root):
        self.root = root
        self.root.title("PyLinq -- File Exploration App")
        self.current_path = os.path.expanduser("~")
        
        # Initialize mimetypes
        mimetypes.init()

        # Create a PanedWindow to hold the Treeview and content area
        self.main_paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=5)
        self.main_paned_window.pack(fill="both", expand=True)

        # Create a frame for the Treeview with enough space for horizontal scrollbar
        self.file_tree_frame = ttk.Frame(self.main_paned_window)
        self.main_paned_window.add(self.file_tree_frame, stretch="first", minsize=250)

        # Create a single content frame to hold the active viewer
        self.content_frame = ttk.Frame(self.main_paned_window)
        self.main_paned_window.add(self.content_frame, stretch="always", minsize=400)

        # Initialize the Treeview and all viewers
        self.file_tree = FileTreeView(self.file_tree_frame, self.open_file)
        
        # Initialize all viewers with the content frame as parent
        self.text_editor = TextEditor(self.content_frame)
        self.image_viewer = ImageViewer(self.content_frame)
        self.pdf_viewer = PDFViewer(self.content_frame)
        self.docx_viewer = DocxViewer(self.content_frame)

        # Initially hide all viewers
        self.text_editor.text_frame.pack_forget()
        self.image_viewer.image_frame.pack_forget()
        self.pdf_viewer.pdf_frame.pack_forget()
        self.docx_viewer.docx_frame.pack_forget()
        
        # Show the text editor initially
        self.show_text_editor()

        # Set up the menu
        self.menu = AppMenu(root, self.execute_callback)

        # Register callbacks
        self.callbacks = {}
        self.register_callbacks()
        
        # Set window size
        root.geometry("1200x800")
        
        # Set window icon
        try:
            icon_path = os.path.join("assets", "folder.png")
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                root.iconphoto(True, icon)
        except Exception as e:
            print(f"Error setting icon: {e}")
        
        # Bind keyboard shortcuts
        root.bind('<Control-s>', self.save_file)
        root.bind('<Control-q>', self.on_closing)
        root.bind('<Control-o>', self.open_file_dialog)
        
        # Set protocol for window close
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def register_callbacks(self):
        """Register all callbacks."""
        self.callbacks['save'] = self.save_file
        self.callbacks['open'] = self.open_file
        self.callbacks['open_dialog'] = self.open_file_dialog
        self.callbacks['close'] = self.on_closing
        self.callbacks['dummy'] = self.dummy_command

    def execute_callback(self, callback_name, *args, **kwargs):
        """Execute the callback based on the callback name."""
        if callback_name in self.callbacks:
            self.callbacks[callback_name](*args, **kwargs)
        else:
            print(f"No callback found for: {callback_name}")

    def open_file(self, path):
        """Open a file based on its type."""
        try:
            if not os.path.exists(path):
                messagebox.showerror("Error", f"File not found: {path}")
                return
                
            self.current_path = path
            
            # Determine file type
            mime_type, _ = mimetypes.guess_type(path)
            file_extension = os.path.splitext(path)[1].lower()
            
            if mime_type and mime_type.startswith('image/'):
                self.show_image_viewer()
                self.image_viewer.open_image(path)
            elif file_extension == '.pdf':
                self.show_pdf_viewer()
                self.pdf_viewer.open_pdf(path)
            elif file_extension == '.docx' or file_extension == '.doc':
                self.show_docx_viewer()
                self.docx_viewer.open_docx(path)
            elif os.path.isdir(path):
                # If it's a directory, just update the tree view
                messagebox.showinfo("Directory", f"Selected directory: {path}")
            else:
                # Default to text editor for all other files
                self.show_text_editor()
                self.text_editor.open_file(path)
        except Exception as e:
            messagebox.showerror("Error", f"Error opening file: {e}")

    def open_file_dialog(self, event=None):
        """Open a file dialog to select a file."""
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            initialdir=self.current_path,
            title="Select file",
            filetypes=(
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("PDF files", "*.pdf"),
                ("Word documents", "*.docx;*.doc")
            )
        )
        if path:
            self.open_file(path)

    def save_file(self, event=None):
        """Save the current file."""
        if self.current_path:
            try:
                # Check if we're in text editor mode
                if self.text_editor.text_frame.winfo_ismapped():
                    self.text_editor.save_file(self.current_path)
                    messagebox.showinfo("Success", f"File saved: {self.current_path}")
                else:
                    messagebox.showinfo("Info", "No text file is currently open for editing.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {e}")

    def on_closing(self, event=None):
        """Handle application closing."""
        try:
            self.text_editor.on_closing()
            self.image_viewer.on_closing()
            self.pdf_viewer.on_closing()
            self.docx_viewer.on_closing()
            self.root.destroy()
        except Exception as e:
            print(f"Error during closing: {e}")
            self.root.destroy()

    def dummy_command(self, button_name):
        """Placeholder for unimplemented commands."""
        messagebox.showinfo("Not Implemented", f"The '{button_name}' feature is not yet implemented.")

    def show_text_editor(self):
        """Show the text editor and hide the other viewers."""
        # Hide all viewers first
        self.text_editor.text_frame.pack_forget()
        self.image_viewer.image_frame.pack_forget()
        self.pdf_viewer.pdf_frame.pack_forget()
        self.docx_viewer.docx_frame.pack_forget()
        
        # Then show only the text editor
        self.text_editor.text_frame.pack(fill="both", expand=True)

    def show_image_viewer(self):
        """Show the image viewer and hide the other viewers."""
        # Hide all viewers first
        self.text_editor.text_frame.pack_forget()
        self.image_viewer.image_frame.pack_forget()
        self.pdf_viewer.pdf_frame.pack_forget()
        self.docx_viewer.docx_frame.pack_forget()
        
        # Then show only the image viewer
        self.image_viewer.image_frame.pack(fill="both", expand=True)
        
    def show_pdf_viewer(self):
        """Show the PDF viewer and hide the other viewers."""
        # Hide all viewers first
        self.text_editor.text_frame.pack_forget()
        self.image_viewer.image_frame.pack_forget()
        self.pdf_viewer.pdf_frame.pack_forget()
        self.docx_viewer.docx_frame.pack_forget()
        
        # Then show only the PDF viewer
        self.pdf_viewer.pdf_frame.pack(fill="both", expand=True)
        
    def show_docx_viewer(self):
        """Show the DOCX viewer and hide the other viewers."""
        # Hide all viewers first
        self.text_editor.text_frame.pack_forget()
        self.image_viewer.image_frame.pack_forget()
        self.pdf_viewer.pdf_frame.pack_forget()
        self.docx_viewer.docx_frame.pack_forget()
        
        # Then show only the DOCX viewer
        self.docx_viewer.docx_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = Pylinq(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"An unexpected error occurred: {e}")