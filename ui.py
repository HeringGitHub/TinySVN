#!/usr/bin/python

from Tkinter import *

import tkMessageBox
import os

# def hello():
#     print "hello"

# class MainMenu():
#     def __init__(self, master):
#         mainmenu = Menu(master)
#         first = Menu(mainmenu, tearoff=0)
#         first.add_command(label="pre", command=hello)
#         first.add_command(label="next", command=hello)
#         mainmenu.add_cascade(label="dir", menu=first)
#         second = Menu(mainmenu, tearoff=0)
#         second.add_command(label="about", command=hello)
#         second.add_command(label="help", command=hello)
#         mainmenu.add_cascade(label="help", menu=second)
#         master.config(menu=mainmenu)
def recur_path(path, depth=0):
    tree = {}
    tree["path"] = path
    tree["depth"] = depth
    tree["closed"] = True
    tree["list"] = []
    tree["child"] = {}
    if os.path.isdir(path):
        _, dirs, files = os.walk(path).next()
        for dir in dirs:
            tree["child"][dir] = recur_path(path + "/" + dir, depth + 1)
        for file in files:
            tree["child"][file] = recur_path(path + "/" + file, depth + 1)
    return tree

def classify(filenames):
    names = list(sorted(filenames))
    count = len(names)
    i = 0
    while i < count:
        if os.path.isfile(filenames[names[i]]["path"]):
            names.append(names[i])
            del names[i]
            count = count - 1
        else:
            i = i + 1
    return names

class MainFrame(Frame):
    def __init__(self, bor=0):
        Frame.__init__(self, borderwidth=bor)
        self.dirtree = {}
        self.__createWidgets__()

    def __createWidgets__(self):
        self.box = Listbox(self, font=15, selectmode="browse")
        self.box.place(relwidth=1.0, relheight=1.0)

    def additem(self, items, index=0, depth=0):
        for it in items:
            self.box.insert(index, depth * " " + it)
            index = index + 1
    def delitem(self, start=0, end=END):
        self.box.delete(start, end)
    
    def register_cb(self, func):
        self.cb_func = func

class MarkFrame(MainFrame):
    def __init__(self, bor=0):
        MainFrame.__init__(self, bor=bor)
        self.dirtree = {}
        self.dirlist = []

    def rollfolder(self, event):
        self.index = self.box.curselection()[0]
        self.update_cb()

    def addproj(self, name, path):
        self.dirtree[name] = recur_path(path)
        self.dirlist.append([name])
        self.additem(self.dirlist[-1])
        self.box.bind('<Double-Button-1>', self.rollfolder)

    def delproj(self, name):
        pass
    
    def update_cb(self, index=-1):
        childlist = self.dirlist[self.index + index + 1]
        dt = self.dirtree
        info = {}
        for c in childlist:
            info = dt[c]
            dt = info["child"]
        
        idx = self.index + index + 1 + 1
        if info["list"]:
            for c in info["list"]:
                self.dirlist.insert(idx, c)
                self.additem([c[-1]], idx, 2 * (len(c) - 1))
                idx = idx + 1
            info["closed"] = False
            del info["list"][:]

        elif info["child"]:
            names = classify(info["child"])
            if info["closed"]:
                tmpidx = idx
                for name in names:
                    tmplist = list(childlist)
                    tmplist.append(name)
                    self.dirlist.insert(tmpidx, tmplist)
                    tmpidx = tmpidx + 1
                self.additem(names, idx, 2 * (info["depth"] + 1))
                info["closed"] = False
            else:
                while idx < len(self.dirlist) and len(self.dirlist[idx]) > len(childlist):
                    info["list"].append(self.dirlist[idx])
                    del self.dirlist[idx]
                self.delitem(idx, idx + len(info["list"]) - 1)
                info["closed"] = True
        if info["child"] and index == -1:
            self.cb_func(info["child"])

class DirListFrame(MainFrame):
    def __init__(self, bor=0):
        MainFrame.__init__(self, bor=bor)
        self.box.bind('<Double-Button-1>', self.rollfolder)
        self.dirtree = {}
        self.dirlist = []

    def update_cb(self, items):
        self.delitem()
        self.dirtree = items
        self.dirlist = classify(items)
        self.additem(self.dirlist)

    def rollfolder(self, event):
        index = self.box.curselection()[0]
        child = self.dirtree[self.dirlist[index]]["child"]
        if child:
            self.update_cb(child)
            self.cb_func(index)
class MainWindow(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.title("TinySVN")
        scr_wid = self.winfo_screenwidth()
        scr_hei = self.winfo_screenheight()
        self.win_wid = scr_wid * 0.7
        self.win_hei = scr_hei * 0.7
        win_skx = (scr_wid - self.win_wid) / 2.0
        win_sky = (scr_hei - self.win_hei) / 2.0
        reso = "%sx%s+%s+%s" % \
            (str(int(self.win_wid)), str(int(self.win_hei)), str(int(win_skx)), str(int(win_sky)))
        self.geometry(reso)
        self.resizable(True, True)
        self.createWidgets()

    def createWidgets(self):
        # self.Menu = MainMenu(self)
        self.MarkBook = MarkFrame(bor=1)
        self.MarkBook.place(x=0, relwidth=0.25, relheight=1.0, bordermode=INSIDE)
        self.DirDetail = DirListFrame(bor=1)
        self.DirDetail.place(relx=0.25, relwidth=0.75, relheight=1.0, bordermode=INSIDE)
        self.MarkBook.register_cb(self.DirDetail.update_cb)
        self.DirDetail.register_cb(self.MarkBook.update_cb)
    def addproj(self, name, path):
        self.MarkBook.addproj(name, path)


app = MainWindow()
app.addproj("avx", "/home/hering/WorkSpace/SVN/trunk")
app.mainloop()