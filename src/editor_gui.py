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

        # Window/Components
        self.text_area = tk.Text(self.root)
        self.text_area.pack(expand=True, fill="both")