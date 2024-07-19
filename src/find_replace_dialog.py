import tkinter as tk
from tkinter import ttk, messagebox

class FindReplaceDialog(tk.Toplevel):
    def __init__(self, parent, text_area):
        super().__init__(parent)
        self.text_area = text_area
        self.title("Find/Replace")
        self.transient(parent)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.draw_gui()

    def draw_gui(self):
        # Find
        ttk.Label(self, text="Find:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.find_var).grid(row=0, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        ttk.Button(self, text="Find Next", command=self.find_next).grid(row=0, column=3, sticky="w", padx=5, pady=5)

