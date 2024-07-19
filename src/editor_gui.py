import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from text_editor import TextEditor
from find_replace_dialog import FindReplaceDialog

class EditorGUI:
    def __init__(self, root) -> None:
        self.root = root
        self.text_editor = TextEditor()
        self.draw_gui()

        # Update status bar
        self.update_status()

        # Check if the text area has been modified when closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def draw_gui(self) -> None:
        self.root.title("PyEd")

        # Set the window size
        window_width = 800
        window_height = 600
        self.root.geometry(f"{window_width}x{window_height}")

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the center position
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the position of the window to the center of the screen
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Text Area
        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind('<<Modified>>', self.text_modified_callback)
        self.ignore_modified = False # Prevents opening file from setting the modified flag

        # Create status bar frame
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(side='bottom', fill='x')

        # Status Bar Left: File info
        self.file_status_var = tk.StringVar()
        self.file_status_label = tk.Label(self.status_frame, textvariable=self.file_status_var, anchor='w')
        self.file_status_label.pack(side='left', fill='x', expand=True)
        
        # Status Bar Right: Position info
        self.position_status_var = tk.StringVar()
        self.position_status_label = tk.Label(self.status_frame, textvariable=self.position_status_var, anchor='e')
        self.position_status_label.pack(side='right', padx=(0, 10))

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
            command=lambda: self.text_area.event_generate("<<Undo>>"),
            accelerator="Ctrl+Z")
        edit_menu.add_command(
            label="Redo",
            command=lambda: self.text_area.event_generate("<<Redo>>"),
            accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cut",
            command=lambda: self.text_area.event_generate("<<Cut>>"),
            accelerator="Ctrl+X")
        edit_menu.add_command(
            label="Copy",
            command=lambda: self.text_area.event_generate("<<Copy>>"),
            accelerator="Ctrl+C")
        edit_menu.add_command(
            label="Paste",
            command=lambda: self.text_area.event_generate("<<Paste>>"),
            accelerator="Ctrl+V")
        edit_menu.add_command(
            label="Select All",
            command=lambda: self.text_area.event_generate("<<SelectAll>>"),
            accelerator="Ctrl+A")
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Find",
            command=self.find_text,
            accelerator="Ctrl+F")
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-S>", lambda e: self.save_file_as())
        self.root.bind("<Control-q>", lambda e: self.on_closing())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-x>", lambda e: self.cut())
        self.root.bind("<Control-c>", lambda e: self.copy())
        self.root.bind("<Control-v>", lambda e: self.paste())
        self.root.bind("<Control-a>", lambda e: self.select_all())
        self.root.bind("<Control-f>", lambda e: self.find_text())

    # Menu functions
    def new_file(self) -> None:
        self.text_editor.text_buffer = ""
        self.text_area.delete("1.0", "end")

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename()
        if file_path:
            self.ignore_modified = True
            self.text_editor.open_file(file_path)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", self.text_editor.text_buffer)
            self.ignore_modified = False
            self.text_area.edit_modified(False)

            # Update status bar
            self.update_status()

    def save_file(self) -> None:
        if self.text_editor.current_file:
            self.text_editor.text_buffer = self.text_area.get("1.0", "end")
            self.text_editor.save_file_as(self.text_editor.current_file)
            self.text_area.edit_modified(False)
            self.update_status()
        else:
            self.save_file_as()

    def save_file_as(self) -> None:
        file_path = filedialog.asksaveasfilename()
        if file_path:
            self.text_editor.text_buffer = self.text_area.get("1.0", "end")
            self.text_editor.save_file_as(file_path)
            self.text_area.edit_modified(False)
            self.update_status()
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

    def find_text(self, event=None):
        FindReplaceDialog(self.root, self.text_area)

    # TODO: Status bar functions:
    # - Set the current file name/modified status
    # - Set the current cursor position
    # - Set the current selection length
    # - Set the current line number
    # - Set the current column number
    # - Set the current word count

    def update_status(self):
        if self.text_editor.current_file:
            filename = self.text_editor.current_file.split("/")[-1]
            modified = " (modified)" if self.text_area.edit_modified() else ""
            file_status = f"{filename}{modified}"
        else:
            file_status = "Untitled"    
        self.file_status_var.set(file_status)

    def text_modified_callback(self, event):
        if self.text_area.edit_modified() and not self.ignore_modified:
            self.update_status()


    # TODO: Tabs