import numpy as np
from scipy.integrate import *
import matplotlib.pyplot as plt, mpld3
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

from pathlib import Path
import logging
from server.models.BaseModelsSchema import BaseModel, Schema, SchemaObject, SchemaObjectType

class OnePrey(BaseModel):

    ModelSchema = Schema(
        'One Prey Model',
        {
            'pop1': SchemaObject(10, 'pop1', 'Prey'),
            'pop2': SchemaObject(10, 'pop2', 'Predetor'),
            'strat1': SchemaObject(2, 'strat1', 'Strategy 1'),
            'strat2': SchemaObject(-2, 'strat2', 'Strategy 2'),
            'time': SchemaObject(1500, 'time', 'Time'),
            'time_G': SchemaObject(1000, 'time_G', 'time_G'),
            'km': SchemaObject(100, 'km', 'km'),
            'r1': SchemaObject(0.25, 'r1', 'r1'),
            'r2': SchemaObject(0.25, 'r2', 'r2'),
            'c': SchemaObject(0.25, 'c', 'c'),
            'k1': SchemaObject(0.5, 'k1', 'k1'),
            'k2': SchemaObject(0.5, 'k2', 'k2'),
            'bM': SchemaObject(0.5, 'bM', 'bM'),
            'rM': SchemaObject(0.25, 'rM', 'rM')
        })

    def __init__(self):
        super(OnePrey, self).__init__(self)

    def __Run__(self):
        logging.info("Running One Prey")

        def evoLV(X, t):

            x = X[0]
            y = X[1]
            u = X[2]
            mu = X[3]

            K = self.KM*math.exp(-(u**2)/self.sk)

            b1 = self.bM*math.exp(-((u-mu)**2)/self.sb)
            b2 = self.bM*math.exp(-((mu-u)**2)/self.sb)
            r1 = self.rM*math.exp(-(u-mu)**2/self.sr)

            dxdt = x * (self.r1/K*(K-x)-b1*y)
            dydt = y * (self.r2*(1-(y/(self.c*b2*x))))

            dKdv =  (-2*u*self.KM/self.sk)*math.exp(-(u**2)/self.sk)
            db1dv = (-2*self.bM*(u-mu)/self.sb)*math.exp(-((u-mu)**2)/self.sb)
            db2dv = (-2*self.bM*(mu-u)/self.sb)*math.exp(-((mu-u)**2)/self.sb)

            drdv = 0 #(-2*rM*(u-mu)/sr)*math.exp(-((u-mu)**2)/sr)

            dG1dv = self.r1/K*dKdv+(K-x)/(K**2)*(K*drdv-r1*dKdv)-y*db1dv
            dG2dv = self.r2*y*db2dv/(self.c*x*b2**2)

            dudt = self.k[0] * dG1dv
            dmudt = self.k[1] * dG2dv

            dxvdt = np.array([dxdt, dydt, dudt, dmudt])
            return dxvdt

        

        def fastG(self, mu):
            x = self.pop[self.time_G][0]
            y = self.pop[self.time_G][1]
            u = self.pop[self.time_G][2]
            #sb = 10*(1-.0034)**time_G
            b2 = self.bM*math.exp(-(((mu-u)**2)/self.sb))
            Gfunc2 = self.r2*(1-(y/(self.c*b2*x)))
            return Gfunc2

        def slowG(self, u):
            x = self.pop[self.time_G][0]
            y = self.pop[self.time_G][1]
            mu = self.pop[self.time_G][3]
            b1 = self.bM*math.exp(-(((u-mu)**2)/self.sb))
            #sr = 10*(1-.004)**time_G
            #r1 = rM*math.exp(-(u-mu)**2/sr)
            K = self.KM*math.exp(-(u ** 2)/self.sk)
            Gfunc1 = self.r1/K*(K-x)-b1*y
            return Gfunc1

        self.time_G = int(self.Parameters['time_G'])

        self.fast = []
        self.slow = []

        self.pop1 = float(self.Parameters['pop1'])
        self.pop2 = float(self.Parameters['pop2'])
        self.strat1 = float(self.Parameters['strat1'])
        self.strat2 = float(self.Parameters['strat2'])

        self.IC = [self.pop1,self.pop2,self.strat1,self.strat2]

        self.time = int(self.Parameters['time'])
        self.KM = float(self.Parameters['km'])
        self.r1 = float(self.Parameters['r1'])
        self.r2 = float(self.Parameters['r2'])
        self.k = [float(self.Parameters['k1']),float(self.Parameters['k2'])]

        self.sk = 2
        self.sa = 4
        self.sb = 10
        self.sr = 10

        self.bM = float(self.Parameters['bM'])
        self.rM = float(self.Parameters['rM'])

        self.c = float(self.Parameters['c'])

        self.intxv = np.array(self.IC)
        self.pop = odeint(evoLV, self.intxv, range(self.time+1))

        # #Obtaining extinction times
        for i in range(len(self.pop[:,1])):
            if (self.pop[:,1][i])<2:
                print(i)
                print('Predator')
                break

        for j in range(len(self.pop[:,0])):
            if (self.pop[:,0][j])<2:
                print(j)
                print('Prey')
                break

        fig = plt.figure()
        plt.subplot(211)
        plt.title('Predator-Prey Dynamics: High Capture Probability')
        plt.plot(self.pop[:,0],label='Prey')
        plt.plot(self.pop[:,1],label='Predator')
        #plt.ylim(ymax=50)
        plt.legend()
        plt.grid(True)
        plt.ylabel('Pop Density')
        plt.subplot(212)
        plt.plot(self.pop[:,2],label='k = ' + str(self.k[0]))
        plt.plot(self.pop[:,3],label='k = ' + str(self.k[1]))
        plt.grid(True)
        plt.ylabel('Indv Strategy')

        scale=3

        for i in np.arange(-scale,scale,.1):
            self.fast.append(fastG(self, i))
            self.slow.append(slowG(self, i))

        plt.plot(np.arange(-scale,scale,.1),self.slow,label='Prey')
        plt.plot(np.arange(-scale,scale,.1),self.fast,label='Predator')
        plt.plot(self.pop[self.time_G][2],slowG(self, self.pop[self.time_G][2]),marker='o',color='y')
        plt.plot(self.pop[self.time_G][3],fastG(self, self.pop[self.time_G][3]),marker='o',color='m')
        plt.title('Adaptive Landscape: Predator-Prey High Capture Probability')
        plt.xlabel('Evolutionary Strategy')
        plt.ylim(-.2,.1)
        plt.legend()
        plt.ylabel('Fitness')
        

        figDictionary = mpld3.fig_to_dict(fig)
        plt.close()
        return figDictionary