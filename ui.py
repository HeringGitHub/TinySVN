#!/usr/bin/python

from Tkinter import *

import tkMessageBox

def hello():
    print "hello"

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

class MainFrame(Frame):
    def __init__(self, bor=0):
        Frame.__init__(self, borderwidth=bor, background="GRAY")
        self.dirtree = {}
        self.__createWidgets__()

    def __createWidgets__(self):
        self.libo = Listbox(self, font=10, selectmode="browse")
        self.libo.place(relwidth=1.0, relheight=1.0)

    def additem(self, items):
        for it in items:
            self.libo.insert(self.libo.size(), it)

    def delitem(self, name):
        pass

    def __unfold__(self):
        pass
    
    def __clear__(self):
        pass

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
        self.MarkBook = MainFrame(bor=1)
        self.MarkBook.place(x=0, relwidth=0.25, relheight=1.0, bordermode=INSIDE)
        self.DirDetail = MainFrame(bor=1)
        self.DirDetail.place(relx=0.25, relwidth=0.75, relheight=1.0, bordermode=INSIDE)

    def addproject(self, name):
        self.MarkBook.additem(name)


app = MainWindow()
app.addproject(["aa","bb"])
app.mainloop()