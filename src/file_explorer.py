"""File Explorer module for the PyEd text editor application.

This module contains the FileExplorer class, which is a subclass 
of the ttk.Treeview widget. The FileExplorer class is used to display 
the file system directory structure in a tree-like format.
"""

import os
from tkinter import ttk

class FileExplorer(ttk.Treeview):
    def __init__(self, master, open_file_callback, **kwargs):
        """__init__ method for the FileExplorer class."""
        super().__init__(master, **kwargs)
        self.master = master
        self.open_file_callback = open_file_callback

        # Bindings
        self.bind("<Double-1>", self.on_double_click_or_enter)
        self.bind("<Return>", self.on_double_click_or_enter)

        # Populate the treeview
        self.populate_tree()


    def populate_tree(self, path="."):
        """Populate the treeview with the file system directory structure."""
        self.delete(*self.get_children())
        abspath = os.path.abspath(path)
        root_node = self.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath)


    def process_directory(self, parent, path):
        """Process a directory and its contents."""
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)


    def on_double_click_or_enter(self, event):
        """Handle the double click or enter key press event."""
        item = self.selection()[0]
        file_path = self.get_full_path(item)
        if os.path.isfile(file_path):
            self.open_file_callback(file_path)


    def get_full_path(self, item):
        """Get the full path of an item in the treeview."""
        path_parts = []
        while item:
            path_parts.insert(0, self.item(item)["text"])
            item = self.parent(item)
        return os.path.join(*path_parts)


    def refresh(self):
        """Refresh the treeview."""
        self.populate_tree()
