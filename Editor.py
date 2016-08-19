#!usr/bin/Python2
"""

A code editor, can also compile and run programs.
Currently supports only C++ in Windows

Now python2 support yay

"""

import Tkinter as GUI
import ttk
import ScrolledText
import commands

lang = ''


class DisplayWidget():
    def __init__(self, book):
        """
        :param book: the tabbed notebook
        :return:
        """
        self.book = book
        self.primary_frame = []
        self.frame_codepad = []
        self.frame_outputpad = []
        self.frame_autocomplete = []
        self.bar_editor = []
        self.lb = []
        self.pad = []
        self.linepad = []
        self.inputpad = []
        self.outputpad = []
        self.W1 = []

    def create_tab(self, *args):

        primary_frame = GUI.Frame(self.book)
        frame_codepad = GUI.Frame(primary_frame)
        frame_autocomplete = GUI.Frame(primary_frame)
        frame_outputpad = GUI.Frame(primary_frame)
        W1 = GUI.PanedWindow(frame_codepad, height=30, width=70)
        bar_editor = GUI.Scrollbar(frame_codepad)
        pad = GUI.Text(W1, height=30, width=60, yscrollcommand=bar_editor.set, undo=True)
        pad.config(fg='#f8f8f2', bg='#002b36', insertbackground='white')
        linepad = GUI.Text(frame_codepad, height=30, width=4, yscrollcommand=bar_editor.set, undo=True)
        linepad.config(fg='#f8f8f2', bg='#002b36', insertbackground='white', state=GUI.DISABLED)
        lb = GUI.Listbox(frame_autocomplete, height=4, width=120)
        lb.config(fg='gray', bg='#002b36')
        inputpad = GUI.Text(W1, height=30, width=30)
        inputpad.config(fg='white', bg='#002b36', insertbackground='white')

        W1.add(pad)
        W1.add(inputpad)

        def share_bar(*event):
            """
            the linenumber abd code textpads share same scrollbar
            :param event: event
            """
            pad.yview(*event)
            linepad.yview(*event)

        bar_editor.config(command=share_bar)

        outputpad = ScrolledText.ScrolledText(frame_outputpad, height=5, width=80)
        outputpad.config(fg='white', bg='#002b36', insertbackground='white', state=GUI.DISABLED)

        primary_frame.pack(side=GUI.LEFT, fill=GUI.BOTH, expand=GUI.YES)
        frame_codepad.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
        linepad.pack(side=GUI.LEFT, fill=GUI.Y)
        W1.pack(side=GUI.LEFT, fill=GUI.BOTH, expand=GUI.YES)
        bar_editor.pack(side=GUI.LEFT, fill=GUI.Y)
        frame_autocomplete.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
        lb.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)

        self.book.add(primary_frame, text='untitled.cpp')

        self.primary_frame.append(primary_frame)
        self.frame_codepad.append(frame_codepad)
        self.frame_outputpad.append(frame_outputpad)
        self.frame_autocomplete.append(frame_autocomplete)
        self.bar_editor.append(bar_editor)
        self.lb.append(lb)
        self.pad.append(pad)
        self.linepad.append(linepad)
        self.inputpad.append(inputpad)
        self.outputpad.append(outputpad)
        self.W1.append(W1)

    def destroy_tab(self):
        if len(self.book.tabs()) == 1:
            return 'break'
        index = self.book.index(self.book.select())
        self.book.forget(self.book.select())
        self.primary_frame.pop(index)
        self.frame_codepad.pop(index)
        self.frame_outputpad.pop(index)
        self.frame_autocomplete.pop(index)
        self.bar_editor.pop(index)
        self.lb.pop(index)
        self.pad.pop(index)
        self.linepad.pop(index)
        self.inputpad.pop(index)
        self.outputpad.pop(index)
        self.W1.pop(index)


def main():
    app = GUI.Tk()
    commands.setKeys()
    display = commands.CodeDisplay()
    cmd_file = commands.FilesFileMenu()
    edit = commands.EditFileMenu()
    run = commands.RunFilemenu()

    book = ttk.Notebook(app)

    def useless():
        print 'sexy'

    def index():
        return book.index(book.select())

    def change_lang(newlang):
        """
        changes current language in editor
        :param newlang: language to switch to
        :return:
        """
        global lang
        lang = newlang
        # r = map(str, app.title().split('.'))
        # if lang == 'c++' and r[-1] == 'py':
        #     app.title('untitled.cpp')
        #     cmd_file.set_new_filedetails('untitled.cpp', os.getcwd() + '/untitled.cpp')
        #     print File.name, File.path
        # if lang == 'py' and r[-1] == 'cpp':
        #     app.title('untitled.py')
        #     cmd_file.set_new_filedetails('untitled.py', os.getcwd() + '/untitled.py')

    change_lang('c++')

    code = DisplayWidget(book)
    code.create_tab()

    menubar = GUI.Menu(app)
    filemenu = GUI.Menu(menubar, tearoff=0)
    filemenu.add_command(label='New', command=useless)
    filemenu.add_command(label='New Tab', command=lambda: cmd_file.create_new_tab(code))
    filemenu.add_command(label='Close Tab', command=lambda: cmd_file.close_tab(code))
    filemenu.add_command(label='Open', command=lambda: cmd_file.Open(
        app, book, code.pad[index()], code.linepad[index()], lang))
    filemenu.add_command(label='Save', command=lambda: cmd_file.Save(
        app, code.pad[index()]))
    filemenu.add_command(label='Save As', command=lambda: cmd_file.Save_As(
        app, code.pad[index()]))
    filemenu.add_command(label='Exit', command=cmd_file.Exit)
    menubar.add_cascade(label='File', menu=filemenu)

    editmenu = GUI.Menu(menubar, tearoff=0)
    editmenu.add_command(label='Undo - (ctrl+z)', command=lambda: edit.undo(
        code.pad[index()], code.linepad[index()]))
    editmenu.add_command(label='Redo - (ctrl+r)', command=lambda: edit.redo(
        code.pad[index()], code.linepad[index()]))
    menubar.add_cascade(label='Edit', menu=editmenu)

    runmenu = GUI.Menu(menubar, tearoff=0)
    runmenu.add_command(label='Compile - (F7)', command=lambda: run.compile(
        app, code.pad[index()], code.outputpad[index()], lang, code.frame_outputpad[index()]))
    runmenu.add_command(label='Run - (F5)', command=lambda: run.run(
        app, code.pad[index()], code.outputpad[index()], code.inputpad[index()], lang, code.frame_outputpad[index()]))
    menubar.add_cascade(label='Run', menu=runmenu)

    langmenu = GUI.Menu(menubar, tearoff=0)
    langmenu.add_radiobutton(label='c++', command=lambda: change_lang('c++'))
    langmenu.add_radiobutton(label='python', command=lambda: change_lang('py'))
    menubar.add_cascade(label='Language', menu=langmenu)

    app.bind('<Escape>', lambda event: display.escape(
        code.frame_autocomplete[index()], code.pad[index()], event))
    app.bind('<Down>', lambda event: display.select_first(
        code.frame_autocomplete[index()], code.lb[index()], code.pad[index()], event))

    code.frame_autocomplete[index()].bind('<Return>', lambda event: display.insert_word(
        code.frame_autocomplete[index()], code.pad[index()], code.lb[index()], lang, event))

    code.pad[index()].bind('<Tab>', lambda event: display.tab_width(code.pad[index()], event))

    app.bind('<KeyPress>', lambda event: display.show_in_console(
        app, book, event, code.pad[index()], code.linepad[index()], lang, code.lb[index()],
        code.frame_codepad[index()], code.W1[index()], code.bar_editor[index()],
        code.frame_outputpad[index()], code.frame_autocomplete[index()], code.outputpad[index()]))

    app.bind('<space>', lambda event: display.add_to_trie(
        code.frame_autocomplete[index()], code.pad[index()], code.lb[index()], event))
    app.bind('<Return>', lambda event: display.indentation(
        code.pad[index()], code.linepad[index()], lang, event))
    app.bind('<F7>', lambda event: run.compile(
        app, code.pad[index()], code.outputpad[index()], lang, code.frame_outputpad[index()], event))
    app.bind('<F5>', lambda event: run.run(
        app, code.pad[index()], code.outputpad[index()], code.inputpad[index()],
        lang, code.frame_outputpad[index()], event))

    app.bind('<Control-r>', lambda event: edit.redo(
        code.pad[index()], code.linepad[index()], lang, event))
    app.bind('<Control-z>', lambda event: edit.undo(
        code.pad[index()], code.linepad[index()], lang, event))
    app.bind('<BackSpace>', lambda event: display.fast_backspace(
        code.pad[index()], code.linepad[index()], event))

    # TODO : Move these somwehre else

    def add_tab(*args):
        cmd_file.create_new_tab(code)
        r = app.geometry().split('+')
        coordinates = map(int,r[0].split('x'))
        # new_tab_button.place_forget()
        # new_tab_button.place(x = coordinates[0] - 60, y = -0.5)

    def remove_tab(*args):
        cmd_file.close_tab(code)
        r = app.geometry().split('+')
        coordinates = map(int,r[0].split('x'))
        # del_tab_button.place_forget()
        # del_tab_button.place(x = coordinates[0] - 30, y = -0.5)

    # new_tab_button = GUI.Button(book,text = 'add',bg='#228b22',fg='white')
    # new_tab_button.place(x = 740, y = -0.5)
    # new_tab_button.bind('<Button-1>',add_tab)
    #
    # del_tab_button = GUI.Button(book,text = 'del',bg='maroon',fg='white')
    # del_tab_button.place(x = 770, y=-0.5)
    # del_tab_button.bind('<Button-1>', remove_tab)

    book.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
    app.config(menu=menubar)
    app.geometry('800x600')
    app.title('CodeEditor')
    app.mainloop()

if __name__ == '__main__':
    main()

