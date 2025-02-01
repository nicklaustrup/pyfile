import os
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from PIL import Image, ImageTk, ImageOps  # Import Pillow modules

from menu import build_app


class Pylinq:
    def __init__(self, root):
        self.root = root
        self.root.title("Filinq -- File Exploration App")
        self.current_path = os.path.expanduser("~")  # Start at home directory

        # Build the app
        build_app(self.root)

        # Create a style for the Treeview
        self.style = ttk.Style()
        self.style.configure("Treeview",
                             highlightthickness=0,
                             bd=0,
                             font=('Calibri', 11))  # Modify font and other properties
        self.style.configure("Treeview.Heading",
                             font=('Calibri', 13, 'bold'))  # Modify heading font
        self.style.map("Treeview",
                       background=[('selected', 'white')],
                       foreground=[('selected', 'black')])
        self.style.layout("Treeview.Item",
                          [('Treeitem.padding', {'sticky': 'nswe', 'children':
                              [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                               ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                               ('Treeitem.text', {'side': 'left', 'sticky': ''})]})])

        # Create a PanedWindow to hold the Treeview and Text widget
        self.paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True)

        # Frame for Treeview and Scrollbar
        frame = ttk.Frame(self.paned_window)
        self.paned_window.add(frame, stretch="always")

        # Set up tree view
        self.tree = ttk.Treeview(frame, style="Treeview")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add Scrollbar
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure Treeview to work with Scrollbar
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        self.tree.configure(xscrollcommand=h_scrollbar.set)

        # Configure grid weights to ensure proper resizing
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Create a frame for the text widget and the close button
        text_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(text_frame, stretch="always")

        # Create a close button
        self.close_button = ttk.Button(text_frame, text="X", command=self.close_file)
        self.close_button.grid(row=0, column=1, sticky="ne")

        # Create a Text widget for displaying file content
        self.text_widget = tk.Text(text_frame, wrap="none")
        self.text_widget.grid(row=1, column=0, sticky="nsew")
        
        # Add vertical and horizontal scrollbars to the Text widget
        text_v_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        text_v_scrollbar.grid(row=1, column=1, sticky="ns")

        text_h_scrollbar = ttk.Scrollbar(text_frame, orient="horizontal", command=self.text_widget.xview)
        text_h_scrollbar.grid(row=2, column=0, sticky="ew")

        self.text_widget.configure(yscrollcommand=text_v_scrollbar.set, xscrollcommand=text_h_scrollbar.set)

        # Configure grid weights to ensure proper resizing
        text_frame.grid_rowconfigure(1, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Set width and height
        root.wm_minsize(width=300, height=300)
        root.geometry("1200x800")

        # Load and resize icons
        self.folder_icon = self.resize_icon("folder.png", (16, 16))
        self.file_icon = self.resize_icon("file.png", (16, 16))
        self.open_folder_icon = self.resize_icon("open.png", (16, 16))

        # Populate the tree
        self.populate_tree(self.current_path)

        # Bind events
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<<TreeviewOpen>>", self.on_treeview_open)
        self.tree.bind("<<TreeviewClose>>", self.on_treeview_close)

    def resize_icon(self, path, size, padding=(5, 5)):
        """Resizes the icon to the specified size and returns a PhotoImage."""
        try:
            image = Image.open(path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            image_with_padding = ImageOps.expand(image, border=padding, fill=(255, 255, 255, 0))
            return ImageTk.PhotoImage(image_with_padding)
        except FileNotFoundError:
            print(f"Icon file not found: {path}")
            return None

    def populate_tree(self, path, parent=""):
        """Populates the tree view with the contents of the given path."""
        # Remove dummy child if it exists
        if parent and self.tree.get_children(parent):
            self.tree.delete(self.tree.get_children(parent)[0])
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                node = self.tree.insert(parent, "end", text=item, values=[item_path], image=self.folder_icon)
                self.tree.insert(node, "end")  # Add a dummy child to make the node expandable
            else:
                self.tree.insert(parent, "end", text=item, values=[item_path], image=self.file_icon)

    def on_double_click(self, event):
        """Handles double-click event on tree view."""
        item = self.tree.selection()[0]
        path = self.tree.item(item, "values")[0]
        if os.path.isdir(path):
            self.populate_tree(path, item)
        else:
            self.open_file(path)

    def open_file(self, path):
        """Opens the file within the program."""
        self.text_widget.delete("1.0", tk.END)
        with open(path, "r") as file:
            self.text_widget.insert("1.0", file.read())

    def close_file(self):
        """Closes the file and resets the text widget."""
        self.text_widget.delete("1.0", tk.END)

    def on_treeview_open(self, event):
        """Handles tree view open event to populate children and change icon."""
        item = self.tree.selection()[0]
        path = self.tree.item(item, "values")[0]
        # Check if the node has already been populated
        if len(self.tree.get_children(item)) == 1:
            # Remove the dummy child
            self.tree.delete(self.tree.get_children(item)[0])
            # Populate the children
            self.populate_tree(path, item)
        # Change the icon to open folder
        self.tree.item(item, image=self.open_folder_icon)

    def on_treeview_close(self, event):
        """Handles tree view close event to change icon back to closed folder."""
        item = self.tree.selection()[0]
        # Change the icon back to closed folder
        self.tree.item(item, image=self.folder_icon)
        

if __name__ == "__main__":
    root = tk.Tk()
    explorer = Pylinq(root)
    root.mainloop()
