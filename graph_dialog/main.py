from os.path import basename, splitext
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pylab as pl

class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = 'Foo'

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.btn = tk.Button(self, text='...', command=self.open_filedialog)
        self.btn.pack()
        self.btn = tk.Button(self, text='Kreslit', command=self.plot_file)
        self.btn.pack()
        self.btn = tk.Button(self, text='Quit', command=self.quit)
        self.btn.pack()

    def open_filedialog(self):
        self.file = filedialog.askopenfilename(title='Vyber soubor',initialdir='/home/mac39195@spseol.cz/wnet_H/Python/graph_dialog')

    def plot_file(self):
        try:
            data = {}
            with open(f"{self.file}", 'r') as f:
                for line in f.readlines():
                    x, y = line.split()
                    data[float(x)] = float(y)
            pl.plot(data.keys(), data.values())
            pl.grid()
            pl.show()
        except AttributeError:
            messagebox.showwarning("More čo robiš", "Není vybrán ždný soubor")
        except:
            messagebox.showwarning("More čo robiš", "Vybraný soubor není .txt")

    def quit(self, event=None):
        super().quit()

app = Application()
app.mainloop()