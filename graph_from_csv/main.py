from os.path import basename, splitext
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pylab as pl

class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)

class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)

        self.fileFrame = tk.LabelFrame(self, text="Soubor")
        self.fileFrame.pack(padx=5, pady=5)
        self.fileEntry = MyEntry(self.fileFrame)
        self.fileEntry.pack(anchor="w")
        self.fileBtn = tk.Button(self.fileFrame, text="...")
        self.fileBtn.pack(anchor="e")

        self.dataformatVar = tk.StringVar(value="RADEK")
        self.radkyRbtn = tk.Radiobutton(self.fileFrame, 
                                        text="Data jsou v řádcích",
                                        variable=self.dataformatVar,
                                        value="RADEK")
        self.radkyRbtn.pack(anchor="w")
        self.sloupceRbtn = tk.Radiobutton(self.fileFrame, 
                                          text="Data jsou ve sloupcích",
                                          variable=self.dataformatVar,
                                          value="SLOUPEC")
        self.sloupceRbtn.pack(anchor="w")

        self.grafFrame = tk.LabelFrame(self, text="Graf")
        self.grafFrame.pack(padx=5, pady=5)
        tk.Label(self.grafFrame, text="Titulek").grid(row=0, column=0)
        self.titleEntry = MyEntry(self.grafFrame)
        self.titleEntry.grid(row=0,column=1)
        tk.Label(self.grafFrame, text="Popisek X").grid(row=1, column=0)
        self.xlabelEntry = MyEntry(self.grafFrame)
        self.xlabelEntry.grid(row=1,column=1)
        tk.Label(self.grafFrame, text="Popisek Y").grid(row=2, column=0)
        self.ylabelEntry = MyEntry(self.grafFrame)
        self.ylabelEntry.grid(row=2,column=1)

        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack()

    def about(self):
        window = About(self)
        window.grab_set()

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()