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
        self.replace_var = tk.StringVar()
        self.case_sensitive_var = tk.BooleanVar()

        # Draw GUI
        self.draw_gui()

    def draw_gui(self):
        # Find
        ttk.Label(self, text="Find:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.find_var).grid(
            row=0, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        ttk.Button(self, text="Find Next", command=self.find_next).grid(
            row=0, column=3, sticky="w", padx=5, pady=5)

        # Replace
        ttk.Label(self, text="Replace with:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.replace_var).grid(
            row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        ttk.Button(self, text="Replace", command=self.replace).grid(
            row=1, column=3, sticky="w", padx=5, pady=5)

        # Replace All
        ttk.Button(self, text="Replace All", command=self.replace_all).grid(
            row=2, column=2, columnspan=2, sticky="e", padx=5, pady=5)
        
        # Case Sensitive
        ttk.Checkbutton(self, text="Case sensitive", variable=self.case_sensitive_var).grid(
            row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    def find_next(self):
        search_text = self.find_var.get()
        if search_text:
            start_pos = self.text_area.search(
                search_text, self.text_area.index("insert"),
                nocase=not self.case_sensitive_var.get())
            if start_pos:
                end_pos = f"{start_pos}+{len(search_text)}c"
                self.text_area.tag_remove("search", "1.0", tk.END)
                self.text_area.tag_add("search", start_pos, end_pos)
                self.text_area.tag_config("search", background="green", foreground="white")
                self.text_area.mark_set("insert", end_pos)
                self.text_area.see("insert")
                return True
        messagebox.showinfo("Find", "No match found.")
        return False
    
    def replace(self):
        current_pos = self.text_area.index("search.first")
        self.text_area.delete("search.first", "search.last")
        self.text_area.insert(current_pos, self.replace_var.get())
        self.find_next()

    def replace_all(self):
        count = 0
        while self.find_next():
            self.replace()
            count += 1
        tk.messagebox.showinfo("Replace All", f"Replaced {count} occurrences.")

    # TODO: Make `find` modal appear in the same position in the main window and 
    # TODO: move with the main window (geometry method?)