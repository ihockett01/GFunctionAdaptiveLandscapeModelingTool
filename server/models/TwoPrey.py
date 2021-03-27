import numpy as np
from scipy.integrate import *
import matplotlib.pyplot as plt, mpld3
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

from pathlib import Path
import logging
from server.models.BaseModelsSchema import BaseModel, Schema, SchemaObject, SchemaObjectType

class TwoPrey(BaseModel):

    ModelSchema = Schema(
        'Two Prey Model',
        {
            'pop1': SchemaObject(10, 'pop1', 'Prey 1'),
            'pop2': SchemaObject(10, 'pop2', 'Prey 2'),
            'pop3': SchemaObject(10, 'pop3', 'Predetor'),
            'strat1': SchemaObject(2.1, 'strat1', 'Strategy 1'),
            'strat2': SchemaObject(2, 'strat2', 'Strategy 2'),
            'strat3': SchemaObject(0, 'strat3', 'Strategy 3'),
            'time': SchemaObject(1500, 'time', 'Time'),
            'time_G': SchemaObject(1000, 'time_G', 'time_G'),
            'km': SchemaObject(100, 'km', 'km'),
            'r1': SchemaObject(0.25, 'r1', 'r1'),
            'r2': SchemaObject(0.25, 'r2', 'r2'),
            'r3': SchemaObject(0.25, 'r3', 'r3'),
            'c': SchemaObject(0.25, 'c', 'c'),
            'k1': SchemaObject(0.5, 'k1', 'k1'),
            'k2': SchemaObject(0.5, 'k2', 'k2'),
            'k3': SchemaObject(0.5, 'k3', 'k3'),
            'bM': SchemaObject(0.5, 'bM', 'bM'),
            'rM': SchemaObject(0.25, 'rM', 'rM')
        })

    def __init__(self):
        super(TwoPrey, self).__init__(self)

    def __Run__(self):
        logging.info("Running Two Prey")
        def evoLV(X, t):

            x1 = X[0]
            x2 = X[1]
            y = X[2]
            u1 = X[3]
            u2 = X[4]
            mu = X[5]

            K1 = self.KM*math.exp(-(u1**2)/self.sk)
            K2 = self.KM*math.exp(-(u2**2)/self.sk)

            b1 = self.bM*math.exp(-((u1-mu)**2)/self.sb)
            b2 = self.bM*math.exp(-((u2-mu)**2)/self.sb)

            r1 = self.rM#*math.exp(-(u1-mu)**2/sr)
            r2 = self.rM#*math.exp(-(u2-mu)**2/sr)

            a1 = math.exp(-(u1-u2)**2/self.sa)
            a2 = math.exp(-(u2-u1)**2/self.sa)

            dx1dt = x1 * (r1/K1*(K1-x1-a1*x2)-b1*y)
            dx2dt = x2 * (r2/K2*(K2-x2-a2*x1)-b2*y)
            dydt = y * (self.r3*(1-(y/(self.c*(b1*x1+b2*x2)))))

            dK1dv = (-2*u1*self.KM/self.sk)*math.exp(-(u1**2)/self.sk)
            dK2dv = (-2*u2*self.KM/self.sk)*math.exp(-(u2**2)/self.sk)

            db1dv = (-2*self.bM*(u1-mu)/self.sb)*math.exp(-((u1-mu)**2)/self.sb)
            db2dv = (-2*self.bM*(u2-mu)/self.sb)*math.exp(-((u2-mu)**2)/self.sb)

            db3dv = (-2*self.bM*(mu-u1)/self.sb)*math.exp(-((mu-u1)**2)/self.sb)
            db4dv = (-2*self.bM*(mu-u2)/self.sb)*math.exp(-((mu-u2)**2)/self.sb)

            da1dv = (-2*(u1-u2)/self.sa)*math.exp(-((u1-u2)**2)/self.sa)
            da2dv = (-2*(u2-u1)/self.sa)*math.exp(-((u2-u1)**2)/self.sa)

            dr1dv = 0#(-2*rM*(u1-mu)/sr)*math.exp(-((u1-mu)**2)/sr)
            dr2dv = 0#(-2*rM*(u2-mu)/sr)*math.exp(-((u2-mu)**2)/sr)

            dG1dv = r1/K1*(dK1dv-da1dv*x2)+(K1-x1-a1*x2)/(K1**2)*(K1*dr1dv-r1*dK1dv)-y*db1dv
            dG2dv = r2/K2*(dK2dv-da2dv*x1)+(K2-x2-a2*x1)/(K2**2)*(K2*dr2dv-r2*dK2dv)-y*db2dv
            dG3dv = (self.r3*y/self.c)*(x1*db3dv+x2*db4dv)/((b1*x1+b2*x2)**2)

            du1dt = self.k[0] * dG1dv
            du2dt = self.k[1] * dG2dv
            dmudt = self.k[2] * dG3dv

            dxvdt = np.array([dx1dt,dx2dt,dydt, du1dt,du2dt, dmudt])
            return dxvdt

        def prey1G(self, u1):
            x1 = self.pop[self.time_G][0]
            x2 = self.pop[self.time_G][1]
            y = self.pop[self.time_G][2]
            u2 = self.pop[self.time_G][4]
            mu = self.pop[self.time_G][5]
            r1 = self.rM#*math.exp(-(u1-mu)**2/sr)
            a1 = math.exp(-(u1-u2)**2/self.sa)
            b1 = self.bM*math.exp(-((u1-mu)**2)/self.sb)
            K1 = self.KM*math.exp(-(u1**2)/self.sk)
            prey1 = r1/K1*(K1-x1-a1*x2)-b1*y
            return prey1

        def prey2G(self, u2):
            x1 = self.pop[self.time_G][0]
            x2 = self.pop[self.time_G][1]
            y = self.pop[self.time_G][2]
            u1 = self.pop[self.time_G][3]
            mu = self.pop[self.time_G][5]
            r2 = self.rM#*math.exp(-(u2-mu)**2/sr)
            a2 = math.exp(-(u2-u1)**2/self.sa)
            b2 = self.bM*math.exp(-((u2-mu)**2)/self.sb)
            K2 = self.KM * math.exp(-(u2 ** 2) / self.sk)
            prey2 = r2/K2*(K2-x2-a2*x1)-b2*y
            return prey2

        def predG(self, mu):
            x1 = self.pop[self.time_G][0]
            x2 = self.pop[self.time_G][1]
            y = self.pop[self.time_G][2]
            u1 = self.pop[self.time_G][3]
            u2 = self.pop[self.time_G][4]
            b1 = self.bM*math.exp(-((u1-mu)**2)/self.sb)
            b2 = self.bM*math.exp(-((u2-mu)**2)/self.sb)
            pred = self.r3*(1-(y/(self.c*(b1*x1+b2*x2))))
            return pred
        
        self.time_G = int(self.Parameters['time_G'])

        self.fast = []
        self.slow = []

        self.pop1 = float(self.Parameters['pop1'])
        self.pop2 = float(self.Parameters['pop2'])
        self.pop3 = float(self.Parameters['pop3'])
        self.strat1 = float(self.Parameters['strat1'])
        self.strat2 = float(self.Parameters['strat2'])
        self.strat3 = float(self.Parameters['strat3'])

        self.IC = [self.pop1,self.pop2,self.pop3,self.strat1,self.strat2,self.strat3]

        self.time = int(self.Parameters['time'])
        self.KM = float(self.Parameters['km'])
        self.r1 = float(self.Parameters['r1'])
        self.r2 = float(self.Parameters['r2'])
        self.r3 = float(self.Parameters['r3'])
        self.k = [float(self.Parameters['k1']),float(self.Parameters['k2']),float(self.Parameters['k3'])]

        self.sk = 2
        self.sa = 4
        self.sb = 10
        self.sr = 10

        self.bM = float(self.Parameters['bM'])
        self.rM = float(self.Parameters['rM'])

        self.c = float(self.Parameters['c'])

        self.intxv = np.array(self.IC)
        self.pop = odeint(evoLV, self.intxv, range(self.time+1))

        self.prey1 = []
        self.prey2 = []
        self.pred = []

        fig = plt.figure()
        plt.subplot(211)
        plt.title('Predator-Prey Dynamics: Speciation')
        plt.plot(self.pop[:,0],label='Prey 1')
        plt.plot(self.pop[:,1],label='Prey 2')
        plt.plot(self.pop[:,2],label='Predator')
        plt.legend()
        #plt.ylim(ymax=50)
        plt.grid(True)
        plt.ylabel('Pop Density')
        plt.subplot(212)
        plt.plot(self.pop[:,3],label='k = ' + str(self.k[0]))
        plt.plot(self.pop[:,4],label='k = ' + str(self.k[1]))
        plt.plot(self.pop[:,5],label='k = ' + str(self.k[2]))
        plt.grid(True)
        plt.ylabel('Indv Strategy')

        scale=2.5

        for i in np.arange(-scale,scale,.1):
            self.prey1.append(prey1G(self, i))
            self.prey2.append(prey2G(self, i))
            self.pred.append(predG(self, i))

        plt.plot(np.arange(-scale,scale,.1),self.prey1,label='Prey 1')
        plt.plot(np.arange(-scale,scale,.1),self.prey2,label='Prey 2')
        plt.plot(np.arange(-scale,scale,.1),self.pred,label='Predator')
        plt.plot(self.pop[self.time_G][3],prey1G(self, self.pop[self.time_G][3]),marker='o',color='purple')
        plt.plot(self.pop[self.time_G][4],prey2G(self, self.pop[self.time_G][4]),marker='o',color='red')
        plt.plot(self.pop[self.time_G][5],predG(self, self.pop[self.time_G][5]),marker='o',color='darkgreen')
        plt.title('Adaptive Landscape: Predator-Prey Speciation')
        plt.xlabel('Evolutionary Strategy: v')
        plt.legend()
        plt.ylim(-.06,.005)
        plt.ylabel('Fitness: G')

        figDictionary = mpld3.fig_to_dict(fig)
        plt.close()
        return figDictionary

