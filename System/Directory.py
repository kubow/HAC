"""A directory browser using Ttk Treeview.

Based on the demo found in Tk 8.5 library/demos/browse
"""
import os
import argparse
import glob

import ttk

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

class Window(object):
    """Class for maintain widgets related to directory"""
    
    def populate_tree(tree, node):
        if tree.set(node, "type") != 'directory':
            return

        path = tree.set(node, "fullpath")
        tree.delete(*tree.get_children(node))

        parent = tree.parent(node)
        special_dirs = [] if parent else glob.glob('.') + glob.glob('..')

        for p in special_dirs + os.listdir(path):
            ptype = None
            p = os.path.join(path, p).replace('\\', '/')
            if os.path.isdir(p): ptype = "directory"
            elif os.path.isfile(p): ptype = "file"

            fname = os.path.split(p)[1]
            id = tree.insert(node, "end", text=fname, values=[p, ptype])

            if ptype == 'directory':
                if fname not in ('.', '..'):
                    tree.insert(id, 0, text="dummy")
                    tree.item(id, text=fname)
            elif ptype == 'file':
                size = os.stat(p).st_size
                tree.set(id, "size", "%d bytes" % size)


    def populate_roots(tree):
        dir = os.path.abspath('.').replace('\\', '/')
        node = tree.insert('', 'end', text=dir, values=[dir, "directory"])
        populate_tree(tree, node)

    def update_tree(event):
        tree = event.widget
        populate_tree(tree, tree.focus())

    def change_dir(event):
        tree = event.widget
        node = tree.focus()
        if tree.parent(node):
            path = os.path.abspath(tree.set(node, "fullpath"))
            if os.path.isdir(path):
                os.chdir(path)
                tree.delete(tree.get_children(''))
                populate_roots(tree)

    def autoscroll(sbar, first, last):
        """Hide and show scrollbar as needed."""
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)
    
class app_browser(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        w = Window()

        vsb = ttk.Scrollbar(orient="vertical")
        hsb = ttk.Scrollbar(orient="horizontal")

        tree = ttk.Treeview(columns=("fullpath", "type", "size"),
            displaycolumns="size", yscrollcommand=lambda f, l: w.autoscroll(vsb, f, l),
            xscrollcommand=lambda f, l:w.autoscroll(hsb, f, l))

        vsb['command'] = tree.yview
        hsb['command'] = tree.xview

        tree.heading("#0", text="Directory Structure", anchor='w')
        tree.heading("size", text="File Size", anchor='w')
        tree.column("size", stretch=0, width=100)

        print dir(w)
        w.populate_roots()
        tree.bind('<<TreeviewOpen>>', w.update_tree)
        tree.bind('<Double-Button-1>', w.change_dir)

        # Arrange the tree and its scrollbars in the toplevel
        tree.grid(column=0, row=0, sticky='nswe')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
    
def directory_lister(directory, output, list_files=False):
    head = 'List Generated on {0} / Total Folder Size - {1} / {2} Subfolders </td></tr>'
    table_head = '<table><tr class="Head">{0}<td>{1}</table>'
    table_row = '<tr class="{0}"><td>{1}</td><td>{2}</td></tr>'
    htm=open(directory+'/ListOfFiles.htm', 'w+')
    htm.write(pageTemplateBegin.replace('XXX', directory))
    htmContent = ''
    total_size = 0
    folder_count = 0
    # Walk the directory tree
    for root, directories, files in os.walk(directory):
        print root
        folder_size = 0
        file_count = 0
        tmpContent = ''
        for filename in files:
            folder_size = folder_size+(os.path.getsize(root+'/'+filename)/1024)
            if list_files:
                filesize = str('{0:.2f}'.format(os.path.getsize(root+'/'+filename)/1024))+' kb'
                tmpContent = tmpContent+table_row.format('File', filename, filesize)+'\n'
            file_count += 1
        ref = '<a href="file:///'+root+'">'+root+'</a> ('+str(file_count)+' files in folder)'
        htmContent = htmContent+'\n'+table_row.format('Fldr', ref, str(folder_size)+' kb')+'\n'+tmpContent
        total_size = total_size+folder_size
        folder_count += 1
    htm.write(head.format(datetime.datetime.now(), str(total_size)+' kb', folder_count))
    htm.write(htmContent)
    htm.write(pageTemplateEnd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="construct h808e")
    parser.add_argument('-b', help='browse dir', type=str, default='')
    parser.add_argument('-l', help='list dir', type=str, default='')
    parser.add_argument('-f', help='file output', type=str, default='')
    args = parser.parse_args()
    if args.b:
        root = tk.Tk()
        app = app_browser(root)
        app.mainloop()
    elif args.l:
        directory_lister(args.l, args.f, True)