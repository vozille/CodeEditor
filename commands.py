"""
The command list which brings life to the GUI :P
"""
#!usr/bin/Python2

import Tkinter as GUI
from ScrolledText import *
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
        return reduce(
            lambda a, b: a | b,
            [node.all_suffixes(prefix + char)
             for(char, node) in self.children.items()]) | results

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
    with open('cppkeywords.txt', 'r') as f:
        for i in f:
            i = i.strip('\n')
            words = map(str, i.split())
            key = words[0]
            words.pop(0)
            keywords[key] = list(words)
        f.close()

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

    def defaultWords(self, pad):
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
        self.defaultWords(pad)

    def addToTrie(self, pad, *args):
        pad.edit_separator()
        r = pad.get('1.0', GUI.END)
        r = map(str, r.split())
        if not MyDict.contains(r[-1]):
            MyDict.insert(self.remove_punc(r[-1]))

    def show_in_console(self, event, app2, pad, linepad):
        pad.edit_separator()
        global FLAG
        FLAG = 1
        self.syntax_highlight(pad)
        self.linenumber(pad, linepad)
        r = pad.get('1.0', GUI.INSERT)
        r = map(str, r.split())
        if len(r) != 0:
            x = MyDict.autocomplete(r[-1])
            lb = GUI.Listbox(app2, height=10, width=30)
            if len(x) and len(r):
                for i in x:
                    lb.insert(GUI.END, i + '\n')
            lb.grid(row=1, column=1)

            pad.tag_configure('num', foreground='#ff69b4')
            try:
                float(r[-1])
                self.highlight_pattern(pad, r[-1], 'num')
            except ValueError:
                pass

    def syntax_highlight(self, pad, pos=GUI.INSERT, flag=0):
        pad.edit_separator()
        pad.tag_configure('default', foreground='#e0115f')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')
        pad.tag_configure('normal', foreground='#f8f8f2')
        pad.tag_configure('quotes', foreground='gold')
        pad.tag_configure('A_datatypes', foreground='#228b22')
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
                self.highlight_pattern(pad, i, 'default', ncoordinates, pos)
            elif i in keywords['loops']:
                self.highlight_pattern(pad, i, 'loops', ncoordinates, pos)
            elif i in keywords['P_datatypes']:
                self.highlight_pattern(
                    pad, i, 'P_datatypes', ncoordinates, pos)
            elif i in keywords['A_datatypes']:
                self.highlight_pattern(
                    pad, i, 'A_datatypes', ncoordinates, pos)

        pattern = '"([A-Za-z0-9_\./\\-]*)"'
        self.highlight_pattern(pad, pattern, 'quotes', '1.0', 'end', True)

        pattern = "'([A-Za-z0-9_\./\\-]*)'"
        self.highlight_pattern(pad, pattern, 'quotes', '1.0', 'end', True)

    def open_highlight(self, pad, lang='c++'):

        pad.tag_configure('default', foreground='#e0115f')
        pad.tag_configure('loops', foreground='green')
        pad.tag_configure('P_datatypes', foreground='aqua')
        pad.tag_configure('quotes', foreground='gold')
        pad.tag_configure('A_datatypes', foreground='#228b22')
        for i in keywords:
            for j in keywords[i]:
                self.highlight_pattern(pad, j, i)

        pattern = '"([A-Za-z0-9_\./\\-]*)"'
        self.highlight_pattern(pad, pattern, 'quotes', '1.0', 'end', True)
        pattern = "'([A-Za-z0-9_\./\\-]*)'"
        self.highlight_pattern(pad, pattern, 'quotes', '1.0', 'end', True)

    def indentation(self, pad, linepad, *args):
        pad.edit_separator()
        curr = pad.get('1.0', GUI.INSERT)
        till_end = pad.get('1.0', GUI.END)
        indent = max(curr.count("{") - curr.count('}'), 0)
        diff = till_end.count('{') - till_end.count('}')
        pad.insert(GUI.INSERT, '    ' * indent)
        cordinate = map(int, pad.index(GUI.INSERT).split('.'))
        if diff > 0:
            pad.insert(GUI.INSERT, '\n' + '    ' * max(indent - 1, 0) + '}')
            pad.mark_set(GUI.INSERT, '%d.%d' % (cordinate[0], cordinate[1]))
        self.linenumber(pad, linepad)

    def highlight_pattern(
            self,
            pad,
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

        count = GUI.IntVar()
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

    def linenumber(self, pad, linepad):
        linepad.config(state=GUI.NORMAL)
        coordinate_pad = map(int, pad.index(GUI.END).split('.'))
        linepad.delete('1.0', GUI.END)
        for i in range(coordinate_pad[0] - 1):
            linepad.insert(GUI.END, str(i + 1) + '.\n')
        linepad.config(state=GUI.DISABLED)

Display = display_func()


class cmd_filemenu(object):

    def __init__(self):
        pass

    def Exit(self):
        exit(0)

    def Open(self, app, pad, linepad, lang='c++'):
        from tkFileDialog import askopenfilename
        open_file = askopenfilename(parent=app)
        if len(open_file) == 0:
            return
        pad.delete('1.0', GUI.END)
        pad.insert(GUI.END, open(open_file).read())
        Display.open_highlight(pad)
        Display.linenumber(pad, linepad)
        x = open_file
        x = x.replace('/', '\\')
        File.Filename(map(str, x.split('\\'))[-1])
        File.FilePath(x)
        File.Execpath(x.replace('cpp', 'exe'))
        app.title(File.name)

    def Save(self, app, pad):
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
        from tkFileDialog import asksaveasfilename
        save_file = asksaveasfilename(parent=app)
        data = pad.get('1.0', GUI.END)[:-1]
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

    def undo(self, pad, linepad, *argv):
        try:
            pad.edit_undo()
            Display.linenumber(pad, linepad)
            Display.open_highlight(pad)
        except GUI.TclError:
            pass

    def redo(self, pad, linepad, *argv):
        try:
            pad.edit_redo()
            Display.linenumber(pad, linepad)
            Display.open_highlight(pad)
        except GUI.TclError:
            pass

    def select_all(self):
        pass

edit = editFileMenu()


class runFilemenu(object):

    def __init__(self):
        pass

    def compile(self, app, pad, outputpad, lang='c++', *args):
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
        outputpad.delete('1.0', GUI.END)
        if len(status) == 0:
            outputpad.insert(GUI.END, 'compiled successfully \n')
        else:
            outputpad.insert(GUI.END, status + '\n')
            p.terminate()
            return -1
        p.terminate()
        outputpad.config(state=GUI.DISABLED)

    def run(self, app, pad, outputpad, inputpad, lang='c++', *args):
        if FLAG:
            x = self.compile(app, pad, outputpad)
            # compilation failed, terminate
            if x == -1:
                return
        outputpad.config(state=GUI.NORMAL)
        outputpad.delete('1.0', GUI.END)
        outputpad.insert(GUI.END, 'Running ...')
        r = inputpad.get('1.0', GUI.END)
        f = open('input.txt', 'w')
        f.write(r)
        f.close()
        os.system('a.exe<input.txt >output.txt')
        r = open('output.txt').read()
        outputpad.delete('1.0', GUI.END)
        outputpad.insert(GUI.END, r)
        outputpad.config(state=GUI.DISABLED)

run = runFilemenu()
