import numpy as np
from scipy.integrate import *
import matplotlib.pyplot as plt, mpld3
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

from pathlib import Path
import logging
from server.models.BaseModelsSchema import BaseModel, Schema, SchemaObject, SchemaObjectType

class Evolvability(BaseModel):

    """ 
    # pop1 = 10 #initial population density: species 1
    # pop2 = 10 #initial population density: species 2
    # strat1 = .5 #initial strategy: species 1
    # strat2 = .5 #initial strategy: species 2

    # time = 1000
    # KM = 100
    # d = [0.05,0.05]
    # r = [0.25,0.25]
    # k = [.2,.5]  # evolvability: how fast the species scale the adaptive landscape 
    # """

    ModelSchema = Schema(
        'Evolvabilty Model', 
        {
            'pop1': SchemaObject(10, 'pop1', 'Population 1 (pop1)'),
            'pop2': SchemaObject(10, 'pop2', 'Population 2 (pop2)'),
            'strat1': SchemaObject(.5, 'strat1', 'Strategy 1 (strat1)'),
            'strat2': SchemaObject(.5, 'strat2', 'Strategey 2 (strat2)'),
            'time': SchemaObject(1500, 'time', 'Time'),
            'km': SchemaObject(100, 'km', 'km'),
            'd1': SchemaObject(0.05, 'd1', 'd1'),
            'd2': SchemaObject(0.05, 'd2', 'd2'),
            'r1': SchemaObject(0.25, 'r1', 'r1'),
            'r2': SchemaObject(0.25, 'r2', 'r2'),
            'k1': SchemaObject(0.2, 'k1','Population 1 Evolvability: how fast cells can climb adaptive landscape (k1)'),
            'k2': SchemaObject(0.5, 'k2','Population 2 Evolvability: how fast cells can climb adaptive landscape (k2)'),
        })

    def __init__(self):
        super(Evolvability, self).__init__(self)

    def __Run__(self):
        plt.switch_backend('Agg')
        logging.info("Running Evolvability")

        def evoLV(X, t):
            gamma = 0 #g1[int(t)]

            x1 = X[0]
            x2 = X[1]
            u1 = X[2]
            u2 = X[3]

            K1 = self.KM * math.exp(-((u1 - self.gamma) ** 2) / (2 * self.sk))
            K2 = self.KM * math.exp(-((u2 - self.gamma) ** 2) / (2 * self.sk))

            a2 = 1 + math.exp(-(u1 - u2 + self.B) ** 2 / (2 * self.sa)) - math.exp(-(self.B ** 2 / (2 * self.sa)))
            a1 = 1 + math.exp(-(u2 - u1 + self.B) ** 2 / (2 * self.sa)) - math.exp(-(self.B ** 2 / (2 * self.sa)))

            dx1dt = x1 * (self.r[0]/K1 * (K1 - a2*x2 - x1) - self.d[0]*self.k[0])
            dx2dt = x2 * (self.r[1]/K2 * (K2 - a1*x1 - x2) - self.d[1]*self.k[1])

            dG1dv = (-(u1-self.gamma)*self.r[0]*self.KM*(x1+a2*x2))/(K1*K1*self.sk)*math.exp(-((u1-gamma)**2)/(2*self.sk)) + (self.r[0]*x2*(u1-u2+self.B))/(K1*self.sa)*math.exp(-((u1-u2+self.B)**2)/(2*self.sa))
            dG2dv = (-(u2-self.gamma)*self.r[1]*self.KM*(a1*x1+x2))/(K2*K2*self.sk)*math.exp(-((u2-gamma)**2)/(2*self.sk)) + (self.r[1]*x1*(u2-u1+self.B))/(K2*self.sa)*math.exp(-((u2-u1+self.B)**2)/(2*self.sa))

            dv1dt = self.k[0] * dG1dv
            dv2dt = self.k[1] * dG2dv

            dxvdt = np.array([dx1dt, dx2dt, dv1dt, dv2dt])
            return dxvdt

        def fastG(self, u2, time_G):

            '''if time_G>4500:
                gamma = 0
            elif time_G>3900:
                gamma = -4.5
            elif time_G>3200:
                gamma = 0
            elif time_G>2500:
                gamma = -4.5
            elif time_G>1700: #1500
                gamma = 0
            elif time_G>800:
                gamma = -4.5
            else:
                gamma = 0

            #gamma = 0 #g1[int(time_G)]

            if time_G>700:
                gamma = -4
            else:
                gamma = 0'''

            #gamma = np.sin(time_G/50)

            x1 = self.pop[time_G][0]
            x2 = self.pop[time_G][1]
            u1 = self.pop[time_G][2]
            a1 = 1 + math.exp(-(u2 - u1 + self.B) ** 2 / (2 * self.sa)) - math.exp(-(self.B ** 2 / (2 * self.sa)))
            K2 = self.KM * math.exp(-((u2 - self.gamma) ** 2) / (2 * self.sk))
            Gfunc2 = self.r[1] / K2 * (K2 - a1 * x1 - x2) - self.d[1] * self.k[1]
            if Gfunc2<-1:
                Gfunc2=-1
            return Gfunc2

        def slowG(self, u1, time_G):
            '''if time_G>4500:
                gamma = 0
            elif time_G>3900:
                gamma = -4.5
            elif time_G>3200:
                gamma = 0
            elif time_G>2500:
                gamma = -4.5
            elif time_G>1700: #1500
                gamma = 0
            elif time_G>800:
                gamma = -4.5
            else:
                gamma = 0

            #gamma = 0 #g1[int(time_G)]

            if time_G > 700:
                gamma = -4
            else:
                gamma = 0'''

            #gamma = np.sin(time_G/50)

            x1 = self.pop[time_G][0]
            x2 = self.pop[time_G][1]
            u2 = self.pop[time_G][3]
            a2 = 1 + math.exp(-(u1 - u2 + self.B) ** 2 / (2 * self.sa)) - math.exp(-(self.B ** 2 / (2 * self.sa)))
            K1 = self.KM * math.exp(-((u1 - self.gamma) ** 2) / (2 * self.sk))
            Gfunc1 = self.r[0] / K1 * (K1 - a2 * x2 - x1) - self.d[0] * self.k[0]
            if Gfunc1<-1:
                Gfunc1 = -1
            return Gfunc1

        self.gamma = 0
        self.pop1 = 10 #initial population density: species 1
        self.pop2 = 10 #initial population density: species 2
        self.strat1 = .5 #initial strategy: species 1
        self.strat2 = .5 #initial strategy: species 2

        self.time = int(self.Parameters['time'])
        
        self.KM = float(self.Parameters['km'])
        self.d = [float(self.Parameters['d1']),float(self.Parameters['d2'])]
        self.r = [float(self.Parameters['r1']),float(self.Parameters['r2'])]
        self.k = [float(self.Parameters['k1']),float(self.Parameters['k2'])]  # evolvability: how fast the species scale the adaptive landscape

        self.k_curr = [self.k[0]]
        self.r_curr = [self.r[0]]
        self.d_curr = [self.d[0]]

        self.IC = [self.pop1,self.pop2,self.strat1,self.strat2]

        self.sk = 12.5 # squared value
        self.sa = 2 #
        self.B = 0 # NOT squared value

        self.intxv = np.array(self.IC)
        self.pop = odeint(evoLV, self.intxv, range(self.time+1))

        #Plotting Adaptive Landscape: 3-Dimensional Landscape
        self.gamma = 0
        self.fast = []
        self.slow = []

        self.xp = np.arange(-5, 5, .1)
        self.yp = np.arange(0, 1001, 1)
        self.Xp, self.Yp = np.meshgrid(self.xp, self.yp)

        for i in self.yp:
            temp1 = []
            temp2 = []
            for j in self.xp:
                temp1.append(slowG(self, j,i))
                temp2.append(fastG(self, j,i))
            self.slow.append(temp1)
            self.fast.append(temp2)
            temp1 = temp2 = []

        self.G_fast=[]
        self.G_slow=[]
        for i in self.yp:
            j = self.pop[i][3]
            self.G_fast.append(fastG(self, j,i))

        for i in self.yp:
            j = self.pop[i][2]
            self.G_slow.append(slowG(self, j,i))

        self.slow = np.array(self.slow)
        self.fast = np.array(self.fast)

        fig = plt.figure()

        if self.Is3d:
            
            ax = plt.axes(projection='3d')
            ax.plot_surface(self.Xp, self.Yp, self.slow, cmap='Blues')
            ax.plot_surface(self.Xp, self.Yp, self.fast, cmap='Oranges')
            ax.plot3D(self.pop[:,3],self.yp,self.G_fast,c='greenyellow') #fast
            ax.plot3D(self.pop[:,2],self.yp,self.G_slow,c='c') #slow
            ax.set_xlabel('Evolutionary Strategy: v')
            ax.set_ylabel('Time')
            ax.set_zlabel('Fitness: G')
            ax.set_zlim(-1,0.2)
            ax.view_init(35, 45)
            plt.title('Adaptive Landscape: No Aggressiveness Close',pad=30)
        else:
            #Obtaining extinction times
            for i in range(len(self.pop[:,1])):
                if (self.pop[:,1][i])<2:
                    print(i)
                    print('Fast')
                    break


            for j in range(len(self.pop[:,0])):
                if (self.pop[:,0][j])<2:
                    print(j)
                    print('Slow')
                    break

            # fig = plt.figure()
            plt.subplot(211)
            plt.title('No Aggressiveness: Close to Strategy Equilibrium')
            plt.plot(self.pop[:,0],label='k = ' + str(self.k[0]))
            plt.plot(self.pop[:,1],label='k = ' + str(self.k[1]))
            plt.ylim(ymax=200)
            plt.grid(True)
            plt.ylabel('Pop Size, x')
            plt.subplot(212)
            plt.plot(self.pop[:,2],label='k = ' + str(self.k[0]))
            plt.plot(self.pop[:,3],label='k = ' + str(self.k[1]))
            plt.grid(True)
            plt.ylabel('Indv Strategy, v')

        figDictionary = mpld3.fig_to_dict(fig)
        plt.close()

        return figDictionary
        

