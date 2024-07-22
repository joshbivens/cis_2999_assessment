import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import font
from text_editor import TextEditor
from find_replace_dialog import FindReplaceDialog
from syntax_highlighted_text import SyntaxHighlightedText

class EditorGUI:
    def __init__(self, root) -> None:
        self.root = root
        self.text_editor = TextEditor()

        # Variables
        self.show_line_numbers = tk.IntVar(value=1)
        self.file_status_var = tk.StringVar()
        self.position_status_var = tk.StringVar()
        self.current_theme = tk.StringVar(value="default")
        self.ignore_modified = False

        # Check if the text area has been modified when closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize GUI
        self.draw_gui()

        # Update status bar
        self.update_status()


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
        self.root.geometry(
            f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Frame for tabs
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(expand=True, fill="both")

        # Was using to not flip the edit_modified flag,
        # but I don't know anymore
        self.ignore_modified = False

        # Initialize Notebook
        self.notebook = ttk.Notebook(self.text_frame)
        self.notebook.pack(fill=tk.BOTH, expand=1)

        # Create a new tab
        self.create_new_tab()

        # Draw the menu/status bar
        self.draw_menu()
        self.draw_status_bar()


    def create_new_tab(self):
        # Create a new frame for the tab
        tab_frame = tk.Frame(self.notebook)
        tab_frame.pack(expand=True, fill="both")

        # Create a new line numbers area
        self.line_numbers = tk.Text(
            tab_frame, width=4, takefocus=0, border=0,
            state="disabled", wrap="none", fg="coral")
        self.line_numbers.pack(side="left", fill="y")
        self.line_numbers.config(font=('Consolas', 10))

        # Create a new text area
        self.text_area = SyntaxHighlightedText(tab_frame, undo=True)
        self.text_area.bind("<<Modified>>", self.text_modified_callback)
        self.text_area.pack(side="left", expand=True, fill="both")

        # Set tabs to 4 spaces
        font = tk.font.Font(font=self.text_area["font"])
        tab = font.measure('    ')
        self.text_area.config(tabs=tab)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(tab_frame, command=self.on_text_scroll)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the text area and line numbers to use the scrollbar
        self.text_area.config(yscrollcommand=self.on_text_scroll)
        self.line_numbers.config(yscrollcommand=self.scrollbar.set)

        # Add the tab to the notebook
        self.notebook.add(tab_frame, text="Untitled")

        # TODO: Return tab_id
        # TODO: Add tab_id to tab dictionary
        # TODO: When switching tabs, update status bar (involves changing a few methods)
        # TODO: When creating a new file, create a new tab
        # TODO: When closing a tab, remove tab_id from dictionary
        
        
    def draw_status_bar(self) -> None:
        # Create status bar frame
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(side="bottom", fill="x")

        # Status Bar Left: File info
        self.file_status_label = tk.Label(
            self.status_frame, textvariable=self.file_status_var, anchor="w")
        self.file_status_label.pack(side="left", fill="x", expand=True)
        
        # Status Bar Right: Position info
        self.position_status_label = tk.Label(
            self.status_frame, textvariable=self.position_status_var, anchor="e")
        self.position_status_label.pack(side="right", padx=(0, 10))


    def draw_menu(self) -> None:
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
        
        # 3. View Menu
        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(
            label="Show Line Numbers",
            onvalue=1,
            offvalue=0,
            variable=self.show_line_numbers,
            command=self.toggle_line_numbers)
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_radiobutton(
            label="Default", variable=self.current_theme,
            value="default", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Monkai", variable=self.current_theme,
            value="monokai", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Solarized Light", variable=self.current_theme,
            value="solarized-light", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Solarized Dark", variable=self.current_theme,
            value="solarized-dark", command=self.change_theme)

        # Keyboard shortcuts bindings
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
        self.text_area.edit_modified(False)
        self.update_status()
        self.create_new_tab()


    def open_file(self) -> None:
        file_path = filedialog.askopenfilename()
        if file_path:
            # self.ignore_modified = True
            self.text_editor.open_file(file_path)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", self.text_editor.text_buffer)
            self.text_area.edit_modified(False)
            # self.ignore_modified = False

            self.update_status()
            self.update_line_numbers()
            self.text_area.highlight()
            self.text_area.focus_set()


    def save_file(self) -> None:
        if self.text_editor.current_file:
            self.text_editor.text_buffer = self.text_area.get("1.0", "end")
            self.text_editor.save_file_as(self.text_editor.current_file)
            self.text_area.edit_modified(False)
            self.update_status()
        else:
            self.save_file_as()


    def save_file_as(self) -> None:
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("All Files", "*.*")])
        if file_path:
            self.text_editor.text_buffer = self.text_area.get("1.0", "end")
            self.text_editor.save_file_as(file_path)
            self.text_area.edit_modified(False)
            self.update_status()


    # Called when window attempts to close in modified state
    # or when user clicks on the exit menu item
    def on_closing(self) -> None:
        print("on_closing called")
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel(
                "Save changes?", "Do you want to save changes before closing?")
            if response:
                self.save_file()
            elif response is None:
                return 
        self.root.destroy()


    def text_modified_callback(self, event=None) -> None:
        print("Text modified callback triggered OUTSIDE")
        if not self.ignore_modified:
            print("Text modified callback triggered")
            self.update_status()
            self.update_line_numbers()
            self.text_area.highlight()
            # Reset modified flag
            self.text_area.edit_modified(False)


    def change_theme(self) -> None:
        self.text_area.change_theme(self.current_theme.get())
        self.update_line_numbers_bg()


    def update_line_numbers_bg(self) -> None:
        bg_color = self.text_area.style.background_color
        self.line_numbers.config(bg=bg_color)


    # Find and Replace
    def find_text(self, event=None):
        FindReplaceDialog(self.root, self.text_area)


    def get_line_col(self):
        cursor_position = self.text_area.index("insert")
        line, col = cursor_position.split(".")
        return int(line), int(col) + 1
    

    def update_status(self, event=None):
        filename = self.text_editor.current_file
        # Update file status
        if filename:
            filename = self.text_editor.current_file
            modified = " (modified)" if self.text_area.edit_modified() else ""
            file_status = f"{filename}{modified}"
        else:
            file_status = "untitled"    
        self.file_status_var.set(file_status)

        # Update position status
        line, col = self.get_line_col()
        line_col_pos = f"Ln {line}, Col {col}"
        self.position_status_var.set(line_col_pos)

        # Update tab title
        tab_title = os.path.basename(filename) if filename else "Untitled"
        self.notebook.tab(
            self.notebook.select(), text=tab_title)
        

    def on_text_scroll(self, *args):
        # Synchronize the scrollbar with text_area and line_numbers
        self.text_area.yview_moveto(args[0])
        self.line_numbers.yview_moveto(args[0])


    # Line Numbers
    def toggle_line_numbers(self):
        if self.show_line_numbers.get():
            self.line_numbers.pack(side="left", fill="y")
            self.update_line_numbers()
        else:
            self.line_numbers.pack_forget()

        # Force a redraw of the text area
        self.text_area.pack_forget()
        self.text_area.pack(expand=True, fill="both")


    def update_line_numbers(self):
        if not self.show_line_numbers.get():
            return
        
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        
        total_lines = self.text_area.index("end-1c").split(".")[0]
        line_numbers_text = "\n".join(
            str(i) for i in range(1, int(total_lines) + 1))
        self.line_numbers.tag_configure("right", justify="right")
        self.line_numbers.insert("1.0", line_numbers_text, "right")
        
        self.line_numbers.config(state="disabled")
        self.line_numbers.yview_moveto(self.text_area.yview()[0])

