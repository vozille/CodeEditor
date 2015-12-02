import Tkinter
from Tkinter import *
from functools import reduce


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
    'return',
    'namespace',
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
        self.highlight()
        r = pad.get('1.0', INSERT)
        r = map(str, r.split())
        if len(r) != 0:
            x = MyDict.autocomplete(r[-1])
            lb = Listbox(app2, height=10, width=30)
            if len(x) and len(r):
                for i in x:
                    lb.insert(END, i + '\n')
            lb.grid(row=1, column=1)

            pad.tag_configure('num', foreground='#d462ff')
            try:
                float(r[-1])
                self.highlight_pattern(r[-1], 'num')
            except ValueError:
                pass

    def highlight(self):
        pad.tag_configure('default', foreground='red')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')

        for word in keywords['default']:
            self.highlight_pattern(word, 'default')
        for word in keywords['loops']:
            self.highlight_pattern(word, 'loops')
        for word in keywords['P_datatypes']:
            self.highlight_pattern(word, 'P_datatypes')

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

    def highlight_pattern(self, pattern, tag, start="1.0",
                          end="end", regexp=False):
        start = pad.index(start)
        end = pad.index(end)
        pad.mark_set("matchStart", start)
        pad.mark_set("matchEnd", start)
        pad.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = pad.search(pattern, "matchEnd", "searchLimit",
                               count=count, regexp=regexp)
            if index == "":
                break
            pad.mark_set("matchStart", index)
            pad.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            pad.tag_add(tag, "matchStart", "matchEnd")
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
        Display.highlight()

    def Save(self):
        from tkFileDialog import asksaveasfilename
        save_file = asksaveasfilename(parent=app)
        data = pad.get('1.0', END)
        sys.stdout = open(save_file, 'w')
        print data
        sys.stdout = sys.__stdout__
cmd_file = cmd_filemenu()

def hello():
    print 'pass'

pad = Text(app, height=20, width=80)
pad.config(fg='white', bg='black', insertbackground='white')

menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='New', command=hello)
filemenu.add_command(label='Open', command=cmd_file.Open)
filemenu.add_command(label='Save', command=cmd_file.Save)
filemenu.add_command(label='Exit', command=cmd_file.Exit)
menubar.add_cascade(label='File', menu=filemenu)


app.bind('<KeyPress>', Display.show_in_console)
app.bind('<space>', Display.addToTrie)
#app.bind('<Return>', Display.addToTrie)
app.bind('<Return>', Display.indentation)
pad.pack(fill=BOTH, expand=YES)
app.config(menu=menubar)
app.mainloop()
app2.mainloop()
