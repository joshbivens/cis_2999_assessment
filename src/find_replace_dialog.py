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

        # Variables
        self.find_var = tk.StringVar()

        # Draw GUI
        self.draw_gui()

    def draw_gui(self):
        # Find
        ttk.Label(self, text="Find:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.find_var).grid(row=0, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        ttk.Button(self, text="Find Next", command=self.find_next).grid(row=0, column=3, sticky="w", padx=5, pady=5)

    def find_next(self):
        search_text = self.find_var.get()
        if search_text:
            start_pos = self.text_area.search(search_text, self.text_area.index(tk.INSERT))
            if start_pos:
                end_pos = f"{start_pos}+{len(search_text)}c"
                self.text_area.tag_remove("search", "1.0", tk.END)
                self.text_area.tag_add("search", start_pos, end_pos)
                self.text_area.tag_config("search", background="yellow")
                self.text_area.mark_set(tk.INSERT, end_pos)
                self.text_area.see(tk.INSERT)
                return True
        return False