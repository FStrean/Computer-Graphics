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
import random


class Window(Frame):
    
    def __init__(self):
        super().__init__()
        
        self.sphere_number = 0
        self.rows = []
        
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
        vscrollbar.grid(row=1, column=6, sticky=N+S+E)
        canvas.create_window((0, 0), window=self.inputMenuContainer, anchor="nw")
        
        canvas.bind_all("<MouseWheel>", lambda e : canvas.yview_scroll(-1 * int((e.delta / 120)), "units"))
        self.inputMenuContainer.bind("<Configure>", lambda e : canvas.configure(scrollregion=canvas.bbox(ALL)))
        
        
        self.addSphere()
        self.addSphere()
        self.addSphere()
        
        self.insertDefaultValues()
        
        build = Button(self, text="Построить", command=self.buildPlot)
        build.grid(row=2, rowspan=2, sticky=E+W+S+N, pady=5, padx=5, columnspan=3)
        
        add_new_sphere = Button(self, text="Добавить новую сферу", command=self.addSphere)
        add_new_sphere.grid(row=3, column=3, sticky=E+W+S+N, pady=5, padx=5, columnspan=3)

        
    def addSphere(self):
        label1 = Label(self.inputMenuContainer, text="Сфера " + str(self.sphere_number + 1))
        label1.grid(row=self.sphere_number, column=0, sticky=E+S+N, pady=5, padx=5)
        entryX = Entry(self.inputMenuContainer)
        entryX.grid(row=self.sphere_number, column=1, sticky=W+S+N, pady=5, padx=5)
        entryY = Entry(self.inputMenuContainer)
        entryY.grid(row=self.sphere_number, column=2, sticky=W+S+N, pady=5, padx=5)
        entryZ = Entry(self.inputMenuContainer)
        entryZ.grid(row=self.sphere_number, column=3, sticky=W+S+N, pady=5, padx=5)
        labelR = Label(self.inputMenuContainer, text="Радиус")
        labelR.grid(row=self.sphere_number, column=4, sticky=E+S+N, pady=5, padx=5)
        entryR = Entry(self.inputMenuContainer)
        entryR.grid(row=self.sphere_number, column=5, sticky=W+S+N, pady=5, padx=5)
        
        self.rows.append([label1, entryX, entryY, entryZ, labelR, entryR])
        
        self.sphere_number += 1
        
    
    def insertDefaultValues(self):
        self.rows[0][1].insert(0, .8)
        self.rows[0][2].insert(0, .4)
        self.rows[0][3].insert(0, 1.)
        self.rows[0][5].insert(0, .6)
        
        self.rows[1][1].insert(0, -.75)
        self.rows[1][2].insert(0, 0)
        self.rows[1][3].insert(0, 2)
        self.rows[1][5].insert(0, .9)
        
        self.rows[2][1].insert(0, -1)
        self.rows[2][2].insert(0, .1)
        self.rows[2][3].insert(0, 0.5)
        self.rows[2][5].insert(0, .6)
    
    
    def getValues(self):
        scene = []
        for row in self.rows:
            scene.append(add_sphere([float(row[1].get()), float(row[2].get()), float(row[3].get())], 
                                    float(row[5].get()), [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]))
            
        scene.append(add_plane([0., -.5, 0.], [0., 1., 0.]))
        return scene
    
    
    def buildPlot(self):
        global color_plane0
        global color_plane1
        global scene
        global L
        global color_light
        global ambient
        global diffuse_c
        global specular_c
        global specular_k
        global w
        global h
        global O
        
        w = 500
        h = 200
        
        color_plane0 = 1. * np.ones(3)
        color_plane1 = 0. * np.ones(3)
        try:
            scene = self.getValues()
        except ValueError:
            return

        L = np.array([5., 5., -10.])
        color_light = np.ones(3)

        ambient = .05
        diffuse_c = 1.
        specular_c = 1.
        specular_k = 50

        depth_max = 5
        col = np.zeros(3)
        O = np.array([0, 0.35, -1.])
        Q = np.array([0., 0., 0.])
        img = np.zeros((h, w, 3))

        r = float(w) / h
        S = (-1., -1. / r + .25, 1., 1. / r + .25)

        rows = np.linspace(S[1], S[3], h)
        columns = np.linspace(S[0], S[2], w)
        print(rows)

        for j, y in random.sample(list(enumerate(rows)), len(rows)):
            for i, x in random.sample(list(enumerate(columns)), len(columns)):
                col[:] = 0
                Q[:2] = (x, y)
                D = normalize(Q - O)
                depth = 0
                rayO, rayD = O, D
                reflection = 1.
                while depth < depth_max:
                    traced = trace_ray(rayO, rayD)
                    if not traced:
                        break
                    obj, M, N, col_ray = traced
                    rayO, rayD = M + N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
                    depth += 1
                    col += reflection * col_ray
                    reflection *= obj.get('reflection', 1.)
                img[h - j - 1, i, :] = np.clip(col, 0, 1)
            self.plot.clear()
            self.plot.imshow(img)
            self.canvas.draw()
            self.canvas.flush_events()
        plt.imsave('fig.png', img)
    
        

def normalize(x):
    x /= np.linalg.norm(x)
    return x

def intersect_plane(O, D, P, N):
    denom = np.dot(D, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(P - O, N) / denom
    if d < 0:
        return np.inf
    return d

def intersect_sphere(O, D, S, R):
    a = np.dot(D, D)
    OS = O - S
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
    disc = b * b - 4 * a * c
    if disc > 0:
        distSqrt = np.sqrt(disc)
        q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return np.inf

def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])

def get_normal(obj, M):
    if obj['type'] == 'sphere':
        N = normalize(M - obj['position'])
    elif obj['type'] == 'plane':
        N = obj['normal']
    return N
    
def get_color(obj, M):
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(M)
    return color

def trace_ray(rayO, rayD):
    t = np.inf
    for i, obj in enumerate(scene):
        t_obj = intersect(rayO, rayD, obj)
        if t_obj < t:
            t, obj_idx = t_obj, i
    if t == np.inf:
        return

    obj = scene[obj_idx]
    M = rayO + rayD * t
    N = get_normal(obj, M)
    color = get_color(obj, M)
    toL = normalize(L - M)
    toO = normalize(O - M)
    l = [intersect(M + N * .0001, toL, obj_sh) 
            for k, obj_sh in enumerate(scene) if k != obj_idx]
    if l and min(l) < np.inf:
        return
    col_ray = ambient
    col_ray += obj.get('diffuse_c', diffuse_c) * max(np.dot(N, toL), 0) * color
    col_ray += obj.get('specular_c', specular_c) * max(np.dot(N, normalize(toL + toO)), 0) ** specular_k * color_light
    return obj, M, N, col_ray

def add_sphere(position, radius, color):
    return dict(type='sphere', position=np.array(position), 
        radius=np.array(radius), color=np.array(color), reflection=.5)
    
def add_plane(position, normal):
    return dict(type='plane', position=np.array(position), 
        normal=np.array(normal),
        color=color_plane0,
        diffuse_c=.75, specular_c=.5, reflection=0.25)

    
def main():
    root = Tk()
    app = Window()
    root.mainloop()

    
    
    
if __name__ == '__main__':
    main()