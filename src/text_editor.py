class TextEditor:
    def __init__(self) -> None:
        self.current_file = None
        self.text_buffer = ""

    def open_file(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf8") as file:
            self.current_file = file_path
            self.text_buffer = file.read()

    def save_file_as(self, file_path: str) -> None:
        with open(file_path, "w", encoding="utf8") as file:
            self.current_file = file_path
            file.write(self.text_buffer)

    # TODO: Now we need to save the text_buffer to the file