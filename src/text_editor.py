class TextEditor:
    def __init__(self) -> None:
        self.current_file = None
        self.text_buffer = ""

    def open_file(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            self.current_file = file_path
            self.text_buffer = file.read()
