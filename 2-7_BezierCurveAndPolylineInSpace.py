from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


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
        self.columnconfigure(5, weight=0)
        
        self.rowconfigure(1, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=0)
        self.rowconfigure(6, weight=0)

        self.createPlot()
        self.createMenu()
        
    
    def createPlot(self):
        figure = Figure(figsize=(5, 5))
    
        self.canvas = FigureCanvasTkAgg(figure, self)
        self.plot = figure.add_subplot(projection="3d")
        
        NavigationToolbar2Tk(self.canvas, self).grid(row=0, column=0, columnspan=6, sticky=E+W+S+N, pady=5, padx=5)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=6, sticky=E+W+S+N, pady=5, padx=5)
        
        
    def createMenu(self):
        canvas = Canvas(self)
        self.inputMenuContainer = Frame(canvas)
        hscrollbar = Scrollbar(self, orient=HORIZONTAL, command=canvas.xview)
        vscrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        
        canvas.configure(xscrollcommand=hscrollbar.set, yscrollcommand=vscrollbar.set)
        
        canvas.grid(row=2, column=0, columnspan=6, sticky=NSEW)
        hscrollbar.grid(row=3, column=0, columnspan=6, sticky=W+E)
        vscrollbar.grid(row=2, column=5, sticky=N+S + E)
        canvas.create_window((0, 0), window=self.inputMenuContainer, anchor="nw")
        
        canvas.bind_all("<MouseWheel>", lambda e : canvas.yview_scroll(-1 * int((e.delta / 120)), "units"))
        self.inputMenuContainer.bind("<Configure>", lambda e : canvas.configure(scrollregion=canvas.bbox(ALL)))
        
        self.pointNubmer = 0
        self.rows = list()
    
        while self.pointNubmer < 5:
            self.addNewPoint()
        
        rotateRelativeToXOrYButton = Button(self, text="Rotate", command=self.rotatePlot)
        label1 = Label(self, text="curve relative to ")
        self.comboBox = Combobox(self, values=["X", "Y"])
        label2 = Label(self, text="on")
        self.entry = Entry(self)
        label3 = Label(self, text="degrees")
        
        rotateRelativeToXOrYButton.grid(row=4, column=0, sticky=NSEW, pady=5, padx=5)
        label1.grid(row=4, column=1, sticky=E, pady=5, padx=5)
        self.comboBox.grid(row=4, column=2, sticky=NSEW, pady=5, padx=5)
        label2.grid(row=4, column=3, sticky=E, pady=5, padx=5)
        self.entry.grid(row=4, column=4, sticky=EW, pady=5, padx=5)
        label3.grid(row=4, column=5, sticky=E, pady=5, padx=5)
        
        
        addNewPointButton = Button(self, text="Add point", command=self.addNewPoint)
        buildPlotButton = Button(self, text="Build plot", command=self.onbuildPlot)
        
        addNewPointButton.grid(row=5, columnspan=6, sticky=NSEW, pady=5, padx=5)
        buildPlotButton.grid(row=6, columnspan=6, sticky=NSEW, pady=5, padx=5)
    
    def addNewPoint(self):         
        label1 = Label(self.inputMenuContainer, text="x")
        label1.grid(row=self.pointNubmer, column=0, sticky=E, pady=5, padx=5)
        entry1 = Entry(self.inputMenuContainer)
        entry1.grid(row=self.pointNubmer, column=1, sticky=EW, pady=5, padx=5)
            
        label2 = Label(self.inputMenuContainer, text="y")
        label2.grid(row=self.pointNubmer, column=2, sticky=E, pady=5, padx=5)
        entry2 = Entry(self.inputMenuContainer)
        entry2.grid(row=self.pointNubmer, column=3, sticky=EW, pady=5, padx=5)
            
        label3 = Label(self.inputMenuContainer, text="z")
        label3.grid(row=self.pointNubmer, column=4, sticky=E, pady=5, padx=5)
        entry3 = Entry(self.inputMenuContainer)
        entry3.grid(row=self.pointNubmer, column=5, sticky=EW, pady=5, padx=5)
        
        delete_button = Button(self.inputMenuContainer, text="Delete")
        delete_button.grid(row=self.pointNubmer, column=6, sticky=EW, pady=5, padx=5)
        
        row = [label1, entry1, label2, entry2, label3, entry3, delete_button]
        self.rows.append(row)
                
        delete_button.configure(command=lambda : self.deletePoint(row))
        
        self.pointNubmer += 1
    
    
    def deletePoint(self, row):
        if(self.pointNubmer > 5):
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
                self.points.append([float(row[1].get()), float(row[3].get()), float(row[5].get())])
        except:
            return
        self.points = np.matrix(self.points)
        self.drawBezierCurveAndPolylineWithPoints(self.points)
        
        
    def drawBezierCurveAndPolylineWithPoints(self, points, color="blue"):
        curve = buildBezierCurveWithPoints(points.getA())  
        self.plot.plot(curve[:, 0], curve[:, 1], curve[:, 2], color=color)
        self.plot.plot(points.getA()[:, 0], points.getA()[:, 1], points.getA()[:, 2], 'o:', color=color)
       
        
    def rotatePlot(self):
        try:
            angle = float(self.entry.get()) * np.pi / 180
        except:
            return
        rotate = None
        
        if(self.points is None):
            self.buildPlot()
        
        maximum_z = np.amax(np.sum((self.points - 
                                    np.c_[np.zeros((np.shape(self.points)[0], 2), dtype=float), 
                                          self.points[:, 2]]).getA()**2, axis=1)**(1/2))
        
        set_lim_func = None

        if(self.comboBox.get() == "X"):
            maximum_y = np.amax(np.sum((self.points - 
                                        np.c_[np.c_[np.zeros((np.shape(self.points)[0], 1), dtype=float), 
                                                    self.points[:, 1]], 
                                              np.zeros((np.shape(self.points)[0], 1), dtype=float)]).getA()**2, axis=1)**(1/2))
            max_value = max(maximum_z, maximum_y)
            rotate = rotateRelativeToX
            set_lim_func = lambda: self.plot.set(ylim=(-max_value, max_value), zlim=(-max_value, max_value))
        elif(self.comboBox.get() == "Y"):
            maximum_x = np.amax(np.sum((self.points - 
                                        np.c_[self.points[:, 0], 
                                        np.zeros((np.shape(self.points)[0], 2), dtype=float)]).getA()**2, axis=1)**(1/2))
            max_value = max(maximum_z, maximum_x)
            rotate = rotateRelativeToY
            set_lim_func = lambda: self.plot.set(xlim=(-max_value, max_value), zlim=(-max_value, max_value))
        else: 
            return
        
        oldPoints = self.points.copy()

        for _ in decimal_range(0, angle, angle / 30):
            self.points = rotate(angle / 30, self.points)
            
            for i in range(np.shape(self.points)[0]):
                self.rows[i][1].delete(0,END)
                self.rows[i][1].insert(0,float(self.points[i, 0]))
                
                self.rows[i][3].delete(0,END)
                self.rows[i][3].insert(0,float(self.points[i, 1]))
                
                self.rows[i][5].delete(0,END)
                self.rows[i][5].insert(0,float(self.points[i, 2]))
                
            self.plot.clear()
            set_lim_func()
            self.buildPlot()
            self.drawBezierCurveAndPolylineWithPoints(oldPoints, color="red")
            self.canvas.draw()
            self.canvas.flush_events()
            plt.pause(0.001)
        
 
def decimal_range(start, stop, increment):
    while start < stop:
        yield start
        start += increment


def buildBezierCurveWithPoints(points):
    t_values = np.arange(0, 1, 0.01)
    
    def TwoPoints(t, P1, P2):
        Q1 = (1 - t) * P1 + t * P2
        return Q1

    def Points(t, points):
        newpoints = []
        for i1 in range(0, len(points) - 1):
            newpoints += [TwoPoints(t, points[i1], points[i1 + 1])]
        return newpoints

    def Point(t, points):
        newpoints = points
        while len(newpoints) > 1:
            newpoints = Points(t, newpoints)
        return newpoints[0]
    
    curve = np.array([[0.0] * len(points[0])])
    for t in t_values:
        curve = np.append(curve, [Point(t, points)], axis=0)
    curve = np.delete(curve, 0, 0)
    return curve


def rotateRelativeToX(angle, points):
    rotateMatrix = np.matrix([[1, 0, 0],
                              [0, np.cos(angle), -np.sin(angle)],
                              [0, np.sin(angle), np.cos(angle)]])
    return points * rotateMatrix


def rotateRelativeToY(angle, points):
    rotateMatrix = np.matrix([[np.cos(angle), 0, np.sin(angle)],
                              [0, 1, 0],
                              [-np.sin(angle), 0, np.cos(angle)]])
    return points * rotateMatrix


    
def main():
    root = Tk()
    app = Window(root)
    root.mainloop()
    
    
    
if __name__ == '__main__':
    main()