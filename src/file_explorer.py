"""File Explorer module for the PyEd text editor application.

This module contains the FileExplorer class, which is a subclass 
of the ttk.Treeview widget. The FileExplorer class is used to display 
the file system directory structure in a tree-like format.
"""

import os
from tkinter import ttk

class FileExplorer(ttk.Treeview):
    def __init__(self, master, **kwargs):
        """__init__ method for the FileExplorer class."""
        super().__init__(master, **kwargs)
        self.master = master

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

    def refresh(self):
        """Refresh the treeview."""
        self.populate_tree()
