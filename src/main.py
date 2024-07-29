import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.widgets import ImageWidget, create_button_column, exit_on_q, palette
from src.queries import execute_query, save_query, search_menu
from src.plot import plot_graph

import urwid

def start_home():
    global query_edit
    query_edit = urwid.Edit(('edit', u"Enter your SQL Query (e.g., SELECT * FROM df):\n"), multiline=True)
    result_text = urwid.Text(('text', u"Query Results will be displayed here."))
    name_edit = urwid.Edit(('edit', u"Enter query name (required):\n"), multiline=False)
    subject_edit = urwid.Edit(('edit', u"Enter query subject (optional):\n"), multiline=False)
    image_widget = ImageWidget('data/query_result_plot.png')

    execute_button = urwid.Button(u"💼 Execute")
    save_button = urwid.Button(u"💾 Save Query")
    load_button = urwid.Button(u"📂 Load Query")
    plot_button = urwid.Button(u"📊 Plot Graph")

    urwid.connect_signal(execute_button, 'click', lambda button: execute_query(button, query_edit, result_text))
    urwid.connect_signal(save_button, 'click', lambda button: save_query(button, query_edit, name_edit, subject_edit))
    urwid.connect_signal(load_button, 'click', lambda button: search_menu(query_edit, palette))
    urwid.connect_signal(plot_button, 'click', lambda button: plot_graph(button, result_text, image_widget))

    buttons = create_button_column(execute_button, save_button, load_button, plot_button)

    pile = urwid.Pile([
        urwid.AttrMap(urwid.Text(('banner', u"SQL Query Executor"), align='center'), 'bg'),
        urwid.Divider('-'),
        urwid.AttrMap(query_edit, 'edit'),
        urwid.AttrMap(name_edit, 'edit'),
        urwid.AttrMap(subject_edit, 'edit'),
        urwid.Divider(),
        buttons,
        urwid.Divider('-'),
        urwid.AttrMap(result_text, 'text'),
        urwid.Divider(),
        urwid.AttrMap(image_widget, 'bg'),
    ])
    fill = urwid.Filler(pile, valign='top')

    loop = urwid.MainLoop(fill, palette, unhandled_input=exit_on_q)
    loop.run()

if __name__ == "__main__":
    start_home()
