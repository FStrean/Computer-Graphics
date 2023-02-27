import numpy as np
import matplotlib

from tkinter import *
from tkinter.ttk import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)
from matplotlib.patches import Rectangle

matplotlib.use("TkAgg")


class Window(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self._plot = None

        self._canvas = None
        self._input_menu_container = None

        self.entry = None
        self.comboBox = None
        
        self.rows = []
        
        self.row_number = 0

        self._points = []

        self.init_ui()

    def init_ui(self):
        self.grid(sticky=N + S + E + W)

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

        self.create_plot()
        self.create_menu()

    def create_plot(self):
        figure = Figure(figsize=(5, 5))

        self._canvas = FigureCanvasTkAgg(figure, self)
        self._plot = figure.add_subplot()

        NavigationToolbar2Tk(self._canvas, self).grid(row=0, column=0, columnspan=3, sticky=E + W + S + N,
                                                      pady=5, padx=5)
        self._canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky=E + W + S + N, pady=5, padx=5)

    def create_menu(self):
        canvas = Canvas(self)
        self._input_menu_container = Frame(canvas)
        horizontal_scrollbar = Scrollbar(self, orient=HORIZONTAL, command=canvas.xview)
        vertical_scrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)

        canvas.configure(xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set)

        canvas.grid(row=1, column=3, columnspan=3, sticky=NSEW)
        horizontal_scrollbar.grid(row=2, column=3, columnspan=3, sticky=W + E)
        vertical_scrollbar.grid(row=1, column=5, sticky=N + S + E)
        canvas.create_window((0, 0), window=self._input_menu_container, anchor="nw")

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int((e.delta / 120)), "units"))
        self._input_menu_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox(ALL)))
        
        self.add_new_row()
        
        label1 = Label(self, text="x_min, x_max")
        self.entry1 = Entry(self, width=5)
        self.entry2 = Entry(self, width=5)
        
        label2 = Label(self, text="y_min, y_max")
        self.entry3 = Entry(self, width=5)
        self.entry4 = Entry(self, width=5)
        
        label1.grid(row=3, column=3, sticky=W, pady=5, padx=1)
        self.entry1.grid(row=3, column=4, sticky=W, pady=5, padx=1)
        self.entry2.grid(row=3, column=5, sticky=W, pady=5, padx=1)
        label2.grid(row=4, column=3, sticky=W, pady=5, padx=1)
        self.entry3.grid(row=4, column=4, sticky=W, pady=5, padx=1)
        self.entry4.grid(row=4, column=5, sticky=W, pady=5, padx=1)

        addNewRow = Button(self, text="Add new row", command=self.add_new_row)
        build_plot_button = Button(self, text="Build plot", command=self.on_build_plot)
        
        addNewRow.grid(row=5, column=0, columnspan=3, sticky=NSEW, pady=5, padx=5)
        build_plot_button.grid(row=4, column=0, columnspan=3, sticky=NSEW, pady=5, padx=5)

    def add_new_row(self):
        delete_button = Button(self._input_menu_container, text="-", width=3)
        delete_button.grid(row=self.row_number, column=0, sticky=EW, pady=5, padx=(0, 10))
        
        label1 = Label(self._input_menu_container, text="P1")
        entry1 = Entry(self._input_menu_container, width=5)
        entry2 = Entry(self._input_menu_container, width=5)
        
        label2 = Label(self._input_menu_container, text="P2")
        entry3 = Entry(self._input_menu_container, width=5)
        entry4 = Entry(self._input_menu_container, width=5)
        
        label1.grid(row=self.row_number, column=1, sticky=EW, pady=5, padx=1)
        entry1.grid(row=self.row_number, column=2, sticky=EW, pady=5, padx=1)
        entry2.grid(row=self.row_number, column=3, sticky=EW, pady=5, padx=(1, 20))
        label2.grid(row=self.row_number, column=4, sticky=EW, pady=5, padx=1)
        entry3.grid(row=self.row_number, column=5, sticky=EW, pady=5, padx=1)
        entry4.grid(row=self.row_number, column=6, sticky=EW, pady=5, padx=1)
        
        row = [delete_button, label1, entry1, entry2, label2, entry3, entry4]
        self.rows.append(row)
        
        delete_button.configure(command=lambda: self.delete_row(row))

        self.row_number += 1

    def delete_row(self, row):
        if(self.row_number > 1):
            row_number = row[0].grid_info()["row"]
            for column in row:
                column.destroy()   
            del self.rows[row_number]
            for row_ in self.rows[row_number:]:
                for column in row_:
                    grinfo = column.grid_info()
                    column.grid(row=grinfo["row"] - 1, column=grinfo["column"], sticky=grinfo["sticky"], pady=grinfo["pady"], padx=grinfo["padx"])
            self.row_number -= 1


    def on_build_plot(self):
        self._plot.clear()
        self.build_plot()
        self._canvas.draw()
        self._canvas.flush_events()

    def build_plot(self):
        self._points = []
        x_min, x_max, y_min, y_max = None, None, None, None
        try:
            x_min, x_max, y_min, y_max = float(self.entry1.get()), float(self.entry2.get()), float(self.entry3.get()), float(self.entry4.get())
            if x_min >= x_max or y_min >= y_max:
                raise ValueError
            for row in self.rows:
                self._points.append([float(row[2].get()), float(row[3].get()), 
                                    float(row[5].get()), float(row[6].get())])
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


def decimal_range(start, stop, increment):
    while start < stop:
        yield start
        start += increment


def cohenSutherlandClip(x1, y1, x2, y2, x_min, x_max, y_min, y_max):
    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000
    
    def computeCode(x, y):
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

    code1 = computeCode(x1, y1)
    code2 = computeCode(x2, y2)
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
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2
 
            if code_out & TOP:
                x = x1 + (x2 - x1) * \
                                (y_max - y1) / (y2 - y1)
                y = y_max
 
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * \
                                (y_min - y1) / (y2 - y1)
                y = y_min
 
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * \
                                (x_max - x1) / (x2 - x1)
                x = x_max
 
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * \
                                (x_min - x1) / (x2 - x1)
                x = x_min
 
            if code_out == code1:
                x1 = x
                y1 = y
                code1 = computeCode(x1, y1)
 
            else:
                x2 = x
                y2 = y
                code2 = computeCode(x2, y2)
 
    if accept:
        return x1, y1, x2, y2
    else:
        raise ValueError("Line is out from screen")


def main():
    root = Tk()
    root.title("Computer graphics")
    Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
