#!/usr/bin/python
from Tkinter import *

import tkFileDialog
import tkMessageBox
import os
import re
import svn
import config

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
            if depth == 0 and dir != ".svn":
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

    def additem(self, items, index=0, depth=0):
        for it in items:
            self.box.insert(index, depth * " " + it)
            index = index + 1
    def delitem(self, start=0, end=END):
        self.box.delete(start, end)
    
    def register_cb(self, func):
        self.cb_func = func
class AddProjDialog(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Add Project')
        scr_wid = self.winfo_screenwidth()
        scr_hei = self.winfo_screenheight()
        self.win_wid = scr_wid * 0.3
        self.win_hei = scr_hei * 0.3
        win_skx = (scr_wid - self.win_wid) / 2.0
        win_sky = (scr_hei - self.win_hei) / 2.0
        reso = "%sx%s+%s+%s" % \
            (str(int(self.win_wid)), str(int(self.win_hei)),
             str(int(win_skx)), str(int(win_sky)))
        self.geometry(reso)
        self.resizable(False, False)
        self.btnfrm = Frame(self)
        self.btnfrm.pack(side=BOTTOM, fill="x")
        self.canbtn = Button(master=self.btnfrm, text=" Cancel ", command=self.destroy)
        self.prebtn = Button(master=self.btnfrm, text="Previous", command=self.prepage)
        self.nxtbtn = Button(master=self.btnfrm, text="  Next  ", command=self.nextpage)
        self.canbtn.pack(side=RIGHT)
        self.nxtbtn.pack(side=RIGHT)
        self.prebtn.pack(side=RIGHT)
        self.labelfrm = Frame(self)
        self.labelfrm.pack(side=BOTTOM, fill="x")
        self.projurl = StringVar(self)
        self.projpath = StringVar(self)
        self.projname = StringVar(self)
        self.listwidget = []
        self.projinfo = {}
        self.index = 1
        self.pages = [self.secondpage, self.firstpage]
        self.pages[self.index]()

    def nextpage(self):
        if self.index == 1: 
            path = self.projpath.get()
            url = self.projurl.get()
            name = self.projname.get()
            if config.Config().has_proj(name):
                self.listwidget.append(Label(master=self.labelfrm, text="Project %s already exist!" % name, fg="red"))
                self.listwidget[-1].pack(side=RIGHT)
                return

            if self.var.get() == 2:
                if not os.path.isdir(path):
                    self.listwidget.append(Label(master=self.labelfrm, text="Invalid path!", fg="red"))
                    self.listwidget[-1].pack(side=RIGHT)
                    return
                svn_info = svn.SVN(path)
                url = svn_info.get_repository()
                if not url:
                    self.listwidget.append(Label(master=self.labelfrm, text="Invalid repository!", fg="red"))
                    self.listwidget[-1].pack(side=RIGHT)
                    return
            else:
                if not re.match(r'^https?:/{2}\w.+$', url):
                    self.listwidget.append(Label(master=self.labelfrm, text="Invalid url!", fg="red"))
                    self.listwidget[-1].pack(side=RIGHT)
                    return
                else:
                    svn_info = svn.SVN(path)
                    svn_info.set_repository(url)
                    svn_info.checkout()
            self.projinfo["name"] = self.projname.get()
            self.projinfo["path"] = path
            self.destroy()
        else:
            self.pages[self.index]()
    
    def prepage(self):
        self.pages[self.index]()

    def firstpage(self):
        self.clear()
        self.var = IntVar(self)
        self.var.set(1)
        self.listwidget.append(Radiobutton(master=self, font=25, text="Use new working copy directory", variable=self.var, value=1))
        self.listwidget[-1].pack(anchor = W)
        
        self.listwidget.append(Radiobutton(master=self, font=25, text="Use existing working copy directory", variable=self.var, value=2))
        self.listwidget[-1].pack(anchor = W)
        self.index = 0
        self.prebtn.config(state=DISABLED)

    def secondpage(self):
        self.clear()
        projframe = Frame(self)
        projframe.pack(fill="x")
        self.listwidget.append(projframe)
        Label(projframe, text='ProjectName:', font=25, width=20, anchor=E).pack(side=LEFT)
        Entry(projframe, textvariable=self.projname, width=30).pack(side=LEFT)

        wcframe = Frame(self)
        wcframe.pack(fill='x')
        self.listwidget.append(wcframe)
        Label(wcframe, text='Workingcopy Path:', font=25, width=20, anchor=E).pack(side=LEFT)
        Entry(wcframe, textvariable=self.projpath, width=30).pack(side=LEFT)
        Button(wcframe, text = "Select Directory", command = self.selectPath).pack(side=LEFT)

        urlframe = Frame(self)
        urlframe.pack(fill='x')
        self.listwidget.append(urlframe)
        Label(urlframe, text='Subversion URL:', font=25, width=20, anchor=E).pack(side=LEFT)
        entry = Entry(urlframe, textvariable=self.projurl, width=30)
        entry.pack(side=LEFT)
        
        if self.var.get() == 2:
            entry.config(state=DISABLED)
            
        self.index = 1
        self.prebtn.config(state=NORMAL)

    def clear(self):
        for widget in self.listwidget:
            widget.destroy()
        del self.listwidget[:]

    def selectPath(self):
        self.projpath.set(tkFileDialog.askdirectory())
        self.wm_attributes('-topmost',1)

class MarkFrame(MainFrame):
    def __init__(self, bor=0):
        MainFrame.__init__(self, bor=bor)
        self.box.place(relwidth=1.0, relheight=0.96)
        self.dirtree = {}
        self.dirlist = []
        self.addbtn = Button(self, text='Add Project', command=self.addproj)
        self.addbtn.place(relwidth=1.0, relheight=0.04, rely=0.96)
        self.config = config.Config()
        self.restore()
        self.hasDialog = False

    def restore(self):
        tmp = sorted(self.config.data.items(), key = lambda v: v[1]["index"])
        for it in tmp:
            self.dirtree[it[0]] = recur_path(it[1]["path"])
            self.dirlist.append([it[0]])
            self.additem(self.dirlist[-1], len(self.dirlist) - 1)
            self.box.bind('<Double-Button-1>', self.rollfolder)

    def addproj(self):
        info = self.get_proj_info()
        if not info:
            return
        del self.ProjDialog
        self.config.add_proj(info["name"], info["path"])
        self.dirtree[info["name"]] = recur_path(info["path"])
        self.dirlist.append([info["name"]])
        self.additem(self.dirlist[-1], len(self.dirlist) - 1)
        self.box.bind('<Double-Button-1>', self.rollfolder)
    
    def get_proj_info(self):
        if not self.hasDialog:
            self.ProjDialog = AddProjDialog()
            self.hasDialog = True
            self.wait_window(self.ProjDialog)
            self.hasDialog = False
            return self.ProjDialog.projinfo 
        else:
            self.ProjDialog.wm_attributes('-topmost',1)
            return None

    def rollfolder(self, event):
        self.index = self.box.curselection()[0]
        self.update_cb()

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
        self.box.place(relwidth=1.0, relheight=1.0)
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

app = MainWindow()
app.mainloop()