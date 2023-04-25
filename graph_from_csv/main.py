from os.path import basename, splitext
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt 

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

class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Graf"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)

        self.fileFrame = tk.LabelFrame(self, text="Soubor")
        self.fileFrame.pack(padx=5, pady=5)
        self.fileEntry = MyEntry(self.fileFrame)
        self.fileEntry.pack(anchor="w")
        self.fileBtn = tk.Button(self.fileFrame, text="...", command=self.selectFile)
        self.fileBtn.pack(anchor="e")
        self.dataformatVar = tk.StringVar(value="RADEK")
        self.rowsRbtn = tk.Radiobutton(self.fileFrame, 
                                        text="Data jsou v řádcích",
                                        variable=self.dataformatVar,
                                        value="RADEK")
        self.rowsRbtn.pack(anchor="w")
        self.columnsRbtn = tk.Radiobutton(self.fileFrame, 
                                          text="Data jsou ve sloupcích",
                                          variable=self.dataformatVar,
                                          value="SLOUPEC")
        self.columnsRbtn.pack(anchor="w")
        self.splitterLabel = tk.Label(self.fileFrame, text="Data jsou rozděleny pomocí:")
        self.splitterLabel.pack(anchor="w")
        self.splitterVar = tk.StringVar(value=";")
        self.splitterEntry = MyEntry(self.fileFrame, textvariable=self.splitterVar)
        self.splitterEntry.pack()

        self.grafFrame = tk.LabelFrame(self, text="Parametry grafu")
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
        tk.Label(self.grafFrame, text="Mřížka").grid(row=3, column=0)
        self.gridVar = tk.BooleanVar(value=0)
        self.gridCheck = tk.Checkbutton(self.grafFrame, variable=self.gridVar)
        self.gridCheck.grid(row=3, column=1, sticky="w")

        self.styleFrame = tk.LabelFrame(self, text="Styl")
        self.styleFrame.pack(padx=5, pady=5)
        self.colors = ("Black","Green", "Red",
                       "Blue", "Purple", "Pink", 
                       "Yellow", "Grey", "Orange")
        self.lines = ('None', '-', ':', '--', '-.')
        self.markers = ",.oxX+-PD123<>v"
        self.lineVar = tk.StringVar(value='-')
        self.markerVar = tk.StringVar(value=",")
        self.lineColorVar = tk.StringVar(value="Black")
        self.markerColorVar = tk.StringVar(value="Black")
        tk.Label(self.styleFrame, text="Čára").grid(row=0, column=0)
        self.lineOption = tk.OptionMenu(self.styleFrame, 
                                        self.lineVar, 
                                        *self.lines)
        self.lineOption.grid(row=0, column=1, sticky="w")
        tk.Label(self.styleFrame, text="Marker").grid(row=1, column=0)
        self.markerOption = tk.OptionMenu(self.styleFrame, 
                                          self.markerVar, 
                                          *self.markers)
        self.markerOption.grid(row=1, column=1, sticky="w")
        self.markerOption = tk.OptionMenu(self.styleFrame, 
                                          self.lineColorVar, 
                                          *self.colors)
        self.markerOption.grid(row=0, column=2, sticky="w")
        self.markerOption = tk.OptionMenu(self.styleFrame, 
                                          self.markerColorVar, 
                                          *self.colors)
        self.markerOption.grid(row=1, column=2, sticky="w")
        tk.Button(self, text="Kreslit", command=self.plotGraph).pack()
        tk.Button(self, text="Quit", command=self.quit).pack()


    def selectFile(self):
        self.file = filedialog.askopenfilename(title='Vyber soubor')
        self.fileEntry.value = self.file

    def plotGraph(self):
        with open(self.file) as f:
            if self.dataformatVar.get() == "RADEK":
                x = f.readline().split(self.splitterVar.get())
                y = f.readline().split(self.splitterVar.get())
                try:
                    x = [float(x_point) for x_point in x]
                    y = [float(y_point) for y_point in y]
                except:
                    x = [float(x_point.replace(",", ".")) for x_point in x]
                    y = [float(y_point.replace(",", ".")) for y_point in y]
            elif self.dataformatVar.get() == "SLOUPEC":
                x, y = [], []
                for line in f:
                    point = line.split(self.splitterVar.get())
                    x_point, y_point = point[0], point[1][:-1]
                    print(point)
                    print(x_point, y_point)
                    try:
                        x_point = float(x_point)
                        y_point = float(y_point)
                    except:
                        x_point = float(x_point.replace(",", "."))
                        y_point = float(y_point.replace(",", "."))
                    x.append(x_point)
                    y.append(y_point)
            plt.plot(x, y,
                     linestyle=self.lineVar.get(),
                     marker=self.markerVar.get(),
                     color=self.lineColorVar.get(),
                     mec=self.markerColorVar.get(),
                     mfc=self.markerColorVar.get()) 
            plt.xlabel(self.xlabelEntry.value)
            plt.ylabel(self.ylabelEntry.value)
            plt.title(self.titleEntry.value)
            plt.grid(self.gridVar.get())
            plt.show()

    def quit(self, event=None):
        super().quit()

app = Application()
app.mainloop()