"""EditorGUI module for PyEd text editor.

This module provides the EditorGUI class that creates the main text editor
window and handles the GUI elements of the text editor.
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter import font
from text_editor import TextEditor
from find_replace_dialog import FindReplaceDialog
from syntax_highlighted_text import SyntaxHighlightedText
from file_explorer import FileExplorer

class EditorGUI:
    def __init__(self, root) -> None:
        """__init__ method for EditorGUI class.

        Args:
            root (tk.Tk): The root window of the text editor.
        """
        self.root = root
        self.text_editor = TextEditor()

        # Variables
        self.show_line_numbers = tk.IntVar(value=1)
        self.show_file_explorer = tk.IntVar(value=1)
        self.file_status_var = tk.StringVar()
        self.position_status_var = tk.StringVar()
        self.current_theme = tk.StringVar(value="default")
        self.bg_color = "yellow"
        self.ignore_modified = False

        # Track modified status
        self.is_modified = False
        self.ignore_modified = False

        # Check if the text area has been modified when closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize GUI
        self.draw_gui()

        # Update status bar
        self.update_file_status()
        self.update_line_col()


    def draw_gui(self) -> None:
        """Draws the GUI for the text editor."""
        self.root.title("PyEd")

        # Set the window size
        window_width = 1000
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

        # Frame for test area and line numbers
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(expand=True, fill="both")

        # Create line numbers area
        self.line_numbers = tk.Text(
            self.text_frame, width=4, takefocus=0, border=0,
            state="disabled", wrap="none", fg="coral")
        self.line_numbers.pack(side="left", fill="y")
        self.line_numbers.config(font=('Consolas', 10))
        # Prevent scrolling
        self.line_numbers.bind("<MouseWheel>", lambda e: "break")

        # Create text area
        self.text_area = SyntaxHighlightedText(self.text_frame, undo=True)
        self.text_area.bind("<Key>", self.text_modified_callback)
        self.text_area.bind("<KeyRelease>", self.update_line_col)
        self.text_area.bind("<ButtonRelease>", self.update_line_col)
        self.text_area.pack(side="left", expand=True, fill="both")

        # Set tabs to 4 spaces
        current_font = tk.font.Font(font=self.text_area["font"])
        tab = current_font.measure('    ')
        self.text_area.config(tabs=tab)

        # Create a scrollbar
        # TODO: FIX ME error calling moveto on on_text_scroll <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.on_text_scroll)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the text area and line numbers to use the scrollbar
        self.text_area.config(yscrollcommand=self.on_text_scroll)
        self.line_numbers.config(yscrollcommand=self.scrollbar.set)

        # File explorer frame
        self.file_explorer_frame = tk.Frame(self.text_frame)
        self.file_explorer_frame.pack(side="right", fill="y")

        # File explorer
        self.file_explorer = FileExplorer(
            self.file_explorer_frame, show="tree", open_file_callback=self.open_file)
        self.file_explorer.pack(side="left", fill="both", expand=True)
        ttk.Style().theme_use("clam")

        # Draw the menu/status bar
        self.draw_menu()
        self.draw_status_bar()
        self.update_bg_color()

        
    def draw_status_bar(self) -> None:
        """Draws the status bar for the text editor."""
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
        """Draws the menu bar for the text editor."""
        # Menu Bar
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # 1. File Menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="Open File", 
            command=self.open_file, 
            accelerator="Ctrl+O")
        file_menu.add_command(
            label="Open Folder", 
            command=self.open_folder,
            accelerator="Ctrl+Shift+O")
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
        
        # File menu key bindings
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-O>", lambda e: self.open_folder())
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-S>", lambda e: self.save_file_as())
        self.root.bind("<Control-q>", lambda e: self.on_closing())

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
        
        # Edit menu key bindings
        self.root.bind("<Control-z>", lambda e: self.text_area.event_generate("<<Undo>>"))
        self.root.bind("<Control-y>", lambda e: self.text_area.event_generate("<<Redo>>"))
        self.root.bind("<Control-x>", lambda e: self.text_area.event_generate("<<Cut>>"))
        self.root.bind("<Control-c>", lambda e: self.text_area.event_generate("<<Copy>>"))
        self.root.bind("<Control-v>", lambda e: self.text_area.event_generate("<<Paste>>"))
        self.root.bind("<Control-a>", lambda e: self.text_area.event_generate("<<SelectAll>>"))
        self.root.bind("<Control-f>", lambda e: self.find_text())
        
        # 3. View Menu
        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(
            label="Show Line Numbers",
            onvalue=1,
            offvalue=0,
            variable=self.show_line_numbers,
            command=self.toggle_line_numbers)
        
        view_menu.add_checkbutton(
            label="Show File Explorer",
            onvalue=1,
            offvalue=0,
            variable=self.show_file_explorer,
            command=self.toggle_file_explorer)
        
        # Toggles key binding
        # TODO: These don't work FIX ME <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.root.bind("<Control-l>", lambda e: self.toggle_line_numbers())
        self.root.bind("<Control-e>", lambda e: self.toggle_file_explorer())
        
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Theme", menu=theme_menu)

        # Light Themes
        theme_menu.add_command(label="Light", state="disabled")
        theme_menu.add_separator()

        theme_menu.add_radiobutton(
            label="Default", variable=self.current_theme,
            value="default", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Solarized Light", variable=self.current_theme,
            value="solarized-light", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Paraiso Light", variable=self.current_theme,
            value="paraiso-light", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Igor", variable=self.current_theme,
            value="igor", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Manni", variable=self.current_theme,
            value="manni", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Perldoc", variable=self.current_theme,
            value="perldoc", command=self.change_theme)

        # Dark Themes
        theme_menu.add_command(label="")
        theme_menu.add_command(label="Dark", state="disabled")
        theme_menu.add_separator()

        theme_menu.add_radiobutton(
            label="Monkai", variable=self.current_theme,
            value="monokai", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Solarized Dark", variable=self.current_theme,
            value="solarized-dark", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Paraiso Dark", variable=self.current_theme,
            value="paraiso-dark", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Material Dark", variable=self.current_theme,
            value="material", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Coffee", variable=self.current_theme,
            value="coffee", command=self.change_theme)
        theme_menu.add_radiobutton(
            label="Nord Darker", variable=self.current_theme,
            value="nord-darker", command=self.change_theme) 


    # Menu functions
    def new_file(self) -> None:
        """Creates a new file in the text editor."""
        self.text_editor.text_buffer = ""
        self.text_area.delete("1.0", "end")
        self.is_modified = False
        self.update_file_status()
        self.create_new_tab()


    def open_file(self, path=None) -> None:
        """Opens a file in the text editor."""
        # Prompts to save if modified
        self.on_open_file()
        file_path = filedialog.askopenfilename() if path is None else path
        if file_path:
            self.ignore_modified = True
            self.text_editor.open_file(file_path)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", self.text_editor.text_buffer)
            self.is_modified = False
            self.ignore_modified = False

            # Update Treeview to file's directory
            self.open_folder(file_path)

            self.update_file_status()
            self.update_line_numbers()
            self.text_area.highlight()
            self.text_area.focus_set()


    def open_folder(self, path=None) -> None:
        """Opens a folder in the file explorer."""
        if path and os.path.isfile(path):
            folder_path = os.path.dirname(path)
        else:
            folder_path = filedialog.askdirectory() if path is None else path

        if folder_path:
            self.file_explorer.populate_tree(folder_path)


    def on_open_file(self) -> None:
        """Called when a file is opened and the text area has been updated."""
        if self.is_modified:
            response = messagebox.askyesnocancel(
                "Save changes?", "Do you want to save changes before opening a new file?")
            if response:
                self.save_file()
            elif response is None:
                return
            
    
    def on_closing(self) -> None:
        """Called when the window is closing."""
        self.on_open_file()
        self.root.destroy()


    def save_file(self) -> None:
        """Saves the current file in the text editor."""
        if self.text_editor.current_file:
            self.text_editor.text_buffer = self.text_area.get("1.0", "end")
            self.text_editor.save_file_as(self.text_editor.current_file)
            self.is_modified = False
            self.update_file_status()
        else:
            self.save_file_as()


    def save_file_as(self) -> None:
        """Saves the current file as a new file in the text editor."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py", filetypes=[("All Files", "*.*")])
        if file_path:
            self.text_editor.text_buffer = self.text_area.get("1.0", "end")
            self.text_editor.save_file_as(file_path)
            self.is_modified = False
            self.update_file_status()


    def text_modified_callback(self, event=None) -> None:
        """Called when the text area is modified.
        
        Args:
            event (tk.Event): The event that triggered the callback.
        """
        if not self.ignore_modified:
            self.is_modified = True
            self.update_line_col()
            self.update_file_status()
            self.update_line_numbers()
            self.text_area.highlight()


    def change_theme(self) -> None:
        """Changes the theme of the text editor."""
        self.text_area.change_theme(self.current_theme.get())
        self.update_bg_color()


    def update_bg_color(self) -> None:
        """Updates the background colors of line numbers and file explorer."""
        # Get bg color from text area
        bg_color = self.text_area.style.background_color

        # Set line numbers bg color
        self.line_numbers.config(bg=bg_color)

        # Lighten/Darken the bg color for the selected text
        selected_bg_color = self.lighten_darken_color(bg_color)
        self.text_area.config(selectbackground=selected_bg_color)

        # Set the bg color for the file explorer
        ttk.Style().configure("Treeview", background=bg_color, 
                fieldbackground=bg_color, foreground="coral")
        

    def lighten_darken_color(self, color) -> str:
        """Lighten a color by a given amount.

        To be used to lighten/darken the background color of 
        the selected text.

        Args:
            color (str): The color to lighten/darken.
        """
        # Remove hash
        color = color.lstrip("#")

        # Convert to RGB
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)

        # Determine brightness
        brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255

        # Amount to lighten/darken
        amount = 0.2

        # Determine factor based on brightness
        factor = 1 - amount if brightness > 0.5 else 1.5 + amount

        # Apply the factor. Ensures values are between 0 and 255
        r = max(0, min(int(r * factor), 255))
        g = max(0, min(int(g * factor), 255))
        b = max(0, min(int(b * factor), 255))
        
        # Recombine and convert to hex
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)


    # Find and Replace
    def find_text(self, event=None):
        """Calls FindReplaceDialog module.
        
        Args:
            event (tk.Event): The event that triggered the callback
        """
        FindReplaceDialog(self.root, self.text_area)


    def get_line_col(self):
        """Returns the current line and column of the cursor."""
        cursor_position = self.text_area.index("insert")
        line, col = cursor_position.split(".")
        return int(line), int(col) + 1
    
    
    def update_line_col(self, event=None):
        """Updates the line and column of the cursor."""
        line, col = self.get_line_col()
        self.position_status_var.set(f"Ln {line}, Col {col}")


    def update_file_status(self, event=None):
        """Updates the file status in the status bar.
        
        Args:
            event (tk.Event): The event that triggered the callback
        """
        # Update file status
        file_name = os.path.abspath(
            self.text_editor.current_file) if self.text_editor.current_file else "New File"
        file_status = f"{file_name}{' (modified)' if self.is_modified else ''}"
        self.file_status_var.set(file_status)
        

    def on_text_scroll(self, *args):
        """Synchronize the scrollbar with text_area and line_numbers.
        
        Args:
            *args: The arguments passed to the callback
        """
        self.line_numbers.yview_moveto(args[0])


    # Line Numbers
    def toggle_line_numbers(self):
        """Toggles the line numbers."""
        if self.show_line_numbers.get():
            self.line_numbers.pack(side="left", fill="y")
            self.update_line_numbers()
        else:
            self.line_numbers.pack_forget()

        # Force a redraw of the text area
        self.text_area.pack_forget()
        self.text_area.pack(expand=True, fill="both")


    def toggle_file_explorer(self, *args):
        """Toggles the file explorer."""
        if self.show_file_explorer.get():
            self.file_explorer_frame.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self.file_explorer_frame.pack_forget()


    def update_line_numbers(self):
        """Updates the line numbers."""
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
