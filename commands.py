# !usr/bin/Python2
"""
The command list which brings life to the GUI :P
"""

import Tkinter as GUI
import os
import subprocess
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
        return reduce(
            lambda a, b: a | b,
            [node.all_suffixes(prefix + char)
             for (char, node) in self.children.items()]) | results

    def autocomplete(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return set()
            node = node.children[char]
        return list(node.all_suffixes(prefix))


MyDict = Trie()

keywords = {}


def setKeys():
    """
    sets default keywords for each language
    :return:
    """
    keywords['c++'] = {}
    with open('cppkeywords.txt', 'r') as f:
        for i in f:
            i = i.strip('\n')
            words = map(str, i.split())
            key = words[0]
            words.pop(0)
            keywords['c++'][key] = list(words)
            for j in words:
                MyDict.insert(j)
    keywords['py'] = {}
    with open('pykeywords.txt', 'r') as f:
        for i in f:
            i = i.strip('\n')
            words = map(str, i.split())
            key = words[0]
            words.pop(0)
            keywords['py'][key] = list(words)
            for j in words:
                MyDict.insert(j)


FLAG = 1


class FileDetails(object):
    """
    stores current file details
    """

    def __init__(self):
        self.path = ''
        self.name = ''
        self.execute = ''

    def filename(self, data):
        self.name = data

    def filepath(self, data):
        self.path = data

    def execpath(self, data):
        self.execute = data


File = FileDetails()

"""
Variables used here :
:param app: the main window
:param frame2: the window for autocomplete
:param pad: the textbox in which code is written
:param lb: the listbox storing autocomplete words
:param lang: programming language
:param linepad: textbox contain lines
:param inputpad: textbox for storing input
:param outputpad: textbox for storing output
:param args: mostly to pass event bindings

:return:
"""


class codeDisplay(object):
    def __init__(self):
        self.cntlbcall = 0
        self.lastinsert = '0.0'

    def escape(self, frame2, pad, *args):
        """
        closes the suggestions box
        """
        self.cntlbcall = 0
        frame2.pack_forget()
        global FLAG
        FLAG = 1
        pad.focus()

    def select_first(self, frame2, lb, pad, event):
        """
        selects the first item in listbox so that it can be navigated
        """
        if lb.size() == 0:
            return
        # self.lastinsert = pad.index(GUI.INSERT)
        frame2.focus()
        lb.select_set(self.cntlbcall)
        lb.see(self.cntlbcall)

        if self.cntlbcall != 0:
            lb.select_clear(self.cntlbcall - 1)
        self.cntlbcall += 1
        if self.cntlbcall > lb.size():
            self.escape(frame2, pad)

    def tab_width(self, pad, *args):
        """
        sets tab with to 4 spaces, std everywhere

        """
        pad.insert(GUI.INSERT, ' ' * 4)
        return 'break'

    def show_outputpad(self, frame2, outputpad):

        frame2.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
        outputpad.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)

    def hide_outputpad(self, frame2, outputpad):

        frame2.pack_forget()
        outputpad.pack_forget()

    def remove_punc(self, r):
        """
        removes punctuation from words
        """
        c = ''
        useless = ['(', ')', '[', ']', '{', '}', '<', '>', ',', '+', '-', '*', '/', '=', ',', '.']
        for d in r:
            if d not in useless:
                c += d
        return c

    def insert_word(self, frame2, pad, lb, lang, *args):
        """
        inserts word to the codepad from the autocomplete box
        """
        # print self.lastinsert

        if self.cntlbcall != 0:
            self.cntlbcall -= 1
        word = lb.get(self.cntlbcall).strip('\n')
        pad.focus()
        coordinates1 = map(int, str(self.lastinsert).split('.'))
        coordinates = str(coordinates1[0]) + '.0'
        r = pad.get(coordinates, str(self.lastinsert))

        pos_space = 0
        for i in range(len(r)):
            if r[i] == ' ':
                pos_space = i
        if pos_space != 0:
            pos_space += 1
        coordinates = str(coordinates1[0]) + '.' + str(pos_space)
        pad.delete(coordinates, coordinates + 'lineend')
        pad.insert(self.lastinsert, word)
        coordinates1 = map(int, str(self.lastinsert).split('.'))
        coordinates1[-1] += len(word)
        pad.mark_set(GUI.INSERT, '%d.%d' % (coordinates1[0], coordinates1[1]))
        self.syntax_highlight(pad, lang, self.lastinsert, 0)
        frame2.pack_forget()
        global FLAG
        FLAG = 1
        self.cntlbcall = 0

    def add_to_trie(self, frame2, pad, lb, *args):
        """
        adds words to trie
        """
        global FLAG
        FLAG = 1
        frame2.pack_forget()
        pad.edit_separator()
        r = pad.get('1.0', GUI.END)
        r = map(str, r.split())
        if not MyDict.contains(r[-1]):
            MyDict.insert(self.remove_punc(r[-1]))

    def show_in_console(self, event, pad, linepad, lang, lb, frame1, W1, bar, frame2, W2, outputpad):
        """
        shows words in console. The main function which has
        keypress bind to it, so it calls many other important
        functions
        """
        pad.edit_separator()
        lb.delete(0, GUI.END)
        global FLAG
        self.hide_outputpad(frame2, outputpad)
        self.syntax_highlight(pad, lang, GUI.INSERT, 0)
        self.linenumber(pad, linepad)
        self.lastinsert = pad.index(GUI.INSERT)

        r = pad.get('1.0', GUI.INSERT)
        r = map(str, r.split())
        # turn on autocomplete if letter detected
        letters = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
        try:
            # pack in the same order
            if r[-1] in letters:
                if FLAG:
                    # frame1.pack_forget()
                    # linepad.pack_forget()
                    # W1.pack_forget()
                    # bar.pack_forget()
                    frame2.pack_forget()
                    lb.pack_forget()
                    # W2.pack_forget()
                    # outputpad.pack_forget()

                    # frame1.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
                    # linepad.pack(side=GUI.LEFT, fill=GUI.Y)
                    # W1.pack(side=GUI.LEFT, fill=GUI.BOTH, expand=GUI.YES)
                    # bar.pack(side=GUI.LEFT, fill=GUI.Y)
                    W2.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
                    lb.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
                    # frame2.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
                    # outputpad.pack(side=GUI.TOP, fill=GUI.BOTH, expand=GUI.YES)
                    FLAG = 0
                    self.cntlbcall = 0
        except IndexError:
            pass
        if len(r) != 0:
            x = MyDict.autocomplete(r[-1])
            if len(x) and len(r):
                # self.cntlbcall = 0
                for i in x:
                    lb.insert(GUI.END, i + '\n')

            pad.tag_configure('num', foreground='#ff69b4')
            r = ''.join(r)
            brackets = ['(', ')', '[', ']', '{', '}', '<', '>', ',', '+', '-', '*', '/']
            for i in brackets:
                r = r.replace(i, ' ')
            r = map(str, r.split())
            try:
                float(r[-1])
                self.highlight_pattern(pad, r[-1], 'num')
            except ValueError:
                pass

    """
    fix
    """

    def syntax_highlight(self, pad, lang='c++', pos=GUI.INSERT, flag=0):
        """
        highlights syntax
        """
        pad.edit_separator()
        pad.tag_configure('default', foreground='#e0115f')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')
        pad.tag_configure('normal', foreground='#f8f8f2')
        pad.tag_configure('quotes', foreground='gold')
        pad.tag_configure('A_datatypes', foreground='orange')
        pad.tag_configure('num', foreground='#ff69b4')

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
            if i in keywords[lang]['default']:
                self.highlight_pattern(pad, i, 'default', ncoordinates, pos)
            if i in keywords[lang]['loops']:
                self.highlight_pattern(pad, i, 'loops', ncoordinates, pos)
            if i in keywords[lang]['P_datatypes']:
                self.highlight_pattern(
                    pad, i, 'P_datatypes', ncoordinates, pos)
            if i in keywords[lang]['A_datatypes']:
                self.highlight_pattern(
                    pad, i, 'A_datatypes', ncoordinates, pos)

        pattern = '"([A-Za-z0-9_\./\\-]*)"'
        self.highlight_pattern(pad, pattern, 'quotes', '1.0', 'end', True)

        pattern = "'([A-Za-z0-9_\./\\-]*)'"
        self.highlight_pattern(pad, pattern, 'quotes', '1.0', 'end', True)

    """
    fix
    """

    def open_highlight(self, pad, lang='c++'):
        """
        highlights syntax when opening a file
        """
        pad.tag_configure('default', foreground='#e0115f')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')
        pad.tag_configure('quotes', foreground='gold')
        pad.tag_configure('A_datatypes', foreground='orange')
        for i in keywords[lang]:
            for j in keywords[lang][i]:
                self.highlight_pattern(pad, j, i)

        pattern = '"([A-Za-z0-9_\./\\-]*)"'
        self.highlight_pattern(pad, pattern, 'quotes', '1.0', 'end', True)
        pattern = "'([A-Za-z0-9_\./\\-]*)'"
        self.highlight_pattern(pad, pattern, 'quotes', '1.0', 'end', True)

    def highlight_pattern(self, pad, pattern,
                          tag, start="1.0", end="end", regexp=False):
        """
        searches for pattern to highlight on basis of tag
        """
        start = pad.index(start)
        end = pad.index(end)
        pad.mark_set("matchStart", start)
        pad.mark_set("matchEnd", start)
        pad.mark_set("searchLimit", end)

        count = GUI.IntVar()
        while True:
            index = pad.search(pattern, "matchEnd", "searchLimit", count=count,
                               regexp=regexp)
            if index == "":
                break
            pad.mark_set("matchStart", index)
            pad.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            pad.tag_add(tag, "matchStart", "matchEnd")

    def indentation(self, pad, linepad, lang='c++', *args):

        """
        produces auto indentation for code
        python took some imagination ;)
        """
        pad.edit_separator()
        if lang == 'c++':
            curr = pad.get('1.0', GUI.INSERT)
            till_end = pad.get('1.0', GUI.END)
            indent = max(curr.count("{") - curr.count('}'), 0)
            diff = till_end.count('{') - till_end.count('}')
            pad.insert(GUI.INSERT, '    ' * indent)
            cordinate = map(int, pad.index(GUI.INSERT).split('.'))
            if diff > 0:
                pad.insert(GUI.INSERT, '\n' + ' ' * 4 * max(indent - 1, 0) + '}')
                pad.mark_set(GUI.INSERT, '%d.%d' % (cordinate[0], cordinate[1]))
        if lang == 'py':
            coordinates1 = map(int, pad.index(GUI.INSERT).split('.'))
            if coordinates1[0] != 1:
                coordinates = str(coordinates1[0] - 1) + '.0'
                r = pad.get(coordinates, str(coordinates1[0] - 1) + '.1111')
                letters = list(str(r))
                cnt = 0
                # find indentation level
                for i in letters:
                    if i == ' ':
                        cnt += 1
                    else:
                        break
                cnt = cnt / 4
                # check if indentation increasing keywords present
                f = 0
                for i in keywords['py']['loops']:
                    if i in r:
                        f = 1
                        break

                if f:
                    pad.insert(GUI.INSERT, (' ' * (cnt + 1) * 4))
                else:
                    pad.insert(GUI.INSERT, (' ' * (cnt) * 4))
        self.linenumber(pad, linepad)

    def fast_backspace(self, pad, linepad, *args):
        """
        so that you dont have to press backspace 4 times to go back to
        outer indentaion level (esp for python)
        """
        coordinates1 = map(int, pad.index(GUI.INSERT).split('.'))
        coordinates = str(coordinates1[0]) + '.0'
        r = pad.get(coordinates, GUI.INSERT)
        if len(str(r)) % 4 == 0:
            return
        if len(set(list(r))) == 1 and r[0] == u' ':
            coordinates = str(coordinates1[0]) + '.' + str(max(0, coordinates1[1] - 3))
            pad.delete(coordinates, GUI.INSERT)
        self.linenumber(pad, linepad)

    def linenumber(self, pad, linepad):
        """
        keeps track of linenumber
        """
        linepad.config(state=GUI.NORMAL)
        coordinate_pad = map(int, pad.index(GUI.END).split('.'))
        linepad.delete('1.0', GUI.END)
        for i in range(coordinate_pad[0] - 1):
            linepad.insert(GUI.END, str(i + 1) + '.\n')
        linepad.config(state=GUI.DISABLED)


Display = codeDisplay()


class fileFileMenu(object):
    def Exit(self):
        """
        exits program
        :return:
        """
        exit(0)

    def Open(self, app, pad, linepad, lang='c++'):
        """
        opens a file and displays it in pad
        :return:
        """
        from tkFileDialog import askopenfilename
        open_file = askopenfilename(parent=app)
        if len(open_file) == 0:
            return
        pad.delete('1.0', GUI.END)
        pad.insert(GUI.END, open(open_file).read())
        Display.open_highlight(pad, lang)
        Display.linenumber(pad, linepad)
        x = open_file
        x = x.replace('/', '\\')
        File.filename(map(str, x.split('\\'))[-1])
        File.filepath(x)
        File.execpath(x.replace('cpp', 'exe'))
        app.title(File.name)

    def Save(self, app, pad):
        """
        saves the contents in pad to file
        to filename on window
        """
        data = pad.get('1.0', GUI.END)[:-1]
        try:
            f = open(File.path, 'w')
            f.write(data)
            f.close()
        except IOError:
            f = open('untitled.cpp', 'w')
            f.write(data)
            f.close()
            return -1

    def Save_As(self, app, pad):
        """
        saves the contents in pad to file
        to specified filename
        """
        from tkFileDialog import asksaveasfilename
        save_file = asksaveasfilename(parent=app)
        data = pad.get('1.0', GUI.END)[:-1]
        f = open(save_file, 'w')
        f.write(data)
        f.close()
        x = save_file
        x = x.replace('/', '\\')
        File.filename(map(str, x.split('\\'))[-1])
        File.filepath(x)
        app.title(File.name)

    def set_new_filedetails(self, name, path):
        """
        sets details of untitled when switching lang
        """
        File.filename(name)
        File.filepath(path)


cmd_file = fileFileMenu()


class editFileMenu(object):
    def undo(self, pad, linepad, lang='c++', *argv):
        """
        undo code
        """
        try:
            pad.edit_undo()
            Display.linenumber(pad, linepad)
            # Display.open_highlight(pad, lang)
        except GUI.TclError:
            pass

    def redo(self, pad, linepad, lang='c++', *argv):
        """
        redo code
        """
        try:
            pad.edit_redo()
            Display.linenumber(pad, linepad)
            Display.syntax_highlight(pad, lang)
        except GUI.TclError:
            pass

    """
    pending
    """

    def select_all(self):
        pass


edit = editFileMenu()


class runFilemenu(object):
    def compile(self, app, pad, outputpad, lang='c++', *args):
        """
        compiles c++ currently
        need MinGw in C drive to work
        """
        frame2 = args[0]
        Display.show_outputpad(frame2, outputpad)
        if lang == 'c++':
            global FLAG
            FLAG = 0

            # remove the old exe and replace it with current one
            try:
                os.remove('a.exe')
            except WindowsError:
                pass
            # Save_As file automatically before compiling
            x = cmd_file.Save(app, pad)

            if x == -1:
                p = subprocess.Popen(
                    [
                        "C:\\Program Files (x86)\\MinGW\\bin\\g++.exe",
                        '-std=c++14',
                        'untitled.cpp'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            else:
                p = subprocess.Popen(
                    [
                        "C:\\Program Files (x86)\\MinGW\\bin\\g++.exe",
                        '-std=c++14',
                        File.path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            status = p.communicate()[1]
            outputpad.config(state=GUI.NORMAL)
            outputpad.delete('1.0', GUI.END)
            if len(status) == 0:
                outputpad.insert(GUI.END, 'compiled successfully \n')
            else:
                outputpad.insert(GUI.END, status + '\n')
                p.terminate()
                return -1
            p.terminate()
            outputpad.config(state=GUI.DISABLED)
        if lang == 'py':
            outputpad.config(state=GUI.NORMAL)
            outputpad.delete('1.0', 'end')
            outputpad.insert(GUI.INSERT, 'Python programs are interpreted. Press run instead')

    def run(self, app, pad, outputpad, inputpad, lang='c++', *args):
        """
        runs python and c++ program
        need python installed
        c++ details in compile
        """
        frame2 = args[0]
        Display.show_outputpad(frame2, outputpad)

        if lang == 'c++':
            outputpad.config(state=GUI.NORMAL)
            outputpad.delete('1.0', GUI.END)
            if FLAG:
                x = self.compile(app, pad, outputpad)
                # compilation failed, terminate
                if x == -1:
                    outputpad.insert(GUI.END, 'Compilation Failed.. Press Compile to get details')
            if not os.path.exists('a.exe'):
                outputpad.delete('1.0', GUI.END)
                outputpad.insert(GUI.END, 'Compilation Failed.. Press Compile to get details')
                return
            r = inputpad.get('1.0', GUI.END)
            f = open('input.txt', 'w')
            f.write(r)
            f.close()
            os.system('a.exe<input.txt >output.txt')
            r = open('output.txt').read()
            outputpad.delete('1.0', GUI.END)
            outputpad.insert(GUI.END, r)
            outputpad.config(state=GUI.DISABLED)

        if lang == 'py':
            cmd_file.Save(app, pad)
            r = inputpad.get('1.0', GUI.END)
            f = open('input.txt', 'w')
            f.write(r)
            f.close()
            outputpad.config(state=GUI.NORMAL)
            f = open('error.txt', 'w')
            status = subprocess.call('python ' + File.path + '<input.txt >output.txt', shell=True,
                                     stderr=f)
            outputpad.config(state=GUI.NORMAL)
            outputpad.delete('1.0', GUI.END)
            outputpad.insert(GUI.END, lang + '\n')
            if status == 0:
                r = open('output.txt').read()
                outputpad.delete('1.0', GUI.END)
                outputpad.insert(GUI.END, r)
                outputpad.config(state=GUI.DISABLED)
            else:
                r = open('error.txt').read()
                outputpad.delete('1.0', GUI.END)
                outputpad.insert(GUI.END, r)
                outputpad.config(state=GUI.DISABLED)
            outputpad.config(state=GUI.DISABLED)


run = runFilemenu()
