import numpy as np
from scipy.integrate import *
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

#Drug Resistance Model

# Model Parameters

#For simplicity, I've ignored the presence of the normal cells in this model

pop1 = 0 #initial population size: normal cell
pop2= 10 #initial population size: cancer cell
strat1 = 3 #initial strategy: normal
strat2 = 3 #initial strategy: cancer

time = 1500
KM = 100
r = [0.25,0.25]
k = [0,0.2]  #evolvability: how fast cells can climb adaptive landscape

uopt = 0
uopt2 = 0 #the cancer cell strategy for which the drug is maximally effective

s1 = 0.2 #Drug Dosage

f1=1 #Drug Efficacy

IC = [pop1,pop2,strat1,strat2]

st = 2

sk = 4 # squared value
sa = 100 # squared value
B = 2 # NOT squared value

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

intxv = np.array(IC)
pop = odeint(evoLV, intxv, range(time+1))

fast = []

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
plt.show()

# plt.figure()
# plt.subplot(211)
# plt.title('Cancer Cell Dynamics: Treatment')
# #plt.plot(pop[:,0],label='k = ' + str(k[0]))
# plt.plot(pop[:,1],label='k = ' + str(k[1]))
# plt.ylim(ymax=200)
# plt.grid(True)
# plt.ylabel('Pop Size, x')
# plt.subplot(212)
# #plt.plot(pop[:,2],label='k = ' + str(k[0]))
# plt.plot(pop[:,3],label='k = ' + str(k[1]))
# plt.grid(True)
# plt.xlabel('Time')
# plt.ylabel('Indv Strategy, v')
# plt.show()