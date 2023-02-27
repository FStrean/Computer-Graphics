from tkinter import *
from tkinter.ttk import *
import matplotlib
matplotlib.use("TkAgg")
import math


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)
from matplotlib.patches import Rectangle

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
        self.rowconfigure(7, weight=0)

        self.createPlot()
        self.createMenu()
        
    
    def createPlot(self):
        figure = Figure(figsize=(5, 5))
    
        self.canvas = FigureCanvasTkAgg(figure, self)
        self._plot = figure.add_subplot()
        
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
    
        self.add_new_line()
        
        label1 = Label(self, text="x_min, x_max")
        self.entry1 = Entry(self, width=5)
        self.entry2 = Entry(self, width=5)
        
        label2 = Label(self, text="y_min, y_max")
        self.entry3 = Entry(self, width=5)
        self.entry4 = Entry(self, width=5)
        
        label1.grid(row=4, column=0, sticky=W, pady=5, padx=1)
        self.entry1.grid(row=4, column=1, sticky=W, pady=5, padx=1)
        self.entry2.grid(row=4, column=2, sticky=W, pady=5, padx=1)
        label2.grid(row=5, column=0, sticky=W, pady=5, padx=1)
        self.entry3.grid(row=5, column=1, sticky=W, pady=5, padx=1)
        self.entry4.grid(row=5, column=2, sticky=W, pady=5, padx=1)
  
        addNewPointButton = Button(self, text="Add line", command=self.add_new_line)
        buildPlotButton = Button(self, text="Build plot", command=self.on_build_plot)
        
        addNewPointButton.grid(row=6, columnspan=6, sticky=NSEW, pady=5, padx=5)
        buildPlotButton.grid(row=7, columnspan=6, sticky=NSEW, pady=5, padx=5)
    
    def add_new_line(self):         
        label1 = Label(self.inputMenuContainer, text="P1")
        label1.grid(row=self.pointNubmer, column=0, sticky=W, pady=5, padx=1)
        entry1 = Entry(self.inputMenuContainer, width=5)
        entry1.grid(row=self.pointNubmer, column=1, sticky=W, pady=5, padx=1)
        entry2 = Entry(self.inputMenuContainer, width=5)
        entry2.grid(row=self.pointNubmer, column=2, sticky=W, pady=5, padx=(1, 20))
        
        label2 = Label(self.inputMenuContainer, text="P2")
        label2.grid(row=self.pointNubmer, column=3, sticky=W, pady=5, padx=1)
        entry3 = Entry(self.inputMenuContainer, width=5)
        entry3.grid(row=self.pointNubmer, column=4, sticky=W, pady=5, padx=1)
        entry4 = Entry(self.inputMenuContainer, width=5)
        entry4.grid(row=self.pointNubmer, column=5, sticky=W, pady=5, padx=(1, 40))
            
        
        delete_button = Button(self.inputMenuContainer, text="Delete")
        delete_button.grid(row=self.pointNubmer, column=6, sticky=EW, pady=5, padx=5)
        
        row = [label1, entry1, entry2, label2, entry3, entry4, delete_button]
        self.rows.append(row)
                
        delete_button.configure(command=lambda : self.delete_point(row))
        
        self.pointNubmer += 1
    
    
    def delete_point(self, row):
        if(self.pointNubmer > 1):
            row_number = row[0].grid_info()["row"]
            for column in row:
                column.destroy()   
            del self.rows[row_number]
            for row_ in self.rows[row_number:]:
                for column in row_:
                    grinfo = column.grid_info()
                    column.grid(row=grinfo["row"] - 1, column=grinfo["column"], sticky=grinfo["sticky"], pady=grinfo["pady"], padx=grinfo["padx"])
            self.pointNubmer -= 1
    
    
    def on_build_plot(self):
        self._plot.clear()
        self.build_plot()
        self.canvas.draw()
        self.canvas.flush_events()
    
    
    def build_plot(self):
        self._points = []
        x_min, x_max, y_min, y_max = None, None, None, None
        try:
            x_min, x_max, y_min, y_max = float(self.entry1.get()), float(self.entry2.get()), float(self.entry3.get()), float(self.entry4.get())
            if x_min >= x_max or y_min >= y_max:
                raise ValueError
            for row in self.rows:
                self._points.append([float(row[1].get()), float(row[2].get()), 
                                    float(row[4].get()), float(row[5].get())])
        except ValueError:
            return
        self.draw_lines_and_screen(np.array(self._points), x_min, x_max, y_min, y_max)
        
        
    def draw_lines_and_screen(self, points, x_min, x_max, y_min, y_max):
        self._plot.add_patch(Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, color="blue", fill=None, alpha=1))
        for point in points:
            self._plot.plot([point[0], point[2]], [point[1], point[3]], color="red")
            try:
                _x1, _y1, _x2, _y2 = cohenSutherlandClip(point[0], point[1], point[2], point[3], 
                                                         x_min, x_max, y_min, y_max)
                self._plot.plot([_x1, _x2], [_y1, _y2], color="green")
            except ValueError:
                continue


def cohenSutherlandClip(x1, y1, x2, y2, x_min, x_max, y_min, y_max):
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8
    def area_code(x, y):
        code = INSIDE
        if x < x_min:
            code |= LEFT
        elif x > x_max:
            code |= RIGHT
        if y < y_min:
            code |= BOTTOM
        elif y > y_max:
            code |= TOP
        return code
    code1, code2= area_code(x1, y1), area_code(x2, y2)
    accept = False
    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        elif (code1 & code2) != 0:
            break
        else:
            x = 1.0
            y = 1.0
            if code1 != 0: code_out = code1
            else: code_out = code2
            if code_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min
            if code_out == code1:
                x1 = x
                y1 = y
                code1 = area_code(x1, y1)
            else:
                x2 = x
                y2 = y
                code2 = area_code(x2, y2)
    if accept: return x1, y1, x2, y2
    else: raise ValueError("Line is not on the screen")


    
def main():
    root = Tk()
    Window(root)
    root.mainloop()
    
    
    
if __name__ == '__main__':
    main()