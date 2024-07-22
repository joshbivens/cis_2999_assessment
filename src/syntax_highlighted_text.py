"""
SyntaxHighlightedText module for syntax highlighting in tkinter 
Text widgets in the PyEd text editor application.

This module provides a SyntaxHighlightedText class that subclasses
tk.Text to provide syntax highlighting for Python files in PyEd text widgets.
The class uses the pygments library to perform syntax highlighting and supports 
changing the theme of the syntax highlighting.
"""

import tkinter as tk
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name

class SyntaxHighlightedText(tk.Text):
    def __init__(self, master=None, theme="default", **kwargs):
        """__init__ method for SyntaxHighlightedText class.
        
        Args:
            master (tk.Tk): The root window of the application.
            theme (str): The name of the theme to use for syntax highlighting.
            **kwargs: Additional keyword arguments to pass to the tk.Text class.
        """
        super().__init__(master, **kwargs)
        self.configure(font=('Consolas', 10))
        self.theme = theme
        self.highlighting = False
        self.lexer = get_lexer_by_name("python")
        self.style = get_style_by_name(self.theme)
        self.setup_tags()

    
    def change_theme(self, theme):
        """Change the theme of the SyntaxHighlightedText widget.
        
        Args:
            theme (str): The name of the theme to change to.
        """
        self.theme = theme
        self.style = get_style_by_name(self.theme)
        self.setup_tags()
        self.highlight()

    
    def setup_tags(self):
        """Setup tags for the SyntaxHighlightedText widget."""
        base_font = self.cget("font") # Overrides default theme font
        for token, style in self.style:
            # Unhandled tokens get default colors
            fg = self.format_color(
                style['color']) if 'color' in style else "#000000"
            bg = self.format_color(
                style['bgcolor']) if 'bgcolor' in style else "#ffffff"
            font = base_font + " bold" if style.get('bold') else base_font
            self.tag_configure(
                str(token), foreground=fg, background=bg, font=font)

        # Light/Dark theme background color    
        bg_color = self.style.background_color
        self.config(bg=bg_color)

    
    # Fixes an error where tkinter doesn't recognize color
    # names without a hash
    def format_color(self, color):
        """Format a color string to include a hash if it doesn't have one.
        
        Args:
            color (str): The color string to format.
        """
        if color and not color.startswith('#'): 
            color = f'#{color}'
        return color

    
    def highlight(self, event=None):
        """Highlight the text in the SyntaxHighlightedText widget.
        
        Args:
            event (tk.Event): The event that triggered the highlight
        """
        if self.highlighting:
            return
        self.highlighting = True

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
