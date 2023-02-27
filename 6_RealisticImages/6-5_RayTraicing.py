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
        
        self.initUI()
        
 
    def initUI(self):
        self.master.title("Computer graphics")
        self.pack(fill=BOTH, expand=True)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)

        self.createPlot()
        self.createMenu()
        self.plot.axis('auto')
        self.pack()

        
    
    def createPlot(self):
        figure = Figure()
    
        self.canvas = FigureCanvasTkAgg(figure, self)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.plot = figure.add_subplot()
        
        toolbar.grid(row=0, column=0, padx=5, sticky=E+W+S+N, columnspan=6)
        self.canvas .get_tk_widget().grid(row=1, column=0, columnspan=6, sticky=E+W+S+N, pady=5, padx=5)
    
        
    def createMenu(self):
        self.progress_bar = Progressbar(self, orient="horizontal", mode="determinate", maximum=100, value=0)
        self.progress_bar.grid(row=2, sticky=E+W+S+N, pady=5, padx=5, columnspan=6)
        
        label1 = Label(self, text="Сфера 1")
        label1.grid(row=3, column=0, sticky=E+S+N, pady=5, padx=5)
        self.entryX1 = Entry(self)
        self.entryX1.grid(row=3, column=1, sticky=W+S+N, pady=5, padx=5)
        self.entryY1 = Entry(self)
        self.entryY1.grid(row=3, column=2, sticky=W+S+N, pady=5, padx=5)
        self.entryZ1 = Entry(self)
        self.entryZ1.grid(row=3, column=3, sticky=W+S+N, pady=5, padx=5)
        labelR1 = Label(self, text="Радиус")
        labelR1.grid(row=3, column=4, sticky=E+S+N, pady=5, padx=5)
        self.entryR1 = Entry(self)
        self.entryR1.grid(row=3, column=5, sticky=W+S+N, pady=5, padx=5)
        
        label2 = Label(self, text="Сфера 2")
        label2.grid(row=4, column=0, sticky=E+S+N, pady=5, padx=5)
        self.entryX2 = Entry(self)
        self.entryX2.grid(row=4, column=1, sticky=W+S+N, pady=5, padx=5)
        self.entryY2 = Entry(self)
        self.entryY2.grid(row=4, column=2, sticky=W+S+N, pady=5, padx=5)
        self.entryZ2 = Entry(self)
        self.entryZ2.grid(row=4, column=3, sticky=W+S+N, pady=5, padx=5)
        labelR2 = Label(self, text="Радиус")
        labelR2.grid(row=4, column=4, sticky=E+S+N, pady=5, padx=5)
        self.entryR2 = Entry(self)
        self.entryR2.grid(row=4, column=5, sticky=W+S+N, pady=5, padx=5)
        
        label3 = Label(self, text="Сфера 3")
        label3.grid(row=5, column=0, sticky=E+S+N, pady=5, padx=5)
        self.entryX3 = Entry(self)
        self.entryX3.grid(row=5, column=1, sticky=W+S+N, pady=5, padx=5)
        self.entryY3 = Entry(self)
        self.entryY3.grid(row=5, column=2, sticky=W+S+N, pady=5, padx=5)
        self.entryZ3 = Entry(self)
        self.entryZ3.grid(row=5, column=3, sticky=W+S+N, pady=5, padx=5)
        labelR3 = Label(self, text="Радиус")
        labelR3.grid(row=5, column=4, sticky=E+S+N, pady=5, padx=5)
        self.entryR3 = Entry(self)
        self.entryR3.grid(row=5, column=5, sticky=W+S+N, pady=5, padx=5)
        
        self.insertDefaultValues()
        
        btn = Button(self, text="Build", command=self.buildPlot)
        btn.grid(row=6, sticky=E+W+S+N, pady=5, padx=5, columnspan=6)

        
    
    def buildPlot(self):
        self.drawShape()
        
    
    def insertDefaultValues(self):
        self.entryX1.insert(0, .75)
        self.entryY1.insert(0, .1)
        self.entryZ1.insert(0, 1.)
        self.entryR1.insert(0, .6)
        
        self.entryX2.insert(0, -.75)
        self.entryY2.insert(0, .1)
        self.entryZ2.insert(0, 2.25)
        self.entryR2.insert(0, .6)
        
        self.entryX3.insert(0, -2.75)
        self.entryY3.insert(0, .1)
        self.entryZ3.insert(0, 3.5)
        self.entryR3.insert(0, .6)
    
    
    def drawShape(self):
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
            scene = [add_sphere([float(self.entryX1.get()), 
                                 float(self.entryY1.get()), 
                                 float(self.entryZ1.get())], 
                                float(self.entryR1.get()), [0., 0., 1.]),
                    add_sphere([float(self.entryX2.get()), 
                                 float(self.entryY2.get()), 
                                 float(self.entryZ2.get())], 
                                float(self.entryR2.get()), [.5, .223, .5]),
                    add_sphere([float(self.entryX3.get()), 
                                 float(self.entryY3.get()), 
                                 float(self.entryZ3.get())], 
                                float(self.entryR3.get()), [1., .572, .184]),
                    add_plane([0., -.5, 0.], [0., 1., 0.]),
                ]
            print(type(scene))
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
        O = np.array([0., 0.35, -1.])
        Q = np.array([0., 0., 0.])
        img = np.zeros((h, w, 3))

        r = float(w) / h
        S = (-1., -1. / r + .25, 1., 1. / r + .25)

        rows = np.linspace(S[1], S[3], h)
        columns = np.linspace(S[0], S[2], w)

        for j, y in random.sample(list(enumerate(rows)), len(rows)):
            for i, x in random.sample(list(enumerate(columns)), len(columns)):
                if i % 10 == 0:
                    self.progress_bar['value'] = i / float(w) * 100
                    self.update()
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
        self.plot.clear()
        self.plot.imshow(img)
        self.canvas.draw()
        self.canvas.flush_events()
        
        self.progress_bar['value'] = 0
        self.update()
    
        

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
        color=lambda M: (color_plane0 
            if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2) else color_plane1),
        diffuse_c=.75, specular_c=.5, reflection=.25)

    
def main():
    root = Tk()
    app = Window()
    root.mainloop()

    
    
    
if __name__ == '__main__':
    main()