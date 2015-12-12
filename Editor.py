#!usr/bin/Python2
"""

A code editor, can also compile and run programs.
Currently supports only C++ in Windows

Now python2 support yay

"""

import Tkinter as GUI
import ScrolledText
import commands as EC
import os

app = GUI.Tk()
app2 = GUI.Tk()
app2.withdraw()
lang = ''

"""
Variables used here :
:param app: the main window
:param app2: the window for autocomplete
:param pad: the textbox in which code is written
:param lb: the listbox storing autocomplete words
:param lang: programming language
:param linepad: textbox contain lines
:param inputpad: textbox for storing input
:param outputpad: textbox for storing output
:param args: mostly to pass event bindings

:return:
"""


def main():
    MyDict = EC.Trie()
    File = EC.FileDetails()
    EC.setKeys()
    Display = EC.codeDisplay()
    cmd_file = EC.fileFileMenu()
    edit = EC.editFileMenu()
    run = EC.runFilemenu()

    def change_lang(newlang):
        """
        changes current language in editor
        :param newlang: language to switch to
        :return:
        """
        global lang
        lang = newlang
        r = map(str, app.title().split('.'))
        if lang == 'c++' and r[-1] == 'py':
            app.title('untitled.cpp')
            cmd_file.set_new_filedetails('untitled.cpp', os.getcwd() + '/untitled.cpp')
            print File.name, File.path
        if lang == 'py' and r[-1] == 'cpp':
            app.title('untitled.py')
            cmd_file.set_new_filedetails('untitled.py', os.getcwd() + '/untitled.py')

    change_lang('c++')

    def hello():
        c = map(int, pad.index(GUI.INSERT).split('.'))
        c[-1] -= 1
        pad.delete(str(c[0]) + '.' + str(c[-1]), GUI.END)

    def shareBar(*args):
        """
        the linenumber abd code textpads share same scrollbar
        :param args: event
        :return:
        """
        pad.yview(*args)
        linepad.yview(*args)

    def shareMouseWheel(event):
        """
        the linenumber abd code textpads share mousewheel
        :param event:
        :return:
        """
        pad.yview('scroll', event.delta, 'units')
        linepad.yview('scroll', -1 * (event.delta / 120), 'units')
        return 'break'

    frame1 = GUI.Frame(app)
    frame12 = GUI.Frame(app)
    frame2 = GUI.Frame(app)
    W1 = GUI.PanedWindow(frame1, height=30, width=70)
    bar_editor = GUI.Scrollbar(frame1)
    bar_input_h = GUI.Scrollbar(frame12, orient=GUI.HORIZONTAL)

    # 272822
    lb = GUI.Listbox(app2, height=10, width=30)
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
    outputpad = ScrolledText.ScrolledText(frame2, height=5, width=80)
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
            linepad,
            lang))
    filemenu.add_command(label='Save', command=lambda: cmd_file.Save(app, pad))
    filemenu.add_command(
        label='Save As',
        command=lambda: cmd_file.Save_As(
            app,
            pad))
    filemenu.add_command(label='Exit', command=cmd_file.Exit)
    menubar.add_cascade(label='File', menu=filemenu)

    editmenu = GUI.Menu(menubar, tearoff=0)
    editmenu.add_command(label='Undo - (ctrl+z)', command=lambda: edit.undo(pad, linepad))
    editmenu.add_command(label='Redo - (ctrl+r)', command=lambda: edit.redo(pad, linepad))
    menubar.add_cascade(label='Edit', menu=editmenu)

    runmenu = GUI.Menu(menubar, tearoff=0)
    runmenu.add_command(label='Compile - (F7)', command=lambda: run.compile(
        app, pad, outputpad, lang))
    runmenu.add_command(label='Run - (F5)', command=lambda: run.run(
        app, pad, outputpad, inputpad, lang))
    menubar.add_cascade(label='Run', menu=runmenu)

    langmenu = GUI.Menu(menubar, tearoff=0)
    langmenu.add_radiobutton(label='c++', command=lambda: change_lang('c++'))
    langmenu.add_radiobutton(label='python', command=lambda: change_lang('py'))
    menubar.add_cascade(label='Language', menu=langmenu)

    pad.bind('<Tab>', lambda event: Display.tab_width(pad, event))
    app2.bind('<Escape>', lambda event: Display.escape(app2, event))
    app2.bind('<Tab>', lambda event: Display.select_first(lb, event))
    app2.bind('<Return>', lambda event: Display.insert_word(app2, pad, lb, lang, event))
    app.bind('<KeyPress>', lambda event: Display.show_in_console(
        event, app2, pad, linepad, lang, lb))
    app.bind('<space>', lambda event: Display.add_to_trie(app2, pad, lb, event))
    app.bind('<Return>', lambda event: Display.indentation(pad, linepad, lang, event))
    app.bind('<F7>', lambda event: run.compile(app, pad, outputpad, lang, event))
    app.bind('<F5>', lambda event: run.run(
        app, pad, outputpad, inputpad, lang, event))

    app.bind('<Control-r>', lambda event: edit.redo(pad, linepad, event))
    app.bind('<Control-z>', lambda event: edit.undo(pad, linepad, event))
    app.bind('<BackSpace>', lambda event: Display.fast_backspace(pad, linepad, event))

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
