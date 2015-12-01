import sys
class Trie(object):
    def __init__(self):
        self.children = {}
        self.flag = False # Flag to represent that a word ends at this node

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
        if not self.children: return results
        return reduce(lambda a, b: a | b, [node.all_suffixes(prefix + char) for (char, node) in self.children.items()]) | results

    def autocomplete(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return set()
            node = node.children[char]
        return list(node.all_suffixes(prefix))

keywords = {}
keywords['default'] = ['main','#include','return','namespace','return','cin','cout','scanf','printf']
keywords['loops'] = ['for','while','do','if','else','switch']
keywords['P_datatypes'] = ['int','float','double','long','string','char','bool','void','struct','NULL']
import Tkinter
from Tkinter import *
app = Tkinter.Tk()
app2 = Tk()
MyDict = Trie()

def remove_punc(r):
    c = ''
    from string import punctuation
    for d in r:
        if d not in punctuation and d != ';' and d != ':' and d != '(' and d != ')':
            c += d
    return c

def defaultWords():
    import sys
    sys.stdin = open('input.txt','r')
    while True:
        try:
            r = map(str,raw_input().split())
            for i in r:
                MyDict.insert(remove_punc(i))
        except EOFError:
            return
defaultWords()

def addToTrie(event):
    r = pad.get('1.0',END)
    r = map(str,r.split())
    if not MyDict.contains(r[-1]):
        MyDict.insert(remove_punc(r[-1]))

    """
    piece of old crap
    """

    # pad.tag_configure('default',foreground = 'red')
    # pad.tag_configure('loops',foreground = 'green')
    # pad.tag_configure('P_datatypes',foreground = 'aqua')
    # pad.tag_configure('num',foreground = '#d462ff')

    # cordinate = map(int,pad.index(INSERT).split('.'))
    # r = pad.get(str(cordinate[0])+'.0',INSERT)[:-1]
    # try:
    #     start = r.rindex(' ') + 1
    # except ValueError:
    #     start = 0
    # word = r[start:]
    # if len(word) == 0:
    #     return
    # if word[0] == '(' or word[0] == '<':
    #     word = word[1:]
    #     start += 1
    # if word[-1] == ')' or word[-1] == '>' or word[-1] == ';':
    #     word = word[:-1]
    # if word in keywords['default']:
    #     pad.tag_add('default',str(cordinate[0])+'.'+str(start),INSERT)
    # if word in keywords['loops']:
    #     pad.tag_add('loops',str(cordinate[0])+'.'+str(start),INSERT)
    # if word in keywords['P_datatypes']:
    #     pad.tag_add('P_datatypes',str(cordinate[0])+'.'+str(start),INSERT)
    # try:
    #     float(word)
    #     pad.tag_add('num',str(cordinate[0])+'.'+str(start),INSERT)
    # except ValueError:
    #     pass

def show_in_console(event):
    highlight()
    r = pad.get('1.0',INSERT)
    r = map(str,r.split())
    if len(r) != 0:
        x = MyDict.autocomplete(r[-1])
        lb = Listbox(app2,height = 10,width = 30)
        if len(x) and len(r):
            for i in x:
                lb.insert(END,i+'\n')
        lb.grid(row = 1, column = 1)

        pad.tag_configure('num',foreground = '#d462ff')
        try:
            float(r[-1])
            highlight_pattern(r[-1],'num')
        except ValueError:
            pass

def highlight():
    pad.tag_configure('default',foreground = 'red')
    pad.tag_configure('loops',foreground = 'green')
    pad.tag_configure('P_datatypes',foreground = 'aqua')

    for word in keywords['default']:
        highlight_pattern(word,'default')
    for word in keywords['loops']:
        highlight_pattern(word,'loops')
    for word in keywords['P_datatypes']:
        highlight_pattern(word,'P_datatypes')

def indentation(event):
    curr = pad.get('1.0',INSERT)
    till_end = pad.get('1.0',END)
    indent = max(curr.count("{") - curr.count('}'),0)
    diff = till_end.count('{') - till_end.count('}')
    pad.insert(INSERT,'    '*indent)
    cordinate = map(int,pad.index(INSERT).split('.'))
    if diff > 0:
        pad.insert(INSERT,'\n'+ '    '*max(indent - 1,0) + '}')
        pad.mark_set(INSERT,'%d.%d' %(cordinate[0],cordinate[1]))

def hello():
    print pad.search('main','1.0',END)


def highlight_pattern(pattern, tag, start="1.0", end="end",regexp=False):
    start = pad.index(start)
    end = pad.index(end)
    pad.mark_set("matchStart", start)
    pad.mark_set("matchEnd", start)
    pad.mark_set("searchLimit", end)

    count = IntVar()
    while True:
        index = pad.search(pattern, "matchEnd","searchLimit",
                            count=count, regexp=regexp)
        if index == "": break
        pad.mark_set("matchStart", index)
        pad.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
        pad.tag_add(tag, "matchStart", "matchEnd")

class cmd_filemenu():
    def Exit(self):
        exit(0)
    def Open(self):
        from tkFileDialog import askopenfilename
        open_file = askopenfilename(parent = app)
        pad.delete('1.0',END)
        pad.insert(END,open(open_file).read())
    def Save(self):
        from tkFileDialog import asksaveasfilename
        save_file = asksaveasfilename(parent = app)
        data = pad.get('1.0',END)
        sys.stdout = open(save_file,'w')
        print data
        sys.stdout = sys.__stdout__


cmd_file = cmd_filemenu()

pad = Text(app,height = 20,width = 80)
pad.config(fg = 'white',bg = 'black',insertbackground = 'white')

menubar = Menu(app)

filemenu = Menu(menubar,tearoff = 0)
filemenu.add_command(label = 'New',command = hello)
filemenu.add_command(label = 'Open',command = cmd_file.Open)
filemenu.add_command(label = 'Save',command = cmd_file.Save)
filemenu.add_command(label = 'Exit',command = cmd_file.Exit)

menubar.add_cascade(label = 'File', menu = filemenu)


app.bind('<KeyPress>',show_in_console)
app.bind('<space>',addToTrie)
app.bind('<Return>',addToTrie)
app.bind('<Return>',indentation)
pad.grid(row = 2,column = 1)
app.config(menu = menubar)
app.mainloop()
app2.mainloop()
