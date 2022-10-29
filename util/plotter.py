import tkinter

class Plotter():

    def __init__(self):
        self.master = tkinter.Tk()
        self.width, self.height = 1000, 250
        self.margin = 20
        self.w = tkinter.Canvas(self.master, width=self.width + self.margin*2, height=self.height + self.margin*2)
        self.w.pack()
        self.w.create_rectangle(self.margin - 1, self.margin - 1, self.width + self.margin + 1, self.height + self.margin + 1)

    def plot(self, bp_f, color="red"):
        points = [(i + self.margin, ((1.0 - bp_f(float(i) / self.width)) * self.height) + self.margin) for i in range(int(self.width))]
        self.w.create_line(points, fill=color, width=2.0)

    def show_plots(self):
        self.master.update()

plotter = None

def plot(signal, color="red"):
    global plotter
    if plotter is None:
        plotter = Plotter()
    plotter.plot(signal, color)

def show_plots():
    plotter.show_plots()
