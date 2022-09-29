from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)
from matplotlib.patches import Polygon, Circle

import numpy as np


class Window(Frame):
    
    def __init__(self):
        super().__init__()
        self.shape = np.matrix([[3, 1], 
                  [6, 1], 
                  [3, 10]], dtype=float)
        self.initUI()
        
 
    def initUI(self):
        self.master.title("Computer graphics")
        self.pack(fill=BOTH, expand=True)
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.createPlot()
        self.createMenu()
        self.drawShape()
        
        self.plot.axis('square')
        self.pack()
        
    
    def createPlot(self):
        figure = Figure(figsize=(5, 5))
    
        self.canvas = FigureCanvasTkAgg(figure, self)
        toolbar = NavigationToolbar2Tk(self.canvas, self).grid(row=0, column=0, columnspan=2,
            padx=5, sticky=E+W+S+N)
        self.plot = figure.add_subplot()
        
        self.canvas .get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=2, sticky=E+W+S+N, pady=5, padx=5)
    
        
    def createMenu(self):
        labelAngle = Label(self, text="Angle")
        labelAngle.grid(row=3, column=0, pady=5, padx=5)
        
        self.entryAngle = Entry(self)
        self.entryAngle.grid(row=3, column=1, sticky=E+W+S+N, pady=5, padx=5)
        
        labelCoordinates = Label(self, text="Coordinates of the point relative to which the turn will be made")
        labelCoordinates.grid(row=4, columnspan=2, sticky=E+W+S+N, pady=5, padx=5)
        
        labelX = Label(self, text="x")
        labelX.grid(row=5, column=0, sticky=E+W+S+N, pady=5, padx=5)
        
        self.entryX = Entry(self)
        self.entryX.grid(row=5, column=1, sticky=E+W+S+N, pady=5, padx=5)
        
        labelY = Label(self, text="y")
        labelY.grid(row=6, column=0, sticky=E+W+S+N, pady=5, padx=5)
        
        self.entryY = Entry(self)
        self.entryY.grid(row=6, column=1, sticky=E+W+S+N, pady=5, padx=5)
  
        btn = Button(self, text="Turn", command=self.onSubmit)
        btn.grid(row=7, columnspan=2, sticky=E+W+S+N, pady=5, padx=5)
        
    def drawPoint(self, x, y):
        circle = Circle((x,y),0.05, fc="red",ec="red")
        self.plot.add_patch(circle)
    
    def drawShape(self):
        p = Polygon(self.shape, closed=False)
        self.plot.add_patch(p)
        
    
    def onSubmit(self):
        angle = float(self.entryAngle.get())
        x = float(self.entryX.get())
        y = float(self.entryY.get())
        
        for i in decimal_range(0, angle, angle / 30):
            self.plot.clear()
            self.shape = np.delete(rotateShapeOnAngleRelativeToPoint(np.matrix(np.c_[self.shape, np.ones((3, 1), dtype=float)]), 
                                                                    angle / 30, x, y), np.s_[2:], axis=1)
            self.drawShape()
            self.drawPoint(x, y)
            self.plot.axis('square')
            self.canvas.draw()
            self.canvas.flush_events()
            
            plt.pause(0.001)
        
 
def decimal_range(start, stop, increment):
    while start < stop:
        yield start
        start += increment


def rotateShapeOnAngleRelativeToPoint(shape, angle : float, x : float, y : float):
    angleInRadians = angle * np.pi / 180
    newCoordinateSystemMatrix = np.matrix([[1, 0, 0], 
                                          [0, 1, 0], 
                                          [-x, -y, 1]])
    shapeRotateMatrix = np.matrix([[np.cos(angleInRadians), np.sin(angleInRadians), 0], 
                                 [-np.sin(angleInRadians), np.cos(angleInRadians), 0], 
                                 [0, 0, 1]])
    oldCoordinateSystemMatrix = np.matrix([[1, 0, 0], 
                                          [0, 1, 0], 
                                          [x, y, 1]])
    
    return shape * newCoordinateSystemMatrix * shapeRotateMatrix * oldCoordinateSystemMatrix

    
def main():
    root = Tk()
    root.columnconfigure(1, weight=1)
    app = Window()
    root.mainloop()

    
    
    
if __name__ == '__main__':
    main()