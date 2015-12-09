"""

A code editor, can also compile and run programs.
Currently supports only C++ in Windows

"""
#!usr/bin/Python2

import Tkinter as GUI
from ScrolledText import *
from functools import partial
import commands as EC


app = GUI.Tk()
app2 = GUI.Tk()
app2.withdraw()


def main():
    def hello():
        c = map(int, pad.index(GUI.INSERT).split('.'))
        c[-1] -= 1
        pad.delete(str(c[0]) + '.' + str(c[-1]), GUI.END)

    def shareBar(*args):
        pad.yview(*args)
        linepad.yview(*args)

    def shareMouseWheel(event):
        pad.yview('scroll', event.delta, 'units')
        linepad.yview('scroll', -1 * (event.delta / 120), 'units')
        return 'break'

    MyDict = EC.Trie()
    File = EC.FileDetails()
    EC.setKeys()
    Display = EC.display_func()
    cmd_file = EC.cmd_filemenu()
    edit = EC.editFileMenu()
    run = EC.runFilemenu()

    frame1 = GUI.Frame(app)
    frame12 = GUI.Frame(app)
    frame2 = GUI.Frame(app)
    W1 = GUI.PanedWindow(frame1, height=30, width=70)
    bar_editor = GUI.Scrollbar(frame1)
    bar_input_h = GUI.Scrollbar(frame12, orient=GUI.HORIZONTAL)

    # 272822
    pad = GUI.Text(
        W1,
        height=30,
        width=60,
        yscrollcommand=bar_editor.set,
        undo=True)
    pad.config(fg='#f8f8f2', bg='#002b36', insertbackground='white')

    linepad = GUI.Text(
        frame1,
        height=30,
        width=4,
        yscrollcommand=bar_editor.set,
        undo=True)
    linepad.config(
        fg='#f8f8f2',
        bg='#002b36',
        insertbackground='white',
        state=GUI.DISABLED)

    inputpad = GUI.Text(
        W1,
        height=30,
        width=30,
        xscrollcommand=bar_input_h.set)
    inputpad.config(fg='white', bg='#002b36', insertbackground='white')
    W1.add(pad)
    W1.add(inputpad)

    bar_editor.config(command=shareBar)
    bar_input_h.config(command=inputpad.xview)
    # 2aa198
    outputpad = ScrolledText(frame2, height=5, width=80)
    outputpad.config(
        fg='white',
        bg='#002b36',
        insertbackground='white',
        state=GUI.DISABLED)

    menubar = GUI.Menu(app)
    filemenu = GUI.Menu(menubar, tearoff=0)
    filemenu.add_command(label='New', command=hello)
    filemenu.add_command(
        label='Open',
        command=lambda: cmd_file.Open(
            app,
            pad,
            linepad))
    filemenu.add_command(label='Save', command=lambda: cmd_file.Save(app, pad))
    filemenu.add_command(
        label='Save As',
        command=lambda: cmd_file.Save_As(
            app,
            pad))
    filemenu.add_command(label='Exit', command=cmd_file.Exit)
    menubar.add_cascade(label='File', menu=filemenu)

    editmenu = GUI.Menu(menubar, tearoff=0)
    editmenu.add_command(label='Undo - (ctrl+z)', command=edit.undo)
    editmenu.add_command(label='Redo - (ctrl+r)', command=edit.redo)
    menubar.add_cascade(label='Edit', menu=editmenu)

    runmenu = GUI.Menu(menubar, tearoff=0)
    runmenu.add_command(
        label='Compile - (F7)',
        command=lambda: run.compile(
            app,
            pad,
            outputpad))
    runmenu.add_command(
        label='Run - (F5)',
        command=lambda: run.run(
            app,
            pad,
            outputpad,
            inputpad))
    menubar.add_cascade(label='Run', menu=runmenu)

    app.bind(
        '<KeyPress>',
        lambda event: Display.show_in_console(
            event,
            app2,
            pad,
            linepad))
    app.bind('<space>', lambda event: Display.addToTrie(pad, event))
    app.bind(
        '<Return>',
        lambda event: Display.indentation(
            pad,
            linepad,
            event))
    app.bind('<F7>', lambda event: run.compile(app, pad, outputpad, event))
    app.bind(
        '<F5>',
        lambda event: run.run(
            app,
            pad,
            outputpad,
            inputpad,
            event))
    app.bind('<Control-r>', lambda event: edit.redo(pad, linepad, event))
    app.bind('<Control-z>', lambda event: edit.undo(pad, linepad, event))

    frame1.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
    linepad.pack(side=GUI.LEFT, fill=GUI.Y)
    W1.pack(side=GUI.LEFT, fill=GUI.BOTH, expand=GUI.YES)
    # pad.pack(side = LEFT,fill=BOTH, expand=YES)
    bar_editor.pack(side=GUI.LEFT, fill=GUI.Y)
    # inputpad.pack(side = LEFT,fill=Y)
    frame12.pack(side=GUI.TOP, fill=GUI.BOTH)
    frame2.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
    bar_input_h.pack(side=GUI.RIGHT)
    outputpad.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
    app.config(menu=menubar)

if __name__ == '__main__':
    main()
    app.title('untitled.cpp')
    app.mainloop()
    app2.mainloop()
