import tkinter as tk
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name

class SyntaxHighlightedText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(font=('Courier', 12))

        self.lexer = get_lexer_by_name("python")
        self.style = get_style_by_name("default")
        self.setup_tags()

    def setup_tags(self):
        for token, opts in self.styles.items():
            foreground = opts['color'] if 'color' in opts else None
            background = opts['bgcolor'] if 'bgcolor' in opts else None
            font = 'bold' if 'bold' in opts else 'normal'
            
            self.tag_configure(str(token), foreground=foreground, 
                               background=background, font=font)

    def highlight(self, event=None):
        # Get text content from the text widget
        content = self.text_area.get("1.0", "end-1c")

        # Set tag at beginning of text widget
        self.text_area.mark_set("range_start", "1.0")

        # For each token, apply start and end tags
        for token, content in lex(content, self.lexer):
            self.text_area.mark_set("range_end", f"range_start + {len(content)}c")
            self.text_area.tag_add(str(token), "range_start", "range_end")
            self.text_area.mark_set("range_start", "range_end")
