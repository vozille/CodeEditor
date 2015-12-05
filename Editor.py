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

app3 = Tk()
compilepad = Text(app3,height = 5,width = 40)
compilepad.pack(side = TOP,fill = BOTH)
app3.withdraw()

class FileDetails(object):
    def __init__(self):
        self.path = ''
        self.name = ''
        self.execute = ''
    def Filename(self,data):
        self.name = data
    def FilePath(self,data):
        self.path = data
    def Execpath(self,data):
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
        r = pad.get('1.0', END)
        r = map(str, r.split())
        if not MyDict.contains(r[-1]):
            MyDict.insert(self.remove_punc(r[-1]))

    def show_in_console(self, event):
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

    def syntax_highlight(self,pos = INSERT,flag = 0):
        pad.tag_configure('default', foreground='#e0115f')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')
        pad.tag_configure('normal',foreground = '#f8f8f2')
        pad.tag_configure('quotes', foreground='gold')
        coordinates1 = map(int,pad.index(pos).split('.'))
        coordinates = str(coordinates1[0]) + '.0'
        if flag:
            coordinates = '1.0'
            pos = 'end'
        else:
            pos = pos + ' lineend'
        r = pad.get(coordinates,pos)
        brackets = ['(',')','[',']','{','}','<','>',',']
        for i in brackets:
            r = r.replace(i,' ')
        s = r
        r = map(str,s.split())
        t = map(str,s.split('\n'))
        for i in r:
            ncoordinates = str(coordinates1[0]) + '.' + str(s.index(i))
            if i in keywords['default']:
                self.highlight_pattern(i,'default',ncoordinates,pos)
            elif i in keywords['loops']:
                self.highlight_pattern(i,'loops',ncoordinates,pos)
            elif i in keywords['P_datatypes']:
                self.highlight_pattern(i,'P_datatypes',ncoordinates,pos)

        pattern = '"([A-Za-z0-9_\./\\-]*)"'
        self.highlight_pattern(pattern,'quotes','1.0','end',True)

        pattern = "'([A-Za-z0-9_\./\\-]*)'"
        self.highlight_pattern(pattern,'quotes','1.0','end',True)

    def open_highlight(self):

        pad.tag_configure('default', foreground='#e0115f')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')
        pad.tag_configure('quotes', foreground='gold')
        for i in keywords:
            for j in keywords[i]:
                self.highlight_pattern(j,i)

        pattern = '"([A-Za-z0-9_\./\\-]*)"'
        self.highlight_pattern(pattern,'quotes','1.0','end',True)
        pattern = "'([A-Za-z0-9_\./\\-]*)'"
        self.highlight_pattern(pattern,'quotes','1.0','end',True)

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

    def highlight_pattern(self, pattern, tag, start="1.0",end="end", regexp=False):
        start = pad.index(start)
        end = pad.index(end)
        pad.mark_set("matchStart", start)
        pad.mark_set("matchEnd", start)
        pad.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = pad.search(pattern, "matchEnd", "searchLimit",count=count, regexp=regexp)
            if index == "":
                break
            pad.mark_set("matchStart", index)
            pad.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            pad.tag_add(tag, "matchStart", "matchEnd")

    def linenumber(self):
        linepad.config(state = NORMAL)
        coordinate_pad = map(int,pad.index(END).split('.'))
        linepad.delete('1.0',END)
        for i in range(coordinate_pad[0]-1):
            linepad.insert(END,str(i+1)+'.\n')
        linepad.config(state = DISABLED)

Display = display_func()


class cmd_filemenu(object):

    def __init__(self):
        pass

    def Exit(self):
        exit(0)

    def Open(self):
        from tkFileDialog import askopenfilename
        open_file = askopenfilename(parent=app)
        pad.delete('1.0', END)
        pad.insert(END, open(open_file).read())
        Display.open_highlight()
        Display.linenumber()
        x = open_file
        x = x.replace('/','\\')
        File.Filename(map(str,x.split('\\'))[-1])
        File.FilePath(x)
        File.Execpath(x.replace('cpp','exe'))
        app.title(File.name)

    def Save(self):
        from tkFileDialog import asksaveasfilename
        save_file = asksaveasfilename(parent=app)
        data = pad.get('1.0', END)
        sys.stdout = open(save_file, 'w')
        print data
        sys.stdout = sys.__stdout__
        x = save_file
        x = x.replace('/','\\')
        File.Filename(map(str,x.split('\\'))[-1])
        File.FilePath(x)
        app.title(File.name)

cmd_file = cmd_filemenu()

class runFilemenu(object):
    def __init__(self):
        pass
    def compile(self):
        app3.deiconify()
        p = subprocess.Popen(["C:\\Program Files (x86)\\MinGW\\bin\\g++.exe", "-Wall", "-o", File.path,File.name]\
                     , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = p.communicate()[1]
        if len(status) == 0:
            compilepad.insert(END,'compiled successfully \n')
        else:
            compilepad.insert(END,status + '\n')

    def run(self):
        compilepad.insert(END,subprocess.check_output([File.execute]))

run = runFilemenu()


def hello():
    c = map(int,pad.index(INSERT).split('.'))
    c[-1] -= 1
    pad.delete(str(c[0])+'.'+str(c[-1]),END)

def shareBar(*args):
    pad.yview(*args)
    linepad.yview(*args)
def shareMouseWheel(event):
    pad.yview('scroll',event.delta,'units')
    linepad.yview('scroll',event.delta,'units')
    return 'break'
bar = Scrollbar(app)
pad = Text(app, height=20, width=80,yscrollcommand = bar.set)
pad.config(fg='#f8f8f2', bg='#272822', insertbackground='white')

linepad = Text(app, height=20, width=4,yscrollcommand = bar.set)
linepad.config(fg='#f8f8f2', bg='#272822', insertbackground='white',state = DISABLED)


bar.config(command = shareBar)

menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='New', command=hello)
filemenu.add_command(label='Open', command=cmd_file.Open)
filemenu.add_command(label='Save', command=cmd_file.Save)
filemenu.add_command(label='Exit', command=cmd_file.Exit)
menubar.add_cascade(label='File', menu=filemenu)

runmenu = Menu(menubar,tearoff = 0)
runmenu.add_command(label = 'Compile',command = run.compile)
runmenu.add_command(label = 'Run',command = run.run)
menubar.add_cascade(label='Run', menu=runmenu)

app.bind('<KeyPress>', Display.show_in_console)
app.bind('<space>', Display.addToTrie)
app.bind('<Return>', Display.indentation)
linepad.pack(side = LEFT,fill=Y)
pad.pack(side = LEFT,fill=BOTH, expand=YES)
bar.pack(side = LEFT,fill = Y)
app.config(menu=menubar)
app.title('untitled.cpp')
app.mainloop()
app2.mainloop()
app3.title('run status')
app3.mainloop()
