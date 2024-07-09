import tkinter as tk
from editor_gui import EditorGUI

def main():
    root = tk.Tk()
    editor = EditorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
