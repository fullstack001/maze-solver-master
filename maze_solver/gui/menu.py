from tkinter import *

def make_menu(root, menu_items):
    menu_bar = Menu(root)
    
    for menu_item in menu_items:
        menu = Menu(menu_bar, tearoff=0)
        for command in menu_item['commands']:
            menu.add_command(label=command['label'], command=command['callback'])
        menu_bar.add_cascade(label=menu_item['label'], menu=menu)

    return menu_bar
