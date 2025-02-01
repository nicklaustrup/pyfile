from tkinter import ttk

def configure_styles():
    style = ttk.Style()
    style.configure("Treeview",
                    highlightthickness=0,
                    bd=0,
                    font=('Calibri', 11))  # Modify font and other properties
    style.configure("Treeview.Heading",
                    font=('Calibri', 13, 'bold'))  # Modify heading font
    style.map("Treeview",
              background=[('selected', 'white')],
              foreground=[('selected', 'black')])
    style.layout("Treeview.Item",
                 [('Treeitem.padding', {'sticky': 'nswe', 'children':
                     [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                      ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                      ('Treeitem.text', {'side': 'left', 'sticky': ''})]})])