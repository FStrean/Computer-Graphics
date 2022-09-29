from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy as np


class Window(Frame):
    
    def __init__(self):
        super().__init__()
        self.shape = np.matrix([[0, 0, 0], 
                  [2, 0, 0], 
                  [1, 1, 0], 
                  [1, 0, 1]], dtype=float)
        self.initUI()
        
 
    def initUI(self):
        self.master.title("Computer graphics")
        self.pack(fill=BOTH, expand=True)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)

        self.createPlot()
        self.createMenu()
        self.drawShape()
        
        self.plot.axis('auto')
        self.pack()
        
    
    def createPlot(self):
        figure = Figure(figsize=(5, 5))
    
        self.canvas = FigureCanvasTkAgg(figure, self)
        toolbar = NavigationToolbar2Tk(self.canvas, self).grid(row=0, column=0, columnspan=6,
            padx=5, sticky=E+W+S+N)
        self.plot = figure.add_subplot(projection="3d")
        
        self.canvas .get_tk_widget().grid(row=1, column=0, columnspan=6, rowspan=2, sticky=E+W+S+N, pady=5, padx=5)
    
        
    def createMenu(self):
        labelAngle = Label(self, text="Angle")
        labelAngle.grid(row=3, column=0, sticky=E+S+N, pady=5, padx=5)
        
        self.entryAngle = Entry(self)
        self.entryAngle.grid(row=3, column=1, sticky=W+S+N, pady=5, padx=5)
        
        labelCoordinates = Label(self, text="Coordinates of the line relative to which the turn will be made")
        labelCoordinates.grid(row=4, columnspan=6, sticky=E+W+S+N, pady=5, padx=5)
        
        
        
        labelX1 = Label(self, text="x1")
        labelX1.grid(row=5, column=0, sticky=E+S+N, pady=5, padx=5)
        
        self.entryX1 = Entry(self)
        self.entryX1.grid(row=5, column=1, sticky=W+S+N, pady=5, padx=5)
        
        labelY1 = Label(self, text="y1")
        labelY1.grid(row=5, column=2, sticky=E+S+N, pady=5, padx=5)
        
        self.entryY1 = Entry(self)
        self.entryY1.grid(row=5, column=3, sticky=W+S+N, pady=5, padx=5)
        
        labelZ1 = Label(self, text="z1")
        labelZ1.grid(row=5, column=4, sticky=E+S+N, pady=5, padx=5)
        
        self.entryZ1 = Entry(self)
        self.entryZ1.grid(row=5, column=5, sticky=W+S+N, pady=5, padx=5)
        
        
        
        labelX2 = Label(self, text="x2")
        labelX2.grid(row=6, column=0, sticky=E+S+N, pady=5, padx=5)
        
        self.entryX2 = Entry(self)
        self.entryX2.grid(row=6, column=1, sticky=W+S+N, pady=5, padx=5)
        
        labelY2 = Label(self, text="y2")
        labelY2.grid(row=6, column=2, sticky=E+S+N, pady=5, padx=5)
        
        self.entryY2 = Entry(self)
        self.entryY2.grid(row=6, column=3, sticky=W+S+N, pady=5, padx=5)
        
        labelZ2 = Label(self, text="z2")
        labelZ2.grid(row=6, column=4, sticky=E+S+N, pady=5, padx=5)
        
        self.entryZ2 = Entry(self)
        self.entryZ2.grid(row=6, column=5, sticky=W+S+N, pady=5, padx=5)
        
        
  
        btn = Button(self, text="Turn", command=self.onSubmit)
        btn.grid(row=7, columnspan=6, sticky=E+W+S+N, pady=5, padx=5)
        
    def drawLine(self, x1, y1, x2, y2, z1, z2):
        self.plot.plot([x1, x2], [y1,y2], [z1,z2], color="red")
    
    def drawShape(self):
        vertices = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]

        tupleList = self.shape.tolist()
        poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
        self.plot.scatter(self.shape[:, 0], self.shape[:, 1], self.shape[:, 2])
        collection = Poly3DCollection(poly3d, linewidths=1, alpha=0.7)
        face_color = [0.5, 0.5, 1] # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
        edge_color=[0, 0, 0]
        collection.set_facecolor(face_color)
        collection.set_edgecolor(edge_color)
        self.plot.add_collection3d(collection)
    
    def onSubmit(self):
        angle = float(self.entryAngle.get())
        x1 = float(self.entryX1.get())
        y1 = float(self.entryY1.get())
        z1 = float(self.entryZ1.get())
        
        x2 = float(self.entryX2.get())
        y2 = float(self.entryY2.get())
        z2 = float(self.entryZ2.get())
        
        for i in decimal_range(0, angle, angle / 30):
            self.plot.clear()
            self.shape = np.delete(rotateShapeOnAngleRelativeToLineInSpace(np.matrix(np.c_[self.shape, np.ones((4, 1), dtype=float)]), 
                                                                           angle / 30, x1, y1, z1, x2, y2, z2), np.s_[3:], axis=1)
            self.drawShape()
            self.drawLine(x1, y1, x2, y2, z1, z2)
            self.plot.axis('auto')
            self.canvas.draw()
            self.canvas.flush_events()
            
            plt.pause(0.001)
        
        
        
 
def decimal_range(start, stop, increment):
    while start < stop:
        yield start
        start += increment


def rotateShapeOnAngleRelativeToLineInSpace(shape, angle : float, x1 : float, y1 : float, z1 : float,  
                                     x2 : float, y2 : float, z2 : float):
    angleInRadians = angle * np.pi / 180

    x = x2 - x1
    y = y2 - y1
    z = z2 - z1
    d = (x**2 + y**2 + z**2)**(1/2)
    cx = x / d
    cy = y / d
    cz = z / d
    d = (cy**2 + cz**2)**(1/2)
    cos = np.cos(angleInRadians)
    sin = np.sin(angleInRadians)
    
    T = np.matrix([[1, 0, 0, 0], 
                   [0, 1, 0, 0], 
                   [0, 0, 1, 0], 
                   [-x1, -y1, -z1, 1]])
    Rx = np.matrix([[1, 0, 0, 0], 
                    [0, cz/d, cy/d, 0],
                    [0, -cy/d, cz/d, 0],
                    [0, 0, 0, 1]])
    
    Ry = np.matrix([[d, 0, cx, 0], 
                    [0, 1, 0, 0],
                    [-cx, 0, d, 0], 
                    [0, 0, 0, 1]])
    
    Rb = np.matrix([[cos, sin, 0, 0], 
                    [-sin, cos, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    
    shapeRotateMatrix = T * Rx * Ry * Rb * Ry**(-1)*Rx**(-1)*T**(-1)
    
    return shape * shapeRotateMatrix

    
def main():
    root = Tk()
    root.columnconfigure(1, weight=1)
    app = Window()
    root.mainloop()

    
    
    
if __name__ == '__main__':
    main()