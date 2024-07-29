import pandasql as psql
import pandas as pd
import json
import os
import urwid

# Dados de exemplo
data = {
    'id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 40],
    'salary': [50000, 60000, 70000, 80000]
}
df = pd.DataFrame(data)

query_result = None
queries_file = 'data/queries.json'
search_type = 'name'  # Tipo de busca padrão

def execute_query(button, query_edit, result_text):
    global query_result
    query = query_edit.get_edit_text()
    print(f"Executing query: {query}")
    try:
        result = psql.sqldf(query, {'df': df})
        query_result = result
        result_text.set_text(result.to_string())
        print(f"Query executed successfully.")
    except Exception as e:
        error_message = f"Error: {str(e)}"
        result_text.set_text(error_message)
        query_result = None
        print(error_message)

def save_query(button, query_edit, name_edit, subject_edit):
    query = query_edit.get_edit_text()
    name = name_edit.get_edit_text().strip()
    subject = subject_edit.get_edit_text().strip()
    
    if not name:
        print("Query name is required.")
        return
    
    print(f"Saving query: {query} with name: {name} and subject: {subject}")
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(queries_file):
            with open(queries_file, 'w') as f:
                json.dump([], f)
        with open(queries_file, 'r+') as f:
            queries = json.load(f)
            queries.append({"name": name, "query": query, "subject": subject})
            f.seek(0)
            json.dump(queries, f, indent=4)
        print("Query saved successfully.")
    except Exception as e:
        print(f"Error saving query: {str(e)}")

def filter_queries(queries, search_text, search_type):
    if search_type == 'name':
        return [q for q in queries if search_text.lower() in q['name'].lower()]
    elif search_type == 'query':
        return [q for q in queries if search_text.lower() in q['query'].lower()]
    elif search_type == 'subject':
        return [q for q in queries if search_text.lower() in q.get('subject', '').lower()]
    return queries

def paginate(items, page_size, page_number):
    start = page_size * page_number
    end = start + page_size
    return items[start:end]

def search_menu(query_edit, palette):
    menu_text = urwid.Text(u"Search Menu", align='center')
    search_name_button = urwid.Button(u"🔍 Search by Name")
    search_query_button = urwid.Button(u"🔍 Search by Query")
    search_subject_button = urwid.Button(u"🔍 Search by Subject")
    back_button = urwid.Button(u"🔙 Back")

    urwid.connect_signal(search_name_button, 'click', lambda button: load_query(button, query_edit, palette, search_type='name'))
    urwid.connect_signal(search_query_button, 'click', lambda button: load_query(button, query_edit, palette, search_type='query'))
    urwid.connect_signal(search_subject_button, 'click', lambda button: load_query(button, query_edit, palette, search_type='subject'))
    urwid.connect_signal(back_button, 'click', lambda button: return_to_main(query_edit, None, palette))

    menu = urwid.Pile([menu_text, urwid.Divider(), search_name_button, search_query_button, search_subject_button, back_button])
    fill = urwid.Filler(menu, valign='top')

    urwid.MainLoop(fill, palette).run()

def load_query(button, query_edit, palette, search_text='', search_type='name', page_number=0, page_size=5):
    print(f"Loading query with search text: {search_text} and search type: {search_type}")
    try:
        if not os.path.exists(queries_file):
            query_edit.set_edit_text("No saved queries found.")
            return
        with open(queries_file, 'r') as f:
            queries = json.load(f)
        
        filtered_queries = filter_queries(queries, search_text, search_type)
        paginated_queries = paginate(filtered_queries, page_size, page_number)
        
        query_choices = [urwid.Button(f"Name: {q['name']}\nQuery: {truncate_text(q['query'])}\nSubject: {q.get('subject', 'N/A')}") for q in paginated_queries]
        query_list = urwid.ListBox(urwid.SimpleFocusListWalker(query_choices))
        for query_button in query_choices:
            urwid.connect_signal(query_button, 'click', lambda button, query=query_button.get_label().split('\n')[1].split(': ')[1]: return_to_main(query, query_edit, palette))
        
        search_edit = urwid.Edit(('edit', f"Search by {search_type}: \n"), multiline=False)
        search_button = urwid.Button(u"Search")
        urwid.connect_signal(search_button, 'click', lambda button: search_queries(search_edit, query_edit, palette, search_type))
        
        next_page_button = urwid.Button(u"Next Page")
        prev_page_button = urwid.Button(u"Previous Page")
        urwid.connect_signal(next_page_button, 'click', lambda button: load_query(button, query_edit, palette, search_text, search_type, page_number + 1, page_size))
        urwid.connect_signal(prev_page_button, 'click', lambda button: load_query(button, query_edit, palette, search_text, search_type, max(0, page_number - 1), page_size))

        exit_button = urwid.Button(u"Back")
        urwid.connect_signal(exit_button, 'click', lambda button: search_menu(query_edit, palette))
        
        list_pile = urwid.Pile([
            urwid.Text(u"Select a query to load:"),
            urwid.Divider(),
            urwid.BoxAdapter(query_list, height=10),
            urwid.Divider(),
            search_edit,
            search_button,
            urwid.Divider(),
            urwid.Columns([prev_page_button, next_page_button]),
            urwid.Divider(),
            exit_button
        ])
        
        urwid.MainLoop(urwid.Filler(list_pile), palette).run()
    except FileNotFoundError:
        query_edit.set_edit_text("No saved queries found.")
    except Exception as e:
        print(f"Error loading query: {str(e)}")

def truncate_text(text, max_length=50):
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text

def search_queries(search_edit, query_edit, palette, search_type):
    search_text = search_edit.get_edit_text()
    load_query(None, query_edit, palette, search_text, search_type)

def return_to_main(query, query_edit, palette):
    if query_edit is not None:
        query_edit.set_edit_text(query)
    raise urwid.ExitMainLoop()

def exit_main_loop(button):
    raise urwid.ExitMainLoop()

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

# Função principal
def main():
    palette = [
        ('banner', 'white', 'black'),
        ('streak', 'black', 'light gray'),
        ('inside', 'black', 'dark blue'),
        ('bg', 'black', 'light gray'),
        ('button', 'black', 'light gray', 'standout'),
        ('button focus', 'light cyan', 'black'),
        ('text', 'light gray', 'black'),
        ('edit', 'light gray', 'dark gray'),
        ('edit focus', 'light cyan', 'dark gray', 'bold'),
    ]

    menu_text = urwid.Text(('banner', u"SQL Query Executor"), align='center')
    query_edit = urwid.Edit(('edit', u"Enter your SQL Query (e.g., SELECT * FROM df):\n"), multiline=True)
    name_edit = urwid.Edit(('edit', u"Enter query name:\n"), multiline=False)
    subject_edit = urwid.Edit(('edit', u"Enter query subject (optional):\n"), multiline=False)
    result_text = urwid.Text(('text', u"Query Results will be displayed here."), wrap='clip')

    execute_button = urwid.Button(u"Execute")
    save_button = urwid.Button(u"Save Query")
    load_button = urwid.Button(u"🔍 Search and Load Query")
    plot_button = urwid.Button(u"Plot Graph")

    urwid.connect_signal(execute_button, 'click', execute_query, user_args=(query_edit, result_text))
    urwid.connect_signal(save_button, 'click', save_query, user_args=(query_edit, name_edit, subject_edit))
    urwid.connect_signal(load_button, 'click', lambda button: search_menu(query_edit, palette))
    urwid.connect_signal(plot_button, 'click', plot_graph, user_args=(result_text, query_edit, palette))

    buttons = urwid.Columns([execute_button, save_button, load_button, plot_button], dividechars=2)
    pile = urwid.Pile([menu_text, query_edit, name_edit, subject_edit, buttons, urwid.Divider(), result_text])

    fill = urwid.Filler(pile, valign='top')
    urwid.MainLoop(fill, palette, unhandled_input=exit_on_q).run()

if __name__ == "__main__":
    main()
