# Capstone Assessment Project

### Project Overview
This project is an text editor developed in Python as the assessment assignment in CIS 2999.

## Objectives
- Create a functional text editor with core features
- Demonstrate proficiency in Python programming
- Apply object-oriented programming principles
- Implement an intuitive graphical interface

## Features
- Basic text editing (typing, deleting)
- Advanced editing (cut/copy/paste/undo/redo)
- File operations (new, open, save, save as)
- Find/replace functionality
- Line numbering
- Syntax highlighting for Python

## Technology Stack
- Python 3.x
- GUI Framework: [tkinter](https://docs.python.org/3/library/tkinter.html)
- Additional library: [pygments](https://pygments.org) (for syntax highlighting)
- Additional library: [pyperclip](https://pypi.org/project/pyperclip/) (for interacting with the system clipboard)

## User Stories

### As a user:
- I want to create, open, edit, and save text files
- I want to find text within the document
- I want to view line numbers for easier code navigation
- I want basic syntax highlighting for Python code

### As a developer:
- I need to implement basic file I/O with error handling
- I need to create a functional GUI
- I need to implement a basic find/replace function
- I need to implement cut/copy/paste operations
- I need to implement undo/redo functions
- I need to integrate basic syntax highlighting for Python

## Project Structure

### Base Class: TextEditor
#### Fields/Properties:
- current_file: str
- text_content: str
- is_modified: bool
#### Methods:
- new_file()
- open_file()
- save_file()
- save_as()

### GUI Class: EditorGUI
#### Methods:
- create_menu_bar()
- create_text_area()
- create_line_numbers()
- handle_events()
- find_text()
- highlight_syntax()

## Implementation Phases
1. Project setup and basic text editing functionality
2. File operations and GUI development
3. Find functionality, line numbering, text manipulation
4. Basic syntax highlighting
5. Testing, bug fixing, and documentation

## Testing:
#### TextEditor
- Create a new file and verify content is empty
- Open an existing file and verify content is loaded correctly
- Save changes to a file and verify content is updated on disk

#### EditorGUI
- Verify all menu items function correctly
- Test find functionality
- Verify line numbers display correctly
- Test basic syntax highlighting for Python code

## Future Enhancements
- Text formatting options
- Multiple document interface (tabs)
- Syntax highlighting for additional languages

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check [issues page](link_to_issues_page) if you want to contribute.

## License
[MIT](https://choosealicense.com/licenses/mit/) 