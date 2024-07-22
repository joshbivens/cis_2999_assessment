import tkinter as tk
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name

class SyntaxHighlightedText(tk.Text):
    def __init__(self, master=None, theme="default", **kwargs):
        super().__init__(master, **kwargs)
        self.configure(font=('Consolas', 10))
        self.theme = theme

        self.lexer = get_lexer_by_name("python")
        self.style = get_style_by_name(self.theme)

        self.highlighting = False

        self.setup_tags()
    
    def change_theme(self, theme):
        self.theme = theme
        self.style = get_style_by_name(self.theme)
        self.setup_tags()
        self.highlight()

    def setup_tags(self):
        base_font = self.cget("font") # Overrides default theme font
        for token, style in self.style:
            # Unhandled tokens get default colors
            fg = self._format_color(
                style['color']) if 'color' in style else "#000000"
            bg = self._format_color(
                style['bgcolor']) if 'bgcolor' in style else "#ffffff"
            font = base_font + " bold" if style.get('bold') else base_font
            self.tag_configure(
                str(token), foreground=fg, background=bg, font=font)

        # Light/Dark theme background color    
        bg_color = self.style.background_color
        self.config(bg=bg_color)

    # Fixes an error where tkinter doesn't recognize color
    # names without a hash
    def _format_color(self, color):
        if color and not color.startswith('#'): 
            color = f'#{color}'
        return color

    def highlight(self, event=None):
        if self.highlighting:
            return
        self.highlighting = True

        print("highlight called")

        content = self.get("1.0", "end-1c")
        self.mark_set("range_start", "1.0")

        for tag in self.tag_names():
            self.tag_remove(tag, "1.0", "end")

        for token, content in lex(content, self.lexer):
            self.mark_set("range_end", f"range_start + {len(content)}c")
            self.tag_add(str(token), "range_start", "range_end")
            self.mark_set("range_start", "range_end")

        self.edit_modified(False)
        self.highlighting = False
