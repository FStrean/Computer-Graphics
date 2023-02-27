import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from tkinter import *
from tkinter.ttk import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)
from scipy.special import comb

matplotlib.use("TkAgg")


class Window(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self._animation_checkbutton = None
        self._old_plot_checkbutton = None
        self._new_plot_checkbutton = None

        self._plot = None

        self._canvas = None
        self._input_menu_container = None

        self.entry = None
        self.comboBox = None

        self.delete_column_buttons = list()
        self.rows = list()

        self.column_number = 0
        self.row_number = 0

        self._points = [[[-150, 0, 150], [-150, 50, 50], [-150, 50, -50], [-150, 0, -150]],
                        [[-50, 50, 150], [-50, -300, 50], [-50, 50, -50], [-50, 50, -150]],
                        [[50, 50, 150], [50, 50, 50], [50, 300, -50], [50, 50, -150]],
                        [[150, 0, 150], [150, 50, 50], [150, 50, -50], [150, 0, -150]]]
        self._old_points = None
        self._set_limits_function = None

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
        self._plot = figure.add_subplot(projection="3d")

        NavigationToolbar2Tk(self._canvas, self).grid(row=0, column=0, columnspan=3, sticky=E + W + S + N,
                                                      pady=5, padx=5)
        self._canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky=E + W + S + N, pady=5, padx=5)

    def create_menu(self):
        def insert_default_values():
            for i in range(self.row_number):
                for j in range(self.column_number):
                    for k in range(3):
                        self.rows[i][j + 1][k].insert(0, self._points[i][j][k])

        self._new_plot_checkbutton = Checkbutton(self, text="Show new plot", command=self.draw_plots)
        self._new_plot_checkbutton.state(['!alternate'])
        self._new_plot_checkbutton.state(['selected'])

        self._old_plot_checkbutton = Checkbutton(self, text="Show old plot", command=self.draw_plots)
        self._old_plot_checkbutton.state(['!alternate'])
        self._old_plot_checkbutton.state(['selected'])

        self._animation_checkbutton = Checkbutton(self, text="Enable animation")
        self._animation_checkbutton.state(['!alternate'])
        self._animation_checkbutton.state(['selected'])

        self._new_plot_checkbutton.grid(row=0, column=3, sticky=EW, pady=5, padx=5)
        self._old_plot_checkbutton.grid(row=0, column=4, sticky=EW, pady=5, padx=5)
        self._animation_checkbutton.grid(row=0, column=5, sticky=EW, pady=5, padx=5)

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

        while self.column_number < 4:
            self.add_delete_column_button()

        while self.row_number < 4:
            self.add_new_row()

        insert_default_values()

        rotate_relative_to_x_or_y_button = Button(self, text="Rotate", command=self.rotate_plot)
        label1 = Label(self, text="curve relative to ")
        self.comboBox = Combobox(self, values=["X", "Y"])
        label2 = Label(self, text="on")
        self.entry = Entry(self)
        label3 = Label(self, text="degrees")

        rotate_relative_to_x_or_y_button.grid(row=2, column=0, sticky=NSEW, pady=5, padx=5)
        label1.grid(row=2, column=1, sticky=E, pady=5, padx=5)
        self.comboBox.grid(row=2, column=2, sticky=NSEW, pady=5, padx=5)
        label2.grid(row=3, column=0, sticky=E, pady=5, padx=5)
        self.entry.grid(row=3, column=1, sticky=EW, pady=5, padx=5)
        label3.grid(row=3, column=2, sticky=E, pady=5, padx=5)

        add_new_points_button = Button(self, text="Add new row", command=self.add_new_row)
        delete_points_button = Button(self, text="Add new column", command=self.add_new_column)
        build_plot_button = Button(self, text="Build plot", command=self.on_build_plot)

        add_new_points_button.grid(row=3, column=3, columnspan=3, sticky=NSEW, pady=5, padx=5)
        delete_points_button.grid(row=4, column=3, columnspan=3, sticky=NSEW, pady=5, padx=5)
        build_plot_button.grid(row=4, column=0, columnspan=3, sticky=NSEW, pady=5, padx=5)

    def add_new_row(self):
        delete_button = Button(self._input_menu_container, text="-", width=3)
        delete_button.grid(row=self.row_number + 1, column=0, sticky=EW, pady=5, padx=(0, 10))
        row = [delete_button]

        delete_button.configure(command=lambda: self.delete_row(delete_button))

        for col in range(self.column_number):
            entry1 = Entry(self._input_menu_container, width=5)
            entry2 = Entry(self._input_menu_container, width=5)
            entry3 = Entry(self._input_menu_container, width=5)
            entry1.grid(row=self.row_number + 1, column=col * 3 + 1, sticky=EW, pady=5, padx=1)
            entry2.grid(row=self.row_number + 1, column=col * 3 + 2, sticky=EW, pady=5, padx=1)
            entry3.grid(row=self.row_number + 1, column=col * 3 + 3, sticky=EW, pady=5, padx=(1, 20))
            row.append([entry1, entry2, entry3])
        self.rows.append(row)

        self.row_number += 1

    def add_new_column(self):
        for row in self.rows:
            row_number = row[0].grid_info()["row"]

            entry1 = Entry(self._input_menu_container, width=5)
            entry2 = Entry(self._input_menu_container, width=5)
            entry3 = Entry(self._input_menu_container, width=5)
            entry1.grid(row=row_number, column=self.column_number * 3 + 1, sticky=EW, pady=5, padx=1)
            entry2.grid(row=row_number, column=self.column_number * 3 + 2, sticky=EW, pady=5, padx=1)
            entry3.grid(row=row_number, column=self.column_number * 3 + 3, sticky=EW, pady=5, padx=(1, 20))

            row.append([entry1, entry2, entry3])

        self.add_delete_column_button()

    def add_delete_column_button(self):
        delete_button = Button(self._input_menu_container, text="-", width=3)
        delete_button.grid(row=0, column=self.column_number * 3 + 1, columnspan=3, sticky=EW, pady=5, padx=(1, 20))
        delete_button.configure(command=lambda: self.delete_column(delete_button))
        self.delete_column_buttons.append(delete_button)
        self.column_number += 1

    def delete_row(self, row_widget):
        row_number = row_widget.grid_info()["row"] - 1
        if self.row_number > 4:
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
                        grid_info = entry.grid_info()
                        entry.grid(row=grid_info["row"] - 1, column=grid_info["column"], sticky=grid_info["sticky"],
                                   pady=grid_info["pady"], padx=grid_info["padx"])
            self.row_number -= 1

    def delete_column(self, column_widget):
        column_number = column_widget.grid_info()["column"] // 3 + 1
        if self.column_number > 4:
            column_widget.destroy()
            for row in self.rows:
                for entry in row[column_number]:
                    entry.destroy()
                del row[column_number]
            for row_ in self.rows:
                for column in row_[column_number:]:
                    for entry in column:
                        grid_info = entry.grid_info()
                        entry.grid(row=grid_info["row"], column=grid_info["column"] - 3, sticky=grid_info["sticky"],
                                   pady=grid_info["pady"], padx=grid_info["padx"])
            del self.delete_column_buttons[column_number - 1]
            for delete_button in self.delete_column_buttons[column_number - 1:]:
                grid_info = delete_button.grid_info()
                delete_button.grid(row=grid_info["row"], column=grid_info["column"] - 3,
                                   columnspan=grid_info["columnspan"], sticky=grid_info["sticky"],
                                   pady=grid_info["pady"], padx=grid_info["padx"])
            self.column_number -= 1

    def on_build_plot(self):
        self._plot.clear()
        self.build_plot()
        self._canvas.draw()
        self._canvas.flush_events()

    def build_plot(self):
        self._points = []
        try:
            for row in self.rows:
                points_row = []
                for point in row[1:]:
                    points_point = []
                    for entry in point:
                        points_point.append(float(entry.get()))
                    points_row.append(points_point)
                self._points.append(points_row)
        except ValueError:
            return
        if self._new_plot_checkbutton.instate(['selected']):
            self.draw_bezier_surface_with_points(np.array(self._points))

    def draw_bezier_surface_with_points(self, points, color="red", surface_color="Reds", are_labels_allowed=True):
        x, y, z = build_bezier_surface(points)

        self._plot.plot_surface(x, y, z, cmap=surface_color, linewidth=1, antialiased=False, alpha=0.7)

        i = 0
        for row in points:
            self._plot.plot(row[:, 0], row[:, 1], row[:, 2], "o:", color=color)
            if are_labels_allowed:
                for point in row:
                    self._plot.text(point[0], point[1], point[2], '%s' % (str(i)), size=10, zorder=15,
                                    color='k')
                    i += 1

        for column in range(points.shape[1]):
            self._plot.plot(points[:, column, 0], points[:, column, 1], points[:, column, 2], "o:", color=color)

    def draw_plots(self, is_rotating=False):
        self._plot.clear()

        if is_rotating:
            self._set_limits_function()
        self.build_plot()
        if self._old_plot_checkbutton.instate(['selected']) and self._old_points:
            self.draw_bezier_surface_with_points(np.array(self._old_points), color="black", surface_color="Greys",
                                                 are_labels_allowed=False)

        self._canvas.draw()
        self._canvas.flush_events()

    def rotate_plot(self):
        def set_limits_yz():
            self._plot.set(ylim=(-max_val, max_val), zlim=(-max_val, max_val))

        def set_limits_xz():
            self._plot.set(xlim=(-max_val, max_val), zlim=(-max_val, max_val))

        try:
            angle = float(self.entry.get()) * np.pi / 180
        except ValueError:
            return

        if len(self._points) != len(self.rows) or len(self._points[0]) != len(self.rows[0]) - 1:
            self.on_build_plot()

        if self.comboBox.get() == "X":
            maximum = []
            for row in self._points:
                row = np.matrix(row)
                maximum.append(np.amax(np.sum((row - np.c_[row[:, 0],
                                                           np.zeros((np.shape(row)[0], 2), dtype=float)]).getA() ** 2,
                                              axis=1) ** (1 / 2)))

            max_val = np.amax(np.array(maximum))
            rotate = rotate_relative_to_x
            self._set_limits_function = set_limits_yz
        elif self.comboBox.get() == "Y":
            maximum = []
            for row in self._points:
                row = np.matrix(row)
                maximum.append(
                    np.amax(np.sum((row - np.c_[np.c_[np.zeros((np.shape(row)[0], 1), dtype=float), row[:, 1]],
                                                np.zeros((np.shape(row)[0], 1),
                                                         dtype=float)]).getA() ** 2, axis=1) ** (1 / 2)))
            max_val = np.amax(np.array(maximum))
            rotate = rotate_relative_to_y
            self._set_limits_function = set_limits_xz
        else:
            return

        self._old_points = self._points.copy()

        def rotate_plot(rotate_angle):
            new_points = list()
            for _row in self._points:
                new_points.append(rotate(rotate_angle, np.matrix(_row)).getA())
            self._points = new_points
            for row_number in range(len(self.rows)):
                for column_number in range(1, len(self.rows[0])):
                    for entry_number in range(len(self.rows[0][1])):
                        try:
                            self.rows[row_number][column_number][entry_number].delete(0, END)
                            self.rows[row_number][column_number][entry_number].insert(0, float(
                                self._points[row_number][column_number - 1][entry_number]))
                        except ValueError:
                            return
            self.draw_plots(is_rotating=True)

        if self._new_plot_checkbutton.instate(['selected']) and self._animation_checkbutton.instate(['selected']):
            for _ in decimal_range(0, angle, angle / 30):
                rotate_plot(angle / 30)
                plt.pause(0.001)
        else:
            rotate_plot(angle)


def decimal_range(start, stop, increment):
    while start < stop:
        yield start
        start += increment


def build_bezier_surface(points):
    def bezier_matrix(d):
        return np.array([[(-1) ** (i - j) * comb(j, i) * comb(d, j)
                          for i in range(d + 1)] for j in range(d + 1)], int)

    count_u, count_v, _ = points.shape
    degree_u, degree_v = count_u - 1, count_v - 1

    resolution = (16, 16)
    u, v = np.linspace(0, 1, resolution[0]), np.linspace(0, 1, resolution[1])
    u_vector = np.array([u ** i for i in range(count_u)])
    v_vector = np.array([v ** i for i in range(count_v)])

    bezier_matrix = [bezier_matrix(i) for i in range(16)]
    bezier_matrix_u, bezier_matrix_v = bezier_matrix[degree_u], bezier_matrix[degree_v]

    m1 = u_vector.T.dot(bezier_matrix_u)
    m2 = bezier_matrix_v.T.dot(v_vector)

    x = m1.dot(points[:, :, 0]).dot(m2)
    y = m1.dot(points[:, :, 1]).dot(m2)
    z = m1.dot(points[:, :, 2]).dot(m2)

    return x, y, z


def rotate_relative_to_x(angle, points):
    rotate_matrix = np.matrix([[1, 0, 0],
                               [0, np.cos(angle), -np.sin(angle)],
                               [0, np.sin(angle), np.cos(angle)]])
    return points * rotate_matrix


def rotate_relative_to_y(angle, points):
    rotate_matrix = np.matrix([[np.cos(angle), 0, np.sin(angle)],
                               [0, 1, 0],
                               [-np.sin(angle), 0, np.cos(angle)]])
    return points * rotate_matrix


def main():
    root = Tk()
    root.title("Computer graphics")
    Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
