import tkinter as tk
from tkinter import filedialog, messagebox
from text_editor import TextEditor

class EditorGUI:
    def __init__(self, root) -> None:
        self.root = root
        self.text_editor = TextEditor()
        self.draw_gui()

    def draw_gui(self) -> None:
        self.root.title("PyEd")
        self.root.geometry("800x600")

        # Window
        self.text_area = tk.Text(self.root)
        self.text_area.pack(expand=True, fill="both")

        # Menu Bar
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # File Menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save as", command=self.save_file_as)
        # file_menu.add_separator()

    def new_file(self) -> None:
        self.text_editor.text_buffer = ""
        self.text_area.delete("1.0", "end")

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename()
        if file_path:
            self.text_editor.open_file(file_path)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", self.text_editor.text_buffer)
            self.root.title(f"PyEd | {self.text_editor.current_file}")

    def save_file(self) -> None:
        if self.text_editor.current_file:
            self.text_editor.save_file_as(self.text_editor.current_file)
            messagebox.showinfo("Info", "File saved successfully")
        else:
            self.save_file_as()

    def save_file_as(self) -> None:
        file_path = filedialog.asksaveasfilename()
        if file_path:
            self.text_editor.save_file_as(file_path)
            messagebox.showinfo("Info", "File saved successfully")
