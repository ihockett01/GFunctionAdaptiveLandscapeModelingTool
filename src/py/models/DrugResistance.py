import numpy as np
from scipy.integrate import *
import matplotlib.pyplot as plt, mpld3
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
from pathlib import Path
import BaseModel as bm

#Drug Resistance Model

class Model(bm.ModelSchema):

    # Model Parameters
    def __init__(self, pop1, pop2, strat1, strat2, outputPath):
        #Model constants
        self.outputPath = outputPath
        self.time = 1500
        self.KM = 100
        self.r = [0.25,0.25]
        self.k = [0,0.2]  #evolvability: how fast cells can climb adaptive landscape

        self.uopt = 0
        self.uopt2 = 0 #the cancer cell strategy for which the drug is maximally effective

        self.s1 = 0.2 #Drug Dosage

        self.f1=1 #Drug Efficacy

        self.st = 2

        self.sk = 4 # squared value
        self.sa = 100 # squared value
        self.B = 2 # NOT squared value

        def evoLV(X, t):

            #Treatment administration

            if t>1000:
                self.s1=0.2
            else:
                self.s1=0

            x1 = X[0]
            x2 = X[1]
            u1 = X[2]
            u2 = X[3]

            K1 = self.KM * math.exp(-(u1 ** 2) / (2 * self.sk))
            K2 = self.KM * math.exp(-(u2 ** 2) / (2 * self.sk))

            a2 = 1 + math.exp(-(u1 - u2 + self.B) ** 2 / (2 * self.sa)) - math.exp(-(self.B ** 2 / (2 * self.sa)))
            a1 = 1 + math.exp(-(u2 - u1 + self.B) ** 2 / (2 * self.sa)) - math.exp(-(self.B ** 2 / (2 * self.sa)))

            dx1dt = x1 * (self.r[0]/K1 * (K1 - a2*x2 - x1))
            dx2dt = x2 * (self.r[1]/K2 * (K2 - a1*x1 - x2)-self.s1*self.f1*math.exp(-(u2-self.uopt)**2/(2*self.st)))

            dG1dv  = (-u1*self.r[0]*self.KM*(x1+a2*x2))/(K1*K1*self.sk)*math.exp(-(u1**2)/(2*self.sk)) + (self.r[0]*x2*(u1-u2+self.B))/(K1*self.sa)*math.exp(-((u1-u2+self.B)**2)/(2*self.sa))
            dG2dv  = (-u2*self.r[1]*self.KM*(a1*x1+x2))/(K2*K2*self.sk)*math.exp(-(u2**2)/(2*self.sk)) + (self.r[1]*x1*(u2-u1+self.B))/(K2*self.sa)*math.exp(-((u2-u1+self.B)**2)/(2*self.sa))+self.s1*self.f1*((u2-self.uopt)/self.st)*math.exp(-((u2-self.uopt)**2)/(2*self.st))

            dv1dt = self.k[0] * dG1dv
            dv2dt = self.k[1] * dG2dv

            dxvdt = np.array([dx1dt, dx2dt, dv1dt, dv2dt])
            return dxvdt


        self.pop1 = pop1
        self.pop2 = pop2
        self.strat1 = strat1
        self.strat2 = strat2
        self.IC = [self.pop1,self.pop2,self.strat1,self.strat2]
        self.intxv = np.array(self.IC)
        self.pop = odeint(evoLV, self.intxv, range(self.time+1))
        self.fast = []

        
    #For simplicity, I've ignored the presence of the normal cells in this model

    def run(self):

        def fastG(u2, time_G):
            if time_G>600:
                self.s1=0.2
            else:
                self.s1=0

            x1 = self.pop[time_G][0]
            x2 = self.pop[time_G][1]
            u1 = self.pop[time_G][2]
            a1 = 1 + math.exp(-(u2 - u1 + self.B) ** 2 / (2 * self.sa)) - math.exp(-(self.B ** 2 / (2 * self.sa)))
            K2 = self.KM * math.exp(-(u2 ** 2) / (2 * self.sk))
            Gfunc2 = (self.r[1] / K2 * (K2 - a1 * x1 - x2) - self.s1 * self.f1 * math.exp(-(u2 - self.uopt) ** 2 / (2 * self.st)))
            if Gfunc2 < -1: #truncating the negative G's for simplicity
                Gfunc2 = -1
            return Gfunc2

        xp = np.arange(-5, 5, .1)
        yp = np.arange(0, self.time+1, 1)
        Xp, Yp = np.meshgrid(xp, yp)

        for i in yp:
            temp1 = []
            temp2 = []
            for j in xp:
                temp2.append(fastG(j,i))
            self.fast.append(temp2)
            temp1 = temp2 = []

        G_fast=[]
        for i in yp:
            j = self.pop[i][3]
            G_fast.append(fastG(j,i))

        fast = np.array(self.fast)

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.plot_surface(Xp, Yp, fast, cmap='Blues')
        ax.plot3D(self.pop[:,3],yp,G_fast,c='red')
        ax.set_xlabel('Evolutionary Strategy: v')
        ax.set_ylabel('Time')
        ax.set_zlabel('Fitness: G')
        ax.set_ylim(0,self.time)
        ax.set_zlim(-1,0.2)
        ax.view_init(35, 45)
        #ax.set_zlim(-1,0)
        plt.title('3D Adaptive Landscape: Treatment',pad=30)
        #plt.savefig('3DAdaptiveLandscapeTreatment.png', format='png')
        #plt.show()
        return mpld3.fig_to_html(fig)
        
        """ plt.figure()
        plt.subplot(211)
        plt.title('Cancer Cell Dynamics: Treatment')
        #plt.plot(pop[:,0],label='k = ' + str(k[0]))
        plt.plot(self.pop[:,1],label='k = ' + str(self.k[1]))
        plt.ylim(ymax=200)
        plt.grid(True)
        plt.ylabel('Pop Size, x')
        plt.subplot(212)
        #plt.plot(pop[:,2],label='k = ' + str(k[0]))
        plt.plot(self.pop[:,3],label='k = ' + str(self.k[1]))
        plt.grid(True)
        plt.xlabel('Time')
        plt.ylabel('Indv Strategy, v')
        #plt.savefig('CancerCellDynamicsTreatment.png', format='png')
        plt.show() """

        #return 'CancerCellDynamicsTreatment.png'
        #return plt

    