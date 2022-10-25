from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)
from scipy.special import comb
from matplotlib import cm

import numpy as np


class Window(Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.points = [[[-150, 0, 150], [-150, 50, 50], [-150, 50, -50], [-150, 0, -150]], 
                       [[-50, 50, 150], [-50, -300, 50], [-50, 50, -50], [-50, 50, -150]],
                       [[50, 50, 150], [50, 50, 50], [50, 300, -50], [50, 50, -150]],
                       [[150, 0, 150], [150, 50, 50], [150, 50, -50], [150, 0, -150]]]
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
        self.rowconfigure(7, weight=0)

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
        
        self.row_number = 0
        self.column_number = 0
        self.rows = list()
        self.delete_column_buttons = list()
        
        while self.column_number < 4:
            self.addDeleteColumnButton()
        
        while self.row_number < 4:
            self.addNewRow()
        
        self.insertDefaultValues()
        
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
        
        
        addNewRow = Button(self, text="Add new row", command=self.addNewRow)
        addNewColumn = Button(self, text="Add new column", command=self.addNewColumn)
        buildPlotButton = Button(self, text="Build plot", command=self.onbuildPlot)
        
        addNewRow.grid(row=5, columnspan=6, sticky=NSEW, pady=5, padx=5)
        addNewColumn.grid(row=6, columnspan=6, sticky=NSEW, pady=5, padx=5)
        buildPlotButton.grid(row=7, columnspan=6, sticky=NSEW, pady=5, padx=5)
    
    def addNewRow(self):
        delete_button = Button(self.inputMenuContainer, text="-", width=3)
        delete_button.grid(row=self.row_number + 1, column=0, sticky=EW, pady=5, padx=(0, 10))
        row = [delete_button] 
        
        delete_button.configure(command=lambda : self.deleteRow(delete_button))
        
        for col in range(self.column_number):
            entry1 = Entry(self.inputMenuContainer, width=5)
            entry2 = Entry(self.inputMenuContainer, width=5)
            entry3 = Entry(self.inputMenuContainer, width=5)
            entry1.grid(row=self.row_number+1, column=col*3+1, sticky=EW, pady=5, padx=1)
            entry2.grid(row=self.row_number+1, column=col*3+2, sticky=EW, pady=5, padx=1)
            entry3.grid(row=self.row_number+1, column=col*3+3, sticky=EW, pady=5, padx=(1, 20))
            row.append([entry1, entry2, entry3])     
        self.rows.append(row)
        
        self.row_number += 1
        
    def addNewColumn(self):
        for row in self.rows:
            row_number = row[0].grid_info()["row"]
            
            entry1 = Entry(self.inputMenuContainer, width=5)
            entry2 = Entry(self.inputMenuContainer, width=5)
            entry3 = Entry(self.inputMenuContainer, width=5)
            entry1.grid(row=row_number, column=self.column_number*3+1, sticky=EW, pady=5, padx=1)
            entry2.grid(row=row_number, column=self.column_number*3+2, sticky=EW, pady=5, padx=1)
            entry3.grid(row=row_number, column=self.column_number*3+3, sticky=EW, pady=5, padx=(1, 20))

            row.append([entry1, entry2, entry3])
            
        self.addDeleteColumnButton()
            
    
    def addDeleteColumnButton(self):
        delete_button = Button(self.inputMenuContainer, text="-", width=3)
        delete_button.grid(row=0, column=self.column_number*3+1, columnspan=3, sticky=EW, pady=5, padx=(1, 20))
        delete_button.configure(command=lambda : self.deleteColumn(delete_button))
        self.delete_column_buttons.append(delete_button)
        self.column_number += 1
    
    def deleteRow(self, row_widget):
        row_number = row_widget.grid_info()["row"] - 1
        if(self.row_number > 4):
            row_widget.destroy()
            for column in self.rows[row_number][1:]:
                for entry in column:
                    entry.destroy()   
            del self.rows[row_number]
            for row_ in self.rows[row_number:]:
                row_[0].grid(row=row_[0].grid_info()["row"] - 1, 
                             column=row_[0].grid_info()["column"], 
                             sticky=row_[0].grid_info()["sticky"], 
                             pady=row_[0].grid_info()["pady"], 
                             padx=row_[0].grid_info()["padx"])
                for column in row_[1:]:
                    for entry in column:
                        grinfo = entry.grid_info()
                        entry.grid(row=grinfo["row"] - 1, column=grinfo["column"], sticky=grinfo["sticky"], pady=grinfo["pady"], padx=grinfo["padx"])
            self.row_number -= 1
            
    def deleteColumn(self, column_widget):
        column_number = column_widget.grid_info()["column"] // 3 + 1
        if(self.column_number > 4):
            column_widget.destroy()
            for row in self.rows:
                for entry in row[column_number]:
                    entry.destroy()
                del row[column_number]
            for row_ in self.rows:
                for column in row_[column_number:]:
                    for entry in column:
                        grinfo = entry.grid_info()
                        entry.grid(row=grinfo["row"], column=grinfo["column"] - 3, sticky=grinfo["sticky"], pady=grinfo["pady"], padx=grinfo["padx"])
            del self.delete_column_buttons[column_number - 1]
            for delete_button in self.delete_column_buttons[column_number - 1:]:
                grinfo = delete_button.grid_info()
                delete_button.grid(row=grinfo["row"], column=grinfo["column"] - 3, columnspan = grinfo["columnspan"], sticky=grinfo["sticky"], pady=grinfo["pady"], padx=grinfo["padx"])
            self.column_number -= 1
    
    def insertDefaultValues(self):
        for i in range(self.row_number):
            for j in range(self.column_number):
                for k in range(3):
                    self.rows[i][j + 1][k].insert(0, self.points[i][j][k])
    
    def onbuildPlot(self):
        self.plot.clear()
        self.buildPlot()
        self.canvas.draw()
        self.canvas.flush_events()
    
    
    def buildPlot(self):
        self.points=[]
        try:
            for row in self.rows:
                points_row = []
                for point in row[1:]:
                    points_point = []
                    for entry in point:
                        points_point.append(float(entry.get()))
                    points_row.append(points_point)
                self.points.append(points_row)
        except:
            return
        self.drawBezierSurfaceWithPoints(np.array(self.points))

        
    def drawBezierSurfaceWithPoints(self, points, color="blue", surface_color = "Blues"):
        x, y, z = buildBezierSurface(points) 
        
        self.plot.plot_surface(x, y, z, cmap=surface_color, linewidth=1, antialiased=False, alpha=0.7)
        
        for row in points:
            self.plot.plot(row[:, 0], row[:, 1], row[:, 2], "o:", color=color)
            
            
        for column in range(points.shape[1]):
            self.plot.plot(points[:, column, 0], points[:, column, 1], points[:, column, 2], "o:", color=color)
        
    def rotatePlot(self):
        try:
            angle = float(self.entry.get()) * np.pi / 180
        except:
            return
        rotate = None
        
        if(len(self.points) != len(self.rows) or len(self.points[0]) != len(self.rows[0]) - 1):
            self.onbuildPlot()
        
        set_lim_func = None

        if(self.comboBox.get() == "X"):
            maximum = []
            for row in self.points:
                row = np.matrix(row)
                maximum.append(np.amax(np.sum((row - np.c_[row[:, 0], 
                                                           np.zeros((np.shape(row)[0], 2), dtype=float)]).getA()**2, axis=1)**(1/2)))
                
            max_val = np.amax(np.array(maximum))
            rotate = rotateRelativeToX
            set_lim_func = lambda: self.plot.set(ylim=(-max_val, max_val), zlim=(-max_val, max_val))
        elif(self.comboBox.get() == "Y"):
            maximum = []
            for row in self.points:  
                row = np.matrix(row)    
                maximum.append(np.amax(np.sum((row - np.c_[np.c_[np.zeros((np.shape(row)[0], 1), dtype=float), row[:, 1]], 
                                                           np.zeros((np.shape(row)[0], 1), dtype=float)]).getA()**2, axis=1)**(1/2)))
            max_val = np.amax(np.array(maximum))
            rotate = rotateRelativeToY
            set_lim_func = lambda: self.plot.set(xlim=(-max_val, max_val), zlim=(-max_val, max_val))
        else: 
            return
        
        oldPoints = self.points.copy()

        for _ in decimal_range(0, angle, angle / 30):
            new_points = list()
            for row in self.points:
                new_points.append(rotate(angle / 30, np.matrix(row)).getA())
            self.points = new_points
            for row_number in range(len(self.rows)):
                for column_number in range(1, len(self.rows[0])):
                    for entry_number in range(len(self.rows[0][1])):
                        self.rows[row_number][column_number][entry_number].delete(0,END)
                        self.rows[row_number][column_number][entry_number].insert(0,float(self.points[row_number][column_number - 1][entry_number]))
                
            self.plot.clear()
            set_lim_func()
            self.buildPlot()
            self.drawBezierSurfaceWithPoints(np.array(oldPoints), color="red", surface_color="Reds")
            self.canvas.draw()
            self.canvas.flush_events()
            plt.pause(0.001)
        
 
def decimal_range(start, stop, increment):
    while start < stop:
        yield start
        start += increment


def buildBezierSurface(cps: np.ndarray, resol=(16, 16)):
    def bezier_matrix(d):
        return np.array([[(-1) ** (i - j) * comb(j, i) * comb(d, j) for i in range(d + 1)] for j in range(d + 1)], int)
    
    
    BM = [bezier_matrix(i) for i in range(16)]
    
    u, v = np.linspace(0, 1, 25), np.linspace(0, 1, 25)

    count_u, count_v, _ = cps.shape
    deg_u, deg_v = count_u - 1, count_v - 1

    u_vec = np.array([u ** i for i in range(count_u)])
    v_vec = np.array([v ** i for i in range(count_v)])

    BM_u, BM_v = BM[deg_u], BM[deg_v]

    cps_x = cps[:, :, 0]
    cps_y = cps[:, :, 1]
    cps_z = cps[:, :, 2]

    m1 = u_vec.T.dot(BM_u)
    m2 = BM_v.T.dot(v_vec)

    x = m1.dot(cps_x).dot(m2)
    y = m1.dot(cps_y).dot(m2)
    z = m1.dot(cps_z).dot(m2)

    return x, y, z
            


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