import tkinter as tk
from tkinter import ttk, messagebox

class FindReplaceDialog(tk.Toplevel):
    def __init__(self, parent, text_area):
        super().__init__(parent)
        self.title("Find and Replace")
        self.text_area = text_area
        self.geometry("250x100")
        self.resizable(False, False)

        # Find
        ttk.Label(self, text="Find:").grid(
            row=0, column=0, sticky="w", 
            padx=5, pady=5)
        self.find_entry = ttk.Entry(self)
        self.find_entry.grid(row=0, column=1, padx=5, pady=5)

