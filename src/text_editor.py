"""This module contains the TextEditor class.

This class interfaces with the file system to open and save files.
"""

class TextEditor:
    def __init__(self) -> None:
        """__init__ method for TextEditor class."""
        self.current_file = None
        self.text_buffer = ""

    
    def open_file(self, file_path: str) -> None:
        """Open a file and read its contents into the text buffer."""
        with open(file_path, "r", encoding="utf8") as file:
            self.current_file = file_path
            self.text_buffer = file.read()

    
    def save_file_as(self, file_path: str) -> None:
        """Save the text buffer to a file."""
        with open(file_path, "w", encoding="utf8") as file:
            self.current_file = file_path
            file.write(self.text_buffer)
