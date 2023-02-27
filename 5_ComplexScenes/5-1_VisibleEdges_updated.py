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
                  [2, 0, -.5], 
                  [0, 2, -.5], 
                  [0, 0, 2]], dtype=float)
        
        self.H = [8.75, 0.75 , 20]
        
        self.initUI()
        
 
    def initUI(self):
        self.master.title("Computer graphics")
        self.pack(fill=BOTH, expand=True)
        self._edges_checkbutton = None
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.createPlot()
        
        
        self.createMenu()
        self.drawShape(self.shape)
        
        self.plot.axis('auto')
        self.pack()
        
        self.rotatePlot()
        
    
    def insertDefaultValues(self):
        for i in range(4):
            for j in range(3):
                self.rows[i][j].insert(0, self.shape[i, j])
    
    def set_lim(self):
        self.plot.set(xlim = (-5, 5), ylim = (-5, 5), zlim = (-5, 5))
    
    def createPlot(self):
        figure = Figure(figsize=(5, 5))
    
        self.canvas = FigureCanvasTkAgg(figure, self)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.plot = figure.add_subplot(projection="3d")
        
        toolbar.grid(row=0, column=0, padx=5, sticky=E+W+S+N)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=E+W+S+N, pady=5, padx=5)
    
        
    def createMenu(self):
        self.plot.azim = 0
        self.plot.dist = 10
        self.plot.elev = 45
        
        self._edges_checkbutton = Checkbutton(self, text="Показывать невидимые грани")
        self._edges_checkbutton.state(['!alternate'])
        self._edges_checkbutton.state(['selected'])
        
        self._edges_checkbutton.grid(row=0, column=1, sticky=EW, pady=5, padx=5)
        
        self._alpha_checkbutton = Checkbutton(self, text="Фигура полупрозрачна")
        self._alpha_checkbutton.state(['!alternate'])
        self._alpha_checkbutton.state(['selected'])
        
        self._alpha_checkbutton.grid(row=0, column=2, sticky=EW, pady=5, padx=5)
        
        canvas = Canvas(self)
        self.inputMenuContainer = Frame(canvas)
        hscrollbar = Scrollbar(self, orient=HORIZONTAL, command=canvas.xview)
        vscrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        
        canvas.configure(xscrollcommand=hscrollbar.set, yscrollcommand=vscrollbar.set)
        
        canvas.grid(row=1, column=1, sticky=NSEW, columnspan=2)
        hscrollbar.grid(row=2, column=1, columnspan=3, sticky=W+E)
        vscrollbar.grid(row=1, column=3, sticky=N+S+E)
        canvas.create_window((0, 0), window=self.inputMenuContainer, anchor="nw")
        
        canvas.bind_all("<MouseWheel>", lambda e : canvas.yview_scroll(-1 * int((e.delta / 120)), "units"))
        self.inputMenuContainer.bind("<Configure>", lambda e : canvas.configure(scrollregion=canvas.bbox(ALL)))
        self.rows = []
        for _row in range(1, 5):
            label1 = Label(self.inputMenuContainer, text="x")
            label1.grid(row=_row, column=1, sticky=E, pady=5, padx=5)
            entry1 = Entry(self.inputMenuContainer)
            entry1.grid(row=_row, column=2, sticky=EW, pady=5, padx=5)
                
            label2 = Label(self.inputMenuContainer, text="y")
            label2.grid(row=_row, column=3, sticky=E, pady=5, padx=5)
            entry2 = Entry(self.inputMenuContainer)
            entry2.grid(row=_row, column=4, sticky=EW, pady=5, padx=5)
            
            label3 = Label(self.inputMenuContainer, text="z")
            label3.grid(row=_row, column=5, sticky=E, pady=5, padx=5)
            entry3 = Entry(self.inputMenuContainer)
            entry3.grid(row=_row, column=6, sticky=EW, pady=5, padx=5)
            
            self.rows.append([entry1, entry2, entry3])
        
        self.insertDefaultValues()
        change_coords_button = Button(self, text="Изменить координаты тетраэдра", command=self.change_coords)
        change_coords_button.grid(row=3, column=1, sticky=NSEW, pady=5, padx=5)
        
    def change_coords(self):
        try:
            for i in range(4):
                self.shape[i, 0] = float(self.rows[i][0].get())
                self.shape[i, 1] = float(self.rows[i][1].get())
                self.shape[i, 2] = float(self.rows[i][2].get())
        except:
            return
            
    def check_if_visible(self, vertice):
        def det(dots, vertice):
            d = np.array([[dots[0] - vertice[0][0], dots[1] - vertice[0][1], dots[2] - vertice[0][2]], 
                          [vertice[1][0] - vertice[0][0], vertice[1][1] - vertice[0][1], vertice[1][2] - vertice[0][2]], 
                          [vertice[2][0] - vertice[0][0], vertice[2][1] - vertice[0][1], vertice[2][2] - vertice[0][2]]])
            return np.linalg.det(d)
        
        if det(self.O, vertice) * det(self.H, vertice) < 0:
            return True
        else:
            return False
    
    def drawShape(self, shape, face_color = [0.5, 0.5, 1]):
        self.O = [((shape[1, 0] + shape[2, 0] + shape[3, 0]) / 3 + shape[0, 0]) / 2,
                  ((shape[1, 1] + shape[2, 1] + shape[3, 1]) / 3 + shape[0, 1]) / 2, 
                  ((shape[1, 2] + shape[2, 2] + shape[3, 2]) / 3 + shape[0, 2]) / 2]

        self.plot.plot([self.H[0], self.O[0]], [self.H[1], self.O[1]], [self.H[2], self.O[2]], marker = 'o')
        
        vertices = []
        
        vertice = [shape.tolist()[0], shape.tolist()[1], shape.tolist()[2]]

        if self._edges_checkbutton.instate(['selected']) or self.check_if_visible(vertice):
            vertices.append([0, 1, 2])
            
        vertice = [shape.tolist()[0], shape.tolist()[1], shape.tolist()[3]]
        if self._edges_checkbutton.instate(['selected']) or self.check_if_visible(vertice):
            vertices.append([0, 1, 3])
            
        vertice = [shape.tolist()[0], shape.tolist()[2], shape.tolist()[3]]
        if self._edges_checkbutton.instate(['selected']) or self.check_if_visible(vertice):
            vertices.append([0, 2, 3])
            
        vertice = [shape.tolist()[1], shape.tolist()[2], shape.tolist()[3]]
        if self._edges_checkbutton.instate(['selected']) or self.check_if_visible(vertice):
            vertices.append([1, 2, 3])
            
        alpha = 1
        if self._alpha_checkbutton.instate(['selected']):
            alpha = 0.5
        tupleList = shape.tolist()
        poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
        collection = Poly3DCollection(poly3d, linewidths=1, alpha=alpha)
        edge_color=[0, 0, 0]
        collection.set_facecolor(face_color)
        collection.set_edgecolor(edge_color)
        self.plot.add_collection3d(collection)
    
        
    def rotatePlot(self):
        
        speed = 45
        while True:
            angle = 90
            for _ in range(0, angle, angle // speed):
                self.shape = rotateRelativeToX(angle // speed, self.shape)
                    
                self.plot.clear()
                self.drawShape(self.shape)
                self.set_lim()
                self.canvas.draw()
                self.canvas.flush_events()
                
                plt.pause(0.01)
                
            angle = 90
            for _ in decimal_range(0, angle, angle // speed):
                self.shape = rotateRelativeToY(angle // speed, self.shape)
                    
                self.plot.clear()
                self.drawShape(self.shape)
                self.set_lim()
                self.canvas.draw()
                self.canvas.flush_events()
                
                plt.pause(0.01)
        
def rotateRelativeToX(angle, points):
    angleInRadians = angle * np.pi / 180
    rotateMatrix = np.matrix([[1, 0, 0],
                              [0, np.cos(angleInRadians), -np.sin(angleInRadians)],
                              [0, np.sin(angleInRadians), np.cos(angleInRadians)]])
    return points * rotateMatrix


def rotateRelativeToY(angle, points):
    angleInRadians = angle * np.pi / 180
    rotateMatrix = np.matrix([[np.cos(angleInRadians), 0, np.sin(angleInRadians)],
                              [0, 1, 0],
                              [-np.sin(angleInRadians), 0, np.cos(angleInRadians)]])
    return points * rotateMatrix       
 
def decimal_range(start, stop, increment):
    while start < stop:
        yield start
        start += increment

    
    
def main():
    root = Tk()
    app = Window()
    root.mainloop()

    
    
    
if __name__ == '__main__':
    main()
    