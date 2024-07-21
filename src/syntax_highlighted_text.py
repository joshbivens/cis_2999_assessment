import tkinter as tk
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name

class SyntaxHighlightedText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(font=('Courier', 10))

        self.lexer = get_lexer_by_name("python")
        self.style = get_style_by_name("monokai")
        self.setup_tags()

    def setup_tags(self):
        for token, style in self.style:
            fg = self._format_color(style['color']) if 'color' in style else "#000000"
            bg = self._format_color(style['bgcolor']) if 'bgcolor' in style else "#ffffff"
            font = 'bold' if 'bold' in style and style['bold'] else 'normal'
            self.tag_configure(str(token), foreground=fg, background=bg, font=font)

    def _format_color(self, color):
        if color and not color.startswith('#'):
            color = f'#{color}'
        return color

    def highlight(self, event=None):
        content = self.get("1.0", "end-1c")
        self.mark_set("range_start", "1.0")

        for tag in self.tag_names():
            self.tag_remove(tag, "1.0", "end")

        for token, content in lex(content, self.lexer):
            self.mark_set("range_end", f"range_start + {len(content)}c")
            self.tag_add(str(token), "range_start", "range_end")
            self.mark_set("range_start", "range_end")

        self.edit_modified(False)
