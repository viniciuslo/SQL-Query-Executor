import urwid
from PIL import Image
import os

class ImageWidget(urwid.Widget):
    def __init__(self, filepath):
        self.filepath = filepath
        self.image_data = []

    def set_image(self, filepath):
        self.filepath = filepath
        self._invalidate()

    def rows(self, size, focus=False):
        if self.image_data:
            return len(self.image_data)
        return 0

    def render(self, size, focus=False):
        maxcol = size[0]
        if os.path.exists(self.filepath):
            img = Image.open(self.filepath)
            img = img.convert("L")
            aspect_ratio = img.height / img.width
            new_width = maxcol
            new_height = int(aspect_ratio * new_width * 0.55)
            img = img.resize((new_width, new_height))
            pixels = img.getdata()
            chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
            self.image_data = [
                "".join(chars[pixel // 25] for pixel in pixels[i * new_width:(i + 1) * new_width])
                for i in range(new_height)
            ]
            return urwid.TextCanvas(self.image_data, maxcol=maxcol)
        return urwid.TextCanvas([""], maxcol=maxcol)

def create_button_column(execute_button, save_button, load_button, plot_button):
    buttons = urwid.Columns([
        urwid.AttrMap(execute_button, None, focus_map='button focus'),
        urwid.AttrMap(save_button, None, focus_map='button focus'),
        urwid.AttrMap(load_button, None, focus_map='button focus'),
        urwid.AttrMap(plot_button, None, focus_map='button focus')
    ], dividechars=2)
    return buttons

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'light gray'),
    ('bg', 'black', 'light gray'),
    ('button', 'black', 'dark cyan'),
    ('button focus', 'white', 'dark blue'),
    ('edit', 'white', 'dark gray'),
    ('text', 'light gray', 'black'),
]
