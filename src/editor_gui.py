import tkinter as tk
from tkinter import filedialog, messagebox
from text_editor import TextEditor

class EditorGUI:
    def __init__(self, root) -> None:
        self.root = root
        self.text_editor = TextEditor()
        self.draw_gui()
        
        # Check if the text area has been modified when closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def draw_gui(self) -> None:
        self.root.title("PyEd")
        self.root.geometry("800x600")

        # Window
        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(expand=True, fill="both")

        # Menu Bar
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # 1. File Menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="Open", 
            command=self.open_file, 
            accelerator="Ctrl+O")
        file_menu.add_command(
            label="New", 
            command=self.new_file, 
            accelerator="Ctrl+N")
        file_menu.add_command(
            label="Save", 
            command=self.save_file,
            accelerator="Ctrl+S")
        file_menu.add_command(
            label="Save as", 
            command=self.save_file_as,
            accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", 
            command=self.on_closing,
            accelerator="Ctrl+Q")

        # 2. Edit Menu
        edit_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(
            label="Undo", 
            command=self.text_area.event_generate("<<Undo>>"),
            accelerator="Ctrl+Z")
        edit_menu.add_command(
            label="Redo",
            command=self.text_area.event_generate("<<Redo>>"),
            accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cut",
            command=self.text_area.event_generate("<<Cut>>"),
            accelerator="Ctrl+X")
        edit_menu.add_command(
            label="Copy",
            command=self.text_area.event_generate("<<Copy>>"),
            accelerator="Ctrl+C")
        edit_menu.add_command(
            label="Paste",
            command=self.text_area.event_generate("<<Paste>>"),
            accelerator="Ctrl+V")
        
        
        # TODO: Might not need these?
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())

    def new_file(self) -> None:
        self.text_editor.text_buffer = ""
        self.text_area.delete("1.0", "end")

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename()
        if file_path:
            self.text_editor.open_file(file_path)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", self.text_editor.text_buffer)

            # TODO: Set "statusbar" label text to current file name instead
            self.root.title(f"PyEd | {self.text_editor.current_file}")

    def save_file(self) -> None:
        if self.text_editor.current_file:
            self.text_editor.text_buffer = self.text_area.get("1.0", "end")
            self.text_editor.save_file_as(self.text_editor.current_file)
            self.text_area.edit_modified(False)
            # TODO: Set "statusbar" label text to current file name + " saved"
        else:
            self.save_file_as()

    def save_file_as(self) -> None:
        file_path = filedialog.asksaveasfilename()
        if file_path:
            self.text_editor.text_buffer = self.text_area.get("1.0", "end")
            self.text_editor.save_file_as(file_path)
            self.text_area.edit_modified(False)
            # TODO: Set "statusbar" label text to current file name + " saved"

    def on_closing(self) -> None:
        if(self.text_area.edit_modified()):
            response = messagebox.askyesnocancel(
                "Save changes?", "Do you want to save changes before closing?")
            if response:
                self.save_file()
            elif response is None:
                return 
        self.root.destroy()
