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
        self.points = [[10, 15, 0],
                       [-11, -15, 8],
                       [0, 0, 40],
                       [58, 25, -5],
                       [-40, 40, 14],
                       [-9, -30, -41],
                       [8, 8, 20],
                       [26, 5, -30],
                       [-22, -9, -50],
                       [31, 29, 27]]
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
        self.plot = figure.add_subplot(projection="3d")
        
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
        
        while(self.pointNubmer < 10):
            self.addNewPoint()
        
        self.insertDefaultValues()
        
        rotateRelativeToXOrYButton = Button(self, text="Rotate", command=self.rotatePlot)
        label1 = Label(self, text="curve relative to ")
        self.comboBox = Combobox(self, values=["X", "Y"])
        label2 = Label(self, text="on")
        self.entry = Entry(self)
        label3 = Label(self, text="degrees")
        
        rotateRelativeToXOrYButton.grid(row=2, column=0, sticky=NSEW, pady=5, padx=5)
        label1.grid(row=2, column=1, sticky=E, pady=5, padx=5)
        self.comboBox.grid(row=2, column=2, sticky=NSEW, pady=5, padx=5)
        label2.grid(row=3, column=0, sticky=E, pady=5, padx=5)
        self.entry.grid(row=3, column=1, sticky=EW, pady=5, padx=5)
        label3.grid(row=3, column=2, sticky=E, pady=5, padx=5)
        
        
        addNewPointsButton = Button(self, text="Add points", command=self.addNewPoint)
        deletePointsButton = Button(self, text="Delete selected points", command=self.deletePoints)
        buildPlotButton = Button(self, text="Build plot", command=self.onbuildPlot)
        
        addNewPointsButton.grid(row=3, column=3, columnspan=3, sticky=NSEW, pady=5, padx=5)
        deletePointsButton.grid(row=4, column=3, columnspan=3, sticky=NSEW, pady=5, padx=5)
        buildPlotButton.grid(row=4, column=0, columnspan=3, sticky=NSEW, pady=5, padx=5)
    
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
        
        delete_checkbutton = Checkbutton(self.inputMenuContainer)
        delete_checkbutton.state(['!alternate'])
        delete_checkbutton.grid(row=self.pointNubmer, column=6, sticky=EW, pady=5, padx=10)
        row = [label1, entry1, label2, entry2, label3, entry3, delete_checkbutton]
        self.rows.append(row)
        
        self.pointNubmer += 1
    
    
    def deletePoints(self):
        rows = []
        for row in self.rows:
            if row[6].instate(['selected']):
                rows.append(row)       
        if (self.pointNubmer - len(rows)) >= 10:
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
    
    def insertDefaultValues(self):
        for i in range(len(self.rows)):
            self.rows[i][1].insert(0, self.points[i][0])
            self.rows[i][3].insert(0, self.points[i][1])
            self.rows[i][5].insert(0, self.points[i][2])
    
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
        self.drawCompoisiteBezierCurveAndPolylineWithPoints(self.points)
        
    def drawCompoisiteBezierCurveAndPolylineWithPoints(self, input_points, color="blue", new_point_color="green"):
        points = []
        for i in range(1, len(input_points)-1, 2):
            intermediate_point = []
            for j in range(i, i+2):
                intermediate_point.append(input_points[j])
            points.append(intermediate_point)
                
        points[0].insert(0, input_points[0])
        points[len(points)-1].append(input_points[len(input_points)-1])
        
        if len(points[len(points)-1]) != 3:
            points[len(points)-1].append(input_points[len(input_points)-1])
        
        curve, new_points = buildCompositeBezierCurveWithPoints(points)
        for part in curve:  
            self.plot.plot(part[:, 0], part[:, 1], part[:, 2], color=color)
        input_points = np.array(input_points)
        self.plot.plot(input_points[:, 0], input_points[:, 1], input_points[:, 2], 'o:', color=color)
        
        self.plot.scatter(new_points[:, 0], new_points[:, 1], new_points[:, 2], color=new_point_color)
       
        
    def rotatePlot(self):
        try:
            angle = float(self.entry.get()) * np.pi / 180
        except:
            return
        rotate = None
        
        if(np.shape(self.points)[0] != len(self.rows)):
            self.onbuildPlot()
        
        set_lim_func = None

        points = np.array(self.points)
        
        if(self.comboBox.get() == "X"): 
            maximum = np.amax(np.sum((points - 
                                        np.c_[points[:, 0], 
                                        np.zeros((np.shape(points)[0], 2), dtype=float)])**2, axis=1)**(1/2))
            rotate = rotateRelativeToX
            set_lim_func = lambda: self.plot.set(ylim=(-maximum, maximum), zlim=(-maximum, maximum))
        elif(self.comboBox.get() == "Y"):      
            maximum = np.amax(np.sum((points - 
                                        np.c_[np.c_[np.zeros((np.shape(points)[0], 1), dtype=float), 
                                                    points[:, 1]], 
                                              np.zeros((np.shape(points)[0], 1), dtype=float)])**2, axis=1)**(1/2))
            rotate = rotateRelativeToY
            set_lim_func = lambda: self.plot.set(xlim=(-maximum, maximum), zlim=(-maximum, maximum))
        else: 
            return
        
        oldPoints = self.points.copy()

        for _ in decimal_range(0, angle, angle / 30):
            self.points = rotate(angle / 30, np.matrix(self.points))
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
            self.drawCompoisiteBezierCurveAndPolylineWithPoints(oldPoints, color="red", new_point_color="purple")
            self.canvas.draw()
            self.canvas.flush_events()
            plt.pause(0.001)
        
 
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
    new_points = []
    new_point = [0, 0, 0]
    for k in range(0, len(points)):
        coordinates = []
        for i in range(3):
            intermediate_point = []
            for coordinate in points[k]:
                intermediate_point.append(coordinate[i])
            coordinates.append(intermediate_point)
            
        if k != 0:
            coordinates[0].insert(0, new_point[0])
            coordinates[1].insert(0, new_point[1])
            coordinates[2].insert(0, new_point[2])    
     
        n = 4    
        if k != len(points) - 1:
            
            new_point[0] = (points[k][len(points[k]) - 1][0] + points[k+1][0][0]) / 2
            new_point[1] = (points[k][len(points[k]) - 1][1] + points[k+1][0][1]) / 2
            new_point[2] = (points[k][len(points[k]) - 1][2] + points[k+1][0][2]) / 2
            
            new_points.append(new_point.copy())
            
            coordinates[0].append(new_point[0])
            coordinates[1].append(new_point[1])
            coordinates[2].append(new_point[2])
        intermediate = []
        for t in np.linspace (0., 1., 25):
            intermediate_line = []
            for coord in coordinates:
                intermediate_line.append(B(coord, 0, n - 1, t))
            intermediate.append(intermediate_line)
        result.append(intermediate)
    return np.array(result), np.array(new_points)

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
    Window(root)
    root.mainloop()
    
    
    
if __name__ == '__main__':
    main()
    