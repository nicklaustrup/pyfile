import os
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps  # Import Pillow modules

from config import configure_styles

class FileTreeView:
    def __init__(self, parent, open_file_callback):
        self.tree_frame = ttk.Frame(parent)
        self.tree_frame.pack(fill="both", expand=True)

        # Create a container frame for the treeview and vertical scrollbar
        self.tree_container = ttk.Frame(self.tree_frame)
        self.tree_container.pack(side="top", fill="both", expand=True)

        # Configure the treeview with show="tree" to only show items, not columns
        # Set the displaycolumns to an empty list to ensure horizontal scrolling works
        self.tree = ttk.Treeview(self.tree_container, style="Treeview", show="tree")
        self.tree.pack(side="left", fill="both", expand=True)

        self.open_file_callback = open_file_callback
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<<TreeviewOpen>>", self.on_treeview_open)
        self.tree.bind("<<TreeviewClose>>", self.on_treeview_close)
        # Add binding for single click to highlight selection
        self.tree.bind("<ButtonRelease-1>", self.on_item_select)
        # Add binding for window resize to update column width
        self.tree_frame.bind("<Configure>", self.on_frame_configure)

        self.folder_icon = self.resize_icon("./assets/folder.png", (16, 16))
        self.file_icon = self.resize_icon("./assets/file.png", (16, 16))
        self.open_folder_icon = self.resize_icon("./assets/open.png", (16, 16))

        # Create a style for the Treeview
        configure_styles()

        # Add Scrollbars
        self.create_scrollbar()
        
        # Populate the tree after everything is set up
        self.populate_drives()

    def on_frame_configure(self, event):
        """Handle frame resize events to adjust column width."""
        # Set the column width to a large value to ensure horizontal scrolling works
        # This ensures long filenames can be scrolled to view
        self.tree.column("#0", width=max(200, event.width - 20), stretch=False)
        
    def create_scrollbar(self):
        """Creates the scrollbars."""
        # Vertical scrollbar - placed in the tree_container frame
        v_scrollbar = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.tree.yview)
        v_scrollbar.pack(side="right", fill="y")
        
        # Horizontal scrollbar - placed directly in the tree_frame
        h_scrollbar = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Configure Treeview to work with both scrollbars
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Make sure the horizontal scrollbar is enabled by setting the column width
        # Set a large minwidth to ensure horizontal scrolling is enabled
        self.tree.column("#0", width=200, minwidth=300, stretch=False)

    def on_item_select(self, event):
        """Handles item selection to highlight the selected item."""
        # The selection is automatically handled by ttk.Treeview
        # We can add custom styling if needed
        pass

    def populate_drives(self):
        """Populates the tree view with the available drives."""
        drives = self.get_drives()
        for drive in drives:
            node = self.tree.insert("", "end", text=drive, values=[drive], image=self.folder_icon)
            self.tree.insert(node, "end")  # Add a dummy child to make the node expandable

    def get_drives(self):
        """Returns a list of available drives on the system."""
        drives = []
        for drive in range(ord('A'), ord('Z') + 1):
            drive_letter = f"{chr(drive)}:\\"
            if os.path.exists(drive_letter):
                drives.append(drive_letter)
        return drives

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
            self.open_file_callback(path)

    def on_treeview_open(self, event):
        """Handles tree view open event to populate children and change icon."""
        item = self.tree.selection()[0]
        path = self.tree.item(item, "values")[0]
        if len(self.tree.get_children(item)) == 1:
            self.tree.delete(self.tree.get_children(item)[0])
            self.populate_tree(path, item)
        self.tree.item(item, image=self.open_folder_icon)

    def on_treeview_close(self, event):
        """Handles tree view close event to change icon back to closed folder."""
        item = self.tree.selection()[0]
        self.tree.item(item, image=self.folder_icon)
        
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