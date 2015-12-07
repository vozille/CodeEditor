"""
A C++ editor, can also compile and run C++ programs.
Must save before compiling.

Pretty much incomplete now, barely works.
"""
#!usr/bin/Python2

import Tkinter
from ScrolledText import *
from Tkinter import *
from functools import reduce
import os
import subprocess


class Trie(object):

    def __init__(self):
        self.children = {}
        self.flag = False  # Flag to represent that a word ends at this node

    def add(self, char):
        self.children[char] = Trie()

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.add(char)
            node = node.children[char]
        node.flag = True

    def contains(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.flag

    def all_suffixes(self, prefix):
        results = set()
        if self.flag:
            results.add(prefix)
        if not self.children:
            return results
        return reduce(lambda a, b: a | b, [node.all_suffixes(
            prefix + char) for (char, node) in self.children.items()]) | results

    def autocomplete(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return set()
            node = node.children[char]
        return list(node.all_suffixes(prefix))
MyDict = Trie()

keywords = {}
keywords['default'] = [
    'main',
    '#include',
    'typedef',
    'using',
    'const',
    'return',
    'cin',
    'cout',
    'scanf',
    'printf']
keywords['loops'] = ['for', 'while', 'do', 'if', 'else', 'switch']
keywords['P_datatypes'] = [
    'int',
    'float',
    'double',
    'long',
    'string',
    'char',
    'bool',
    'void',
    'struct',
    'auto',
    'NULL']
app = Tkinter.Tk()
app2 = Tk()
app2.withdraw()

FLAG = 1

class FileDetails(object):

    def __init__(self):
        self.path = ''
        self.name = ''
        self.execute = ''

    def Filename(self, data):
        self.name = data

    def FilePath(self, data):
        self.path = data

    def Execpath(self, data):
        self.execute = data
File = FileDetails()


class display_func(object):

    def __init__(self):
        pass

    def remove_punc(self, r):

        c = ''
        from string import punctuation
        for d in r:
            if d not in punctuation and d != ';' and d != ':' and d != '(' and d != ')':
                c += d
        return c

    def defaultWords(self):
        pad.edit_separator()
        import sys
        sys.stdin = open('input.txt', 'r')
        while True:
            try:
                r = map(str, raw_input().split())
                for i in r:
                    MyDict.insert(self.remove_punc(i))
            except EOFError:
                return
        self.defaultWords()

    def addToTrie(self, event):
        pad.edit_separator()
        r = pad.get('1.0', END)
        r = map(str, r.split())
        if not MyDict.contains(r[-1]):
            MyDict.insert(self.remove_punc(r[-1]))

    def show_in_console(self, event):
        pad.edit_separator()
        global FLAG
        FLAG = 1
        self.syntax_highlight()
        self.linenumber()
        r = pad.get('1.0', INSERT)
        r = map(str, r.split())
        if len(r) != 0:
            x = MyDict.autocomplete(r[-1])
            lb = Listbox(app2, height=10, width=30)
            if len(x) and len(r):
                for i in x:
                    lb.insert(END, i + '\n')
            lb.grid(row=1, column=1)

            pad.tag_configure('num', foreground='#ff69b4')
            try:
                float(r[-1])
                self.highlight_pattern(r[-1], 'num')
            except ValueError:
                pass

    def syntax_highlight(self, pos=INSERT, flag=0):
        pad.edit_separator()
        pad.tag_configure('default', foreground='#e0115f')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')
        pad.tag_configure('normal', foreground='#f8f8f2')
        pad.tag_configure('quotes', foreground='gold')
        coordinates1 = map(int, pad.index(pos).split('.'))
        coordinates = str(coordinates1[0]) + '.0'
        if flag:
            coordinates = '1.0'
            pos = 'end'
        else:
            pos = pos + ' lineend'
        r = pad.get(coordinates, pos)
        brackets = ['(', ')', '[', ']', '{', '}', '<', '>', ',']
        for i in brackets:
            r = r.replace(i, ' ')
        s = r
        r = map(str, s.split())
        t = map(str, s.split('\n'))
        for i in r:
            ncoordinates = str(coordinates1[0]) + '.' + str(s.index(i))
            if i in keywords['default']:
                self.highlight_pattern(i, 'default', ncoordinates, pos)
            elif i in keywords['loops']:
                self.highlight_pattern(i, 'loops', ncoordinates, pos)
            elif i in keywords['P_datatypes']:
                self.highlight_pattern(i, 'P_datatypes', ncoordinates, pos)


        pattern = '"([A-Za-z0-9_\./\\-]*)"'
        self.highlight_pattern(pattern, 'quotes', '1.0', 'end', True)

        pattern = "'([A-Za-z0-9_\./\\-]*)'"
        self.highlight_pattern(pattern, 'quotes', '1.0', 'end', True)

    def open_highlight(self):

        pad.tag_configure('default', foreground='#e0115f')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')
        pad.tag_configure('quotes', foreground='gold')
        for i in keywords:
            for j in keywords[i]:
                self.highlight_pattern(j, i)

        pattern = '"([A-Za-z0-9_\./\\-]*)"'
        self.highlight_pattern(pattern, 'quotes', '1.0', 'end', True)
        pattern = "'([A-Za-z0-9_\./\\-]*)'"
        self.highlight_pattern(pattern, 'quotes', '1.0', 'end', True)

    """
    unused now

    def highlight(self):
        pad.tag_configure('default', foreground='#e0115f')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')
        pad.tag_configure('quotes', foreground='gold')
        for word in keywords['default']:
            self.highlight_pattern(word, 'default')
        for word in keywords['loops']:
            self.highlight_pattern(word, 'loops')
        for word in keywords['P_datatypes']:
            self.highlight_pattern(word, 'P_datatypes')
        pattern = '"([A-Za-z0-9_\./\\-]*)"'
        self.highlight_pattern(pattern,'quotes','1.0','end',True)
        pattern = "'([A-Za-z0-9_\./\\-]*)'"
        self.highlight_pattern(pattern,'quotes','1.0','end',True)

    """

    def indentation(self, event):
        pad.edit_separator()
        curr = pad.get('1.0', INSERT)
        till_end = pad.get('1.0', END)
        indent = max(curr.count("{") - curr.count('}'), 0)
        diff = till_end.count('{') - till_end.count('}')
        pad.insert(INSERT, '    ' * indent)
        cordinate = map(int, pad.index(INSERT).split('.'))
        if diff > 0:
            pad.insert(INSERT, '\n' + '    ' * max(indent - 1, 0) + '}')
            pad.mark_set(INSERT, '%d.%d' % (cordinate[0], cordinate[1]))
        self.linenumber()

    def highlight_pattern(
            self,
            pattern,
            tag,
            start="1.0",
            end="end",
            regexp=False):
        start = pad.index(start)
        end = pad.index(end)
        pad.mark_set("matchStart", start)
        pad.mark_set("matchEnd", start)
        pad.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = pad.search(
                pattern,
                "matchEnd",
                "searchLimit",
                count=count,
                regexp=regexp)
            if index == "":
                break
            pad.mark_set("matchStart", index)
            pad.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            pad.tag_add(tag, "matchStart", "matchEnd")

    def linenumber(self):
        linepad.config(state=NORMAL)
        coordinate_pad = map(int, pad.index(END).split('.'))
        linepad.delete('1.0', END)
        for i in range(coordinate_pad[0] - 1):
            linepad.insert(END, str(i + 1) + '.\n')
        linepad.config(state=DISABLED)

Display = display_func()


class cmd_filemenu(object):

    def __init__(self):
        pass

    def Exit(self):
        exit(0)

    def Open(self):
        from tkFileDialog import askopenfilename
        open_file = askopenfilename(parent=app)
        if len(open_file) == 0:
            return
        pad.delete('1.0', END)
        pad.insert(END, open(open_file).read())
        Display.open_highlight()
        Display.linenumber()
        x = open_file
        x = x.replace('/', '\\')
        File.Filename(map(str, x.split('\\'))[-1])
        File.FilePath(x)
        File.Execpath(x.replace('cpp', 'exe'))
        app.title(File.name)

    def Save(self):
        from tkFileDialog import asksaveasfilename
        save_file = asksaveasfilename(parent=app)
        data = pad.get('1.0', END)[:-1]
        f = open(save_file, 'w')
        f.write(data)
        f.close()
        x = save_file
        x = x.replace('/', '\\')
        File.Filename(map(str, x.split('\\'))[-1])
        File.FilePath(x)
        app.title(File.name)

cmd_file = cmd_filemenu()

class editFileMenu(object):

    def undo(self,*argv):
        try:
            pad.edit_undo()
            Display.linenumber()
            Display.open_highlight()
        except TclError:
            pass
    def redo(self,*argv):
        try:
            pad.edit_redo()
            Display.linenumber()
            Display.open_highlight()
        except TclError:
            pass
    def select_all(self):
        pass

edit = editFileMenu()

class runFilemenu(object):

    def __init__(self):
        pass

    def compile(self):
        global FLAG
        FLAG = 0
        # remove the old exe and replace it with current one
        try:
            os.remove('a.exe')
        except WindowsError:
            pass
        # Save file automatically before compiling
        data = pad.get('1.0', END)[:-1]
        f = open(File.path, 'w')
        f.write(data)
        f.close()

        outputpad.config(state=NORMAL)
        outputpad.delete('1.0', END)
        p = subprocess.Popen(
            [
                "C:\\Program Files (x86)\\MinGW\\bin\\g++.exe",
                '-std=c++14',
                File.path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        status = p.communicate()[1]
        if len(status) == 0:
            outputpad.insert(END, 'compiled successfully \n')
        else:
            outputpad.insert(END, status + '\n')
            p.terminate()
            return -1
        p.terminate()
        outputpad.config(state=DISABLED)


    def run(self):
        if FLAG:
            x = self.compile()
            # compilation failed, terminate
            if x == -1:
                return
        outputpad.config(state=NORMAL)
        r = inputpad.get('1.0', END)
        f = open('input.txt', 'w')
        f.write(r)
        f.close()
        os.system('a.exe<input.txt >output.txt')
        r = open('output.txt').read()
        outputpad.delete('1.0', END)
        outputpad.insert(END, r)
        outputpad.config(state=DISABLED)


run = runFilemenu()


def hello():
    c = map(int, pad.index(INSERT).split('.'))
    c[-1] -= 1
    pad.delete(str(c[0]) + '.' + str(c[-1]), END)


def shareBar(*args):
    pad.yview(*args)
    linepad.yview(*args)


def shareMouseWheel(event):
    pad.yview('scroll', event.delta, 'units')
    linepad.yview('scroll', -1 * (event.delta / 120), 'units')
    return 'break'


frame1 = Frame(app)
frame12 = Frame(app)
frame2 = Frame(app)
W1 = PanedWindow(frame1, height=30, width=70)
bar_editor = Scrollbar(frame1)
bar_input_h = Scrollbar(frame12, orient=HORIZONTAL)

# 272822
pad = Text(W1, height=30, width=60, yscrollcommand=bar_editor.set, undo = True)
pad.config(fg='#f8f8f2', bg='#002b36', insertbackground='white')

linepad = Text(frame1, height=30, width=4, yscrollcommand=bar_editor.set, undo = True)
linepad.config(
    fg='#f8f8f2',
    bg='#002b36',
    insertbackground='white',
    state=DISABLED)

inputpad = Text(W1, height=30, width=30, xscrollcommand=bar_input_h.set)
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
    state=DISABLED)

menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='New', command=hello)
filemenu.add_command(label='Open', command=cmd_file.Open)
filemenu.add_command(label='Save', command=cmd_file.Save)
filemenu.add_command(label='Exit', command=cmd_file.Exit)
menubar.add_cascade(label='File', menu=filemenu)

editmenu = Menu(menubar, tearoff = 0)
editmenu.add_command(label = 'Undo', command = edit.undo)
editmenu.add_command(label = 'Redo', command = edit.redo)
menubar.add_cascade(label = 'Edit', menu = editmenu)

runmenu = Menu(menubar, tearoff=0)
runmenu.add_command(label='Compile', command=run.compile)
runmenu.add_command(label='Run', command=run.run)
menubar.add_cascade(label='Run', menu=runmenu)

app.bind('<KeyPress>', Display.show_in_console)
app.bind('<space>', Display.addToTrie)
app.bind('<Return>', Display.indentation)
app.bind('<Control-r>',edit.redo)
app.bind('<Control-z>',edit.undo)

frame1.pack(side=TOP, fill=BOTH, expand=YES)
linepad.pack(side=LEFT, fill=Y)
W1.pack(side=LEFT, fill=BOTH, expand=YES)
# pad.pack(side = LEFT,fill=BOTH, expand=YES)
bar_editor.pack(side=LEFT, fill=Y)
# inputpad.pack(side = LEFT,fill=Y)
frame12.pack(side=TOP, fill=BOTH)
frame2.pack(side=TOP, fill=BOTH, expand=YES)
bar_input_h.pack(side=RIGHT)
outputpad.pack(side=TOP, fill=BOTH, expand=YES)

app.config(menu=menubar)
app.title('untitled.cpp')
app.mainloop()
app2.mainloop()
