import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from scipy.interpolate import griddata



class sensors:
    
    def make(self,x_min=0,x_max=0,y_min=0,y_max=0,nx=1,ny=1,height=0.8,file='points.pts'):
        with open(file, 'w') as f:
            x = np.linspace(x_min,x_max,nx)
            y = np.linspace(y_min,y_max,ny)
            for i in x:
                for j in y:
                    print(i,j,height,0,0,1,file=f)
    def read(file,grid=False,array=False):
        x,y,z, _, _, _ = np.loadtxt(file).T
        x_grid,y_grid,z_grid = np.unique(x), np.unique(y), np.unique(z)
        nx, ny, nz = len(x_grid), len(y_grid), len(z_grid)
        y_max = np.max(y)
        y_min = np.min(y)
        x_max = np.max(x)
        x_min = np.min(x)
        
        print("nx:    {}".format(nx))
        print("ny:    {}".format(ny))
        print("y_max: {}".format(y_max))
        print("y_min: {}".format(y_min))
        print("x_max: {}".format(x_max))
        print("x_min: {}".format(x_min))
        
        if (grid):
            return x_grid,y_grid
        if (array):
            return x,y
                    
                    
class daylight:
    """
    Class to read txt files from a Radiance Simulation, calculate and render UDIs, illuminance maps and others.

    Use:
    a = ill.daylight(arg1)

    Parameters
    ----------
    arg1 : path of the ILL file to load into a DataFrame.
    arg1 = 'data/CEEA.ill'
    Returns
    nx: number of elements in the x direction of the grid
    ny: number of elements in the y direction of the grid
    Lx: Lenght in the x direction of the grid
    Ly: Lenght in the y direction of the grid
    dx: Size of the grid in the x direction
    dy: Size of the grid in the y direction
    -------
    The class contains the following methods:
    
    udi()
        Calculate the UDI [https://patternguide.advancedbuildings.net/using-this-guide/analysis-methods/useful-daylight-illuminance]
        defining the following parameters:
        E_LL:  Lower limit illumination level [lx]
        E_UL:  Upper limit illumination level [lx]
        t_min: Start hour of day to evaluate the UDI [h]
        t_http://localhost:8891/edit/modulos/illumination.py#max: End hout of day to evaluate the UDI [h]
        dC:    Number of color leves for the UDI [-]
        Once executed, prints the frequency of visual comfort (FVC).
        
    map()
        Plot the illuminance map for the space for a specific day, time and renders using a maximum value of the illuminance:
        day:  day to plot the illuminance map [-]
        hour: Time of day (0,24) to plot the illuminance map [h]
        Lmax: Maximum value to render illuminance map [lx]
    
    x()
        Plot the illuminance along the x direction at a specific value of y:
        day:  day to plot the illuminance along the x direction [-]
        hour: Time of day (0,24) to plot the illuminance along the x direction [h]
        jj:   Number of element (0,Ly) to plot the illuminance along the x direcion [-]
        
    
    y()
        Plot the illuminance along the y direction at a specific value of x:
        day:  day to plot the illuminance along the x direction [-]
        hour: Time of day (0,24) to plot the illuminance along the y direction [h]
        ii:   Number of element (0,Lx) to plot the illuminance along the y direcion [-]

    """

    def __init__(self,illuminance, sensores):
        self.x,self.y,self.z, _, _, _ = np.loadtxt(sensores).T
        self.x_grid, self.y_grid, self.z_grid = np.unique(self.x), np.unique(self.y), np.unique(self.z)
        self.nx, self.ny, self.nz = len(self.x_grid), len(self.y_grid), len(self.z_grid)
        self.y_max = np.max(self.y)
        self.y_min = np.min(self.y)
        self.x_max = np.max(self.x)
        self.x_min = np.min(self.x)
        self.s = np.genfromtxt(illuminance,skip_header=10,delimiter=' ').T
        
        print("Datos obtenidos con Radiance")
        print("nx:    {}".format(self.nx))
        print("ny:    {}".format(self.ny))
        print("y_max: {}".format(self.y_max))
        print("y_min: {}".format(self.y_min))
        print("x_max: {}".format(self.x_max))
        print("x_min: {}".format(self.x_min))
    def mapa(self,dia=1,hora=12,Lmax=2000,niveles=10):
        position = (dia-1)*24+(hora-1)
        mapa = self.s[position].reshape(self.nx,self.ny)
        fig, ax1 = plt.subplots(figsize=(10,8))
        plt.set_cmap('jet')
        bar = ax1.contourf(self.x_grid,self.y_grid,mapa.T,levels = np.linspace(0,Lmax,niveles) )
        plt.colorbar(bar,ticks=np.linspace(0,Lmax,niveles),label=('Illuminance $[lx]$'))
        plt.xlabel('x$[m]$')
        plt.ylabel('y$[m]$')
        return self.x_grid,self.y_grid,mapa.T
    def profile_X(self,dia,hora,position_x):
        position = (dia-1)*24+(hora-1)
        mapa = self.s[position].reshape(self.nx,self.ny).flatten()

        j = np.linspace(self.y_min,self.y_max,self.ny)
        i =  np.array([position_x] * self.ny)
        mediciones = np.array([i,j])
        lineal = griddata((self.x, self.y),mapa, (i,j) , method='linear')
        return j,lineal
    def profile_Y(self,dia,hora,position_y):
        position = (dia-1)*24+(hora-1)
        mapa = self.s[position].reshape(self.nx,self.ny).flatten()

        i = np.linspace(self.x_min,self.x_max,self.nx)
        j =  np.array([position_y] * self.nx)
        mediciones = np.array([i,j])
        lineal = griddata((self.x, self.y),mapa, (i,j) , method='linear')
        return i,lineal
