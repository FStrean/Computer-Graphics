from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)

import numpy as np


class Window(Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.points = None
        self.initUI()
        
 
    def initUI(self):
        self.master.title("Computer graphics")
        self.grid(sticky=N+S+E+W)
        
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)

        self.createPlot()
        self.createMenu()
        
    
    def createPlot(self):
        figure = Figure(figsize=(5, 5))
    
        self.canvas = FigureCanvasTkAgg(figure, self)
        self.plot = figure.add_subplot()
        
        NavigationToolbar2Tk(self.canvas, self).grid(row=0, column=0, columnspan=6, sticky=E+W+S+N, pady=5, padx=5)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky=E+W+S+N, pady=5, padx=5)
        
        
    def createMenu(self):
        canvas = Canvas(self)
        self.inputMenuContainer = Frame(canvas)
        hscrollbar = Scrollbar(self, orient=HORIZONTAL, command=canvas.xview)
        vscrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        
        canvas.configure(xscrollcommand=hscrollbar.set, yscrollcommand=vscrollbar.set)
        
        canvas.grid(row=1, column=3, columnspan=3, sticky=NSEW)
        hscrollbar.grid(row=2, column=3, columnspan=3, sticky=W+E)
        vscrollbar.grid(row=1, column=5, sticky=N+S+E)
        canvas.create_window((0, 0), window=self.inputMenuContainer, anchor="nw")
        
        canvas.bind_all("<MouseWheel>", lambda e : canvas.yview_scroll(-1 * int((e.delta / 120)), "units"))
        self.inputMenuContainer.bind("<Configure>", lambda e : canvas.configure(scrollregion=canvas.bbox(ALL)))
        
        self.pointNubmer = 0
        self.rows = list()
    
        self.addNewPoints(True)
        self.addNewPoints()
        self.addNewPoints()
        
        addNewPointsButton = Button(self, text="Add points", command=self.addNewPoints)
        deletePointsButton = Button(self, text="Delete selected points", command=self.deletePoints)
        buildPlotButton = Button(self, text="Build plot", command=self.onbuildPlot)
        
        addNewPointsButton.grid(row=3, column=3, columnspan=3, sticky=NSEW, pady=5, padx=5)
        deletePointsButton.grid(row=4, column=3, columnspan=3, sticky=NSEW, pady=5, padx=5)
        buildPlotButton.grid(row=2, column=0, columnspan=3, rowspan=3, sticky=NSEW, pady=5, padx=5)
        
        
        
    def addNewPoints(self, first=False):
        for _ in range(3 + first):       
            label1 = Label(self.inputMenuContainer, text="x")
            label1.grid(row=self.pointNubmer, column=0, sticky=E, pady=5, padx=5)
            entry1 = Entry(self.inputMenuContainer)
            entry1.grid(row=self.pointNubmer, column=1, sticky=EW, pady=5, padx=5)
                
            label2 = Label(self.inputMenuContainer, text="y")
            label2.grid(row=self.pointNubmer, column=2, sticky=E, pady=5, padx=5)
            entry2 = Entry(self.inputMenuContainer)
            entry2.grid(row=self.pointNubmer, column=3, sticky=EW, pady=5, padx=5)


            delete_checkbutton = Checkbutton(self.inputMenuContainer)
            delete_checkbutton.state(['!alternate'])
            delete_checkbutton.grid(row=self.pointNubmer, column=4, sticky=EW, pady=5, padx=5)
            row = [label1, entry1, label2, entry2, delete_checkbutton]
            self.rows.append(row)           
            
            self.pointNubmer += 1
    
    
    def deletePoints(self):
        rows = []
        for row in self.rows:
            if row[4].instate(['selected']):
                rows.append(row)       
        if(((len(rows) % 3) == 0) & ((self.pointNubmer - len(rows)) >= 10)):
            for row in rows:
                row_number = row[0].grid_info()["row"]
                for column in row:
                   column.destroy()   
                del self.rows[row_number]
                for row_ in self.rows[row_number:]:
                    for column in row_:
                         grinfo = column.grid_info()
                         column.grid(row=grinfo["row"] - 1, column=grinfo["column"], sticky=grinfo["sticky"], pady=grinfo["pady"], padx=grinfo["padx"])
                self.pointNubmer -= 1
    
    
    def onbuildPlot(self):
        self.plot.clear()
        self.buildPlot()
        self.canvas.draw()
        self.canvas.flush_events()
    
    
    def buildPlot(self): 
        self.points=list()
        try:
            for row in self.rows:
                self.points.append([float(row[1].get()), float(row[3].get())])
        except:
            return
        self.points = np.array(self.points)
        self.drawCompoisiteBezierCurveAndPolylineWithPoints(self.points.tolist())
        
        
    def drawCompoisiteBezierCurveAndPolylineWithPoints(self, input_points, color="blue"):
        points = []
        for i in range(0, len(input_points), 3):
            if(i == len(input_points) - 1):
                break
            intermediate_point = []
            for j in range(i, i + 4):
                intermediate_point.append(input_points[j])
            points.append(intermediate_point)
        
        points = np.array(points)
        curve = buildCompositeBezierCurveWithPoints(points)
        for part in curve:  
            self.plot.plot(part[:, 0], part[:, 1], color=color)
        self.plot.plot(self.points[:, 0], self.points[:, 1], 'o:', color=color)
       
        
 
def decimal_range(start, stop, increment):
    while start < stop:
        yield start
        start += increment


def buildCompositeBezierCurveWithPoints(points):
    def B(coorArr, i, j, t):
        if j == 0:
            return coorArr[i]
        return (B(coorArr, i, j - 1, t)*(1 - t) 
            + B(coorArr, i + 1, j - 1, t)*t)
        
    result = []
    for k in range(0, points.shape[0]):
        coordinates = []
        for i in range(points[k, 0].shape[0]):
            intermediate_point = []
            for coordinate in points[k]:
                intermediate_point.append(coordinate[i])
            coordinates.append(intermediate_point)

        n = len(coordinates[0])
        
        intermediate = []
        for t in np.linspace (0., 1., 25):
            intermediate_line = []
            for coord in coordinates:
                intermediate_line.append(B(coord, 0, n - 1, t))
            intermediate.append(intermediate_line)
        result.append(intermediate)
    return np.array(result)


    
def main():
    root = Tk()
    app = Window(root)
    root.mainloop()
    
    
    
if __name__ == '__main__':
    main()