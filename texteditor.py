import os
import tkinter as tk
from tkinter import ttk, Text, messagebox
import re

class LineNumbers(tk.Canvas):
    """A canvas that displays line numbers for a text widget."""
    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, **kwargs)
        self.text_widget = text_widget
        self.text_widget.bind('<KeyRelease>', self.on_key_release)
        self.text_widget.bind('<MouseWheel>', self.on_key_release)
        self.text_widget.bind('<Configure>', self.on_key_release)
        self.font = kwargs.get('font', ('Courier', 10))
        
    def on_key_release(self, event=None):
        self.redraw()
        
    def redraw(self):
        """Redraws the line numbers."""
        self.delete('all')
        
        # Get visible lines
        i = self.text_widget.index('@0,0')
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split('.')[0]
            self.create_text(2, y, anchor='nw', text=linenum, font=self.font, fill='#606366')
            i = self.text_widget.index(f'{i}+1line')

class TextEditor:
    """
    A simple text editor class that provides functionalities to create, open, save, and close text files.
    """
    def __init__(self, parent):
        self.text_frame = ttk.Frame(parent)
        self.text_frame.pack(fill="both", expand=True)

        # Create a header frame for the close button
        self.header_frame = ttk.Frame(self.text_frame)
        self.header_frame.pack(fill="x")
        
        # Create close button but don't show it initially
        self.close_button = ttk.Button(self.header_frame, text="X", command=self.close_file)
        # Don't pack the close button initially - it will be shown when a file is opened
        
        # Create a frame for line numbers and text widget
        self.editor_frame = ttk.Frame(self.text_frame)
        self.editor_frame.pack(fill="both", expand=True)
        
        # Create text widget first
        self.text_widget = Text(self.editor_frame, wrap="none", undo=True, 
                               font=('Courier', 10))
        self.text_widget.pack(side="right", fill="both", expand=True)
        
        # Create line numbers widget with text_widget parameter
        self.line_numbers = LineNumbers(self.editor_frame, self.text_widget, width=30, bg='#f0f0f0')
        self.line_numbers.pack(side="left", fill="y")
        
        # Configure line numbers font
        self.line_numbers.font = ('Courier', 10)
        
        # Configure tags for syntax highlighting
        self.text_widget.tag_configure("keyword", foreground="#0000FF")
        self.text_widget.tag_configure("string", foreground="#008000")
        self.text_widget.tag_configure("comment", foreground="#808080", font=('Courier', 10, 'italic'))
        self.text_widget.tag_configure("function", foreground="#800080")
        self.text_widget.tag_configure("number", foreground="#FF8000")
        
        # Add scrollbars
        self.add_scrollbars()
        
        # Bind events for syntax highlighting
        self.text_widget.bind('<KeyRelease>', self.highlight_syntax)

        # Add keyboard shortcuts
        self.text_widget.bind('<Control-s>', lambda e: self.save_file())
        self.text_widget.bind('<Control-o>', lambda e: self.open_file())
        self.text_widget.bind('<Control-z>', lambda e: self.text_widget.edit_undo())
        self.text_widget.bind('<Control-y>', lambda e: self.text_widget.edit_redo())

        self.current_file_path = None
        
    def add_scrollbars(self):
        """Add scrollbars to the text widget."""
        # Create a frame for the vertical scrollbar
        v_scroll_frame = ttk.Frame(self.editor_frame)
        v_scroll_frame.pack(side="right", fill="y")
        
        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(v_scroll_frame, orient="vertical", command=self.text_widget.yview)
        v_scrollbar.pack(fill="y", expand=True)
        
        # Create a frame for the horizontal scrollbar
        h_scroll_frame = ttk.Frame(self.text_frame)
        h_scroll_frame.pack(side="bottom", fill="x")
        
        # Create horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(h_scroll_frame, orient="horizontal", command=self.text_widget.xview)
        h_scrollbar.pack(fill="x", expand=True)
        
        # Configure the text widget to use the scrollbars
        self.text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    def open_file(self, path=None):
        """Opens the file within the program."""
        if path is None:
            return
            
        self.current_file_path = path
        self.text_widget.delete("1.0", "end")
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_widget.insert("1.0", content)
                self.highlight_syntax()
                self.line_numbers.redraw()
                
                # Show the close button when a file is opened
                self.close_button.pack(side="right")
        except UnicodeDecodeError:
            # Try with a different encoding or handle binary files
            messagebox.showinfo("Binary File", "This appears to be a binary file and cannot be displayed.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening file: {str(e)}")

    def save_file(self, path=None):
        """Saves the current file."""
        if path is None:
            path = self.current_file_path
        if path:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(self.text_widget.get("1.0", "end-1c"))
                self.text_widget.edit_modified(False)
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")
                return False
        return False

    def close_file(self):
        """Closes the file and resets the text widget."""
        if self.text_widget.edit_modified():
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before closing?")
            if response:  # Yes
                if not self.save_file():
                    return  # Don't close if save failed
            elif response is None:  # Cancel
                return
        self.text_widget.delete("1.0", "end")
        self.current_file_path = None
        self.text_widget.edit_modified(False)
        self.line_numbers.redraw()
        
        # Hide the close button when file is closed
        self.close_button.pack_forget()

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
            
    def highlight_syntax(self, event=None):
        """Apply syntax highlighting to the text."""
        # Remove existing tags
        for tag in ["keyword", "string", "comment", "function", "number"]:
            self.text_widget.tag_remove(tag, "1.0", "end")
            
        # Get file extension to determine language
        if not self.current_file_path:
            return
            
        file_ext = os.path.splitext(self.current_file_path)[1].lower()
        
        # Define patterns based on file type
        patterns = {
            "keyword": [],
            "string": [r'"[^"\\]*(?:\\.[^"\\]*)*"', r"'[^'\\]*(?:\\.[^'\\]*)*'"],
            "comment": [],
            "function": [],
            "number": [r'\b\d+\b']
        }
        
        # Python specific patterns
        if file_ext == '.py':
            patterns["keyword"] = [r'\b(and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b']
            patterns["comment"] = [r'#.*']
            patterns["function"] = [r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)\b', r'\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)\b']
        
        # JavaScript/HTML/CSS patterns
        elif file_ext in ['.js', '.html', '.css']:
            patterns["keyword"] = [r'\b(var|let|const|function|return|if|else|for|while|do|switch|case|break|continue|try|catch|finally|throw|new|delete|typeof|instanceof|void|this|super|class|extends|import|export|default|async|await)\b']
            patterns["comment"] = [r'//.*', r'/\*[\s\S]*?\*/']
            patterns["function"] = [r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)\b']
        
        # Apply highlighting
        content = self.text_widget.get("1.0", "end-1c")
        for tag, regexes in patterns.items():
            for regex in regexes:
                for match in re.finditer(regex, content):
                    start = f"1.0+{match.start()}c"
                    end = f"1.0+{match.end()}c"
                    self.text_widget.tag_add(tag, start, end)
        
        # Update line numbers
        self.line_numbers.redraw()
