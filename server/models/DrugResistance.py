import numpy as np
from scipy.integrate import *
import matplotlib.pyplot as plt, mpld3
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

from pathlib import Path
import logging
from server.models.BaseModelsSchema import BaseModel, Schema, SchemaObject, SchemaObjectType

class DrugResistance(BaseModel):

    #set the default values
    time = 1500
    KM = 100
    r = [0.25,0.25]
    k = [0,0.2]  #evolvability: how fast cells can climb adaptive landscape

    uopt = 0
    uopt2 = 0 #the cancer cell strategy for which the drug is maximally effective

    s1 = 0.2 #Drug Dosage

    f1 = 1 #Drug Efficacy

    st = 2

    sk = 4 # squared value
    sa = 100 # squared value
    B = 2 # NOT squared value

    pop1 = 0
    pop2 = 10
    strat1 = 3
    strat2 = 3
    
    ModelSchema = Schema(
        'Drug Resistance Model',
        {
            'pop1': SchemaObject(0, 'pop1', 'Population 1 (pop1)'),
            'pop2': SchemaObject(10, 'pop2', 'Population 2 (pop2)'),
            'strat1': SchemaObject(3, 'strat1', 'Strategy 1 (strat1)'),
            'strat2': SchemaObject(3, 'strat2', 'Strategey 2 (strat2)'),
            'time': SchemaObject(time, 'time', 'Time'),
            'km': SchemaObject(100, 'km', 'km'),
            'r1': SchemaObject(0.25, 'r1', 'r1'),
            'r2': SchemaObject(0.25, 'r2', 'r2'),
            'k1': SchemaObject(0, 'k1','Population 1: how fast cells can climb adaptive landscape (k1)'),
            'k2': SchemaObject(0.2, 'k2','Population 2: how fast cells can climb adaptive landscape (k2)'),
            'uopt': SchemaObject(0, 'uopt', 'uopt'),
            'uopt2': SchemaObject(0, 'uopt2', 'The cancer cell strategy for which the drug is maximally effective (uopt2)'),
            's1': SchemaObject(0.2, 's1', 'Drug Dosage (s1)'),
            'f1': SchemaObject(1, 'f1', 'Drug Efficacy (f1)'),
            'st': SchemaObject(2, 'st', 'st') 
        })

    def __init__(self):
        
        super(DrugResistance, self).__init__(self)
        
    def __Run__(self):
        plt.switch_backend('Agg')
        global time
        global KM
        global r
        global k  #evolvability: how fast cells can climb adaptive landscape

        global uopt
        global uopt2 #the cancer cell strategy for which the drug is maximally effective

        global s1 #Drug Dosage

        global f1 #Drug Efficacy

        global st

        global sk # squared value
        global sa # squared value
        global B # NOT squared value

        global pop1
        global pop2
        global strat1
        global strat2

        global IC
        global intxv
        global pop
        global fast

        global xp
        global yp
        global Xp 
        global Yp

        logging.info("Running Drug Resistance")
        
        def evoLV(X, t):

            #Treatment administration

            if t>1000:
                s1=0.2
            else:
                s1=0

            x1 = X[0]
            x2 = X[1]
            u1 = X[2]
            u2 = X[3]

            K1 = KM * math.exp(-(u1 ** 2) / (2 * sk))
            K2 = KM * math.exp(-(u2 ** 2) / (2 * sk))

            a2 = 1 + math.exp(-(u1 - u2 + B) ** 2 / (2 * sa)) - math.exp(-(B ** 2 / (2 * sa)))
            a1 = 1 + math.exp(-(u2 - u1 + B) ** 2 / (2 * sa)) - math.exp(-(B ** 2 / (2 * sa)))

            dx1dt = x1 * (r[0]/K1 * (K1 - a2*x2 - x1))
            dx2dt = x2 * (r[1]/K2 * (K2 - a1*x1 - x2)-s1*f1*math.exp(-(u2-uopt)**2/(2*st)))

            dG1dv  = (-u1*r[0]*KM*(x1+a2*x2))/(K1*K1*sk)*math.exp(-(u1**2)/(2*sk)) + (r[0]*x2*(u1-u2+B))/(K1*sa)*math.exp(-((u1-u2+B)**2)/(2*sa))
            dG2dv  = (-u2*r[1]*KM*(a1*x1+x2))/(K2*K2*sk)*math.exp(-(u2**2)/(2*sk)) + (r[1]*x1*(u2-u1+B))/(K2*sa)*math.exp(-((u2-u1+B)**2)/(2*sa))+s1*f1*((u2-uopt)/st)*math.exp(-((u2-uopt)**2)/(2*st))

            dv1dt = k[0] * dG1dv
            dv2dt = k[1] * dG2dv

            dxvdt = np.array([dx1dt, dx2dt, dv1dt, dv2dt])
            return dxvdt

        def fastG(u2, time_G):
            if time_G>600:
                s1=0.2
            else:
                s1=0

            x1 = pop[time_G][0]
            x2 = pop[time_G][1]
            u1 = pop[time_G][2]
            a1 = 1 + math.exp(-(u2 - u1 + B) ** 2 / (2 * sa)) - math.exp(-(B ** 2 / (2 * sa)))
            K2 = KM * math.exp(-(u2 ** 2) / (2 * sk))
            Gfunc2 = (r[1] / K2 * (K2 - a1 * x1 - x2) - s1 * f1 * math.exp(-(u2 - uopt) ** 2 / (2 * st)))
            if Gfunc2 < -1: #truncating the negative G's for simplicity
                Gfunc2 = -1
            return Gfunc2

        time = int(self.Parameters['time'])
        KM = float(self.Parameters['km'])
        r = [float(self.Parameters['r1']),float(self.Parameters['r2'])]
        k = [float(self.Parameters['k1']),float(self.Parameters['k2'])]  #evolvability: how fast cells can climb adaptive landscape

        uopt = int(self.Parameters['uopt'])
        uopt2 = int(self.Parameters['uopt2']) #the cancer cell strategy for which the drug is maximally effective

        s1 = float(self.Parameters['s1']) #Drug Dosage

        f1 = float(self.Parameters['f1']) #Drug Efficacy

        st = float(self.Parameters['st'])

        sk = 4 # squared value
        sa = 100 # squared value
        B = 2 # NOT squared value

        pop1 = int(self.Parameters['pop1'])
        pop2 = int(self.Parameters['pop2'])
        strat1 = int(self.Parameters['strat1'])
        strat2 = int(self.Parameters['strat2'])

        IC = [pop1,pop2,strat1,strat2]
        intxv = np.array(IC)
        pop = odeint(evoLV, intxv, range(time+1))
        fast = []

        xp = np.arange(-5, 5, .1)
        yp = np.arange(0, time+1, 1)
        Xp, Yp = np.meshgrid(xp, yp)

        for i in yp:
            temp1 = []
            temp2 = []
            for j in xp:
                temp2.append(fastG(j,i))
            fast.append(temp2)
            temp1 = temp2 = []

        G_fast=[]
        for i in yp:
            j = pop[i][3]
            G_fast.append(fastG(j,i))

        fast = np.array(fast)

        if self.Is3d:
            fig = plt.figure()
            ax = plt.axes(projection='3d')
            ax.plot_surface(Xp, Yp, fast, cmap='Blues')
            ax.plot3D(pop[:,3],yp,G_fast,c='red')
            ax.set_xlabel('Evolutionary Strategy: v')
            ax.set_ylabel('Time')
            ax.set_zlabel('Fitness: G')
            ax.set_ylim(0,time)
            ax.set_zlim(-1,0.2)
            ax.view_init(35, 45)
            #ax.set_zlim(-1,0)
            plt.title('3D Adaptive Landscape: Treatment',pad=30)

        else:
            fig = plt.figure()
            plt.subplot(211)
            plt.title('Cancer Cell Dynamics: Treatment')
            #plt.plot(pop[:,0],label='k = ' + str(k[0]))
            plt.plot(pop[:,1],label='k = ' + str(k[1]))
            plt.ylim(ymax=200)
            plt.grid(True)
            plt.ylabel('Pop Size, x')
            plt.subplot(212)
            #plt.plot(pop[:,2],label='k = ' + str(k[0]))
            plt.plot(pop[:,3],label='k = ' + str(k[1]))
            plt.grid(True)
            plt.xlabel('Time')
            plt.ylabel('Indv Strategy, v')
        
        return self.Base.__Complete__(fig, plt)
        
        