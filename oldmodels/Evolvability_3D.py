import numpy as np
from scipy.integrate import *
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

#Code for Evolvability Model

# Model Parameters

#Used for evolutionary tracking
'''
g = np.random.rand(1001)
g1 = []
for i in range(len(g)):
    if (i%5==0):
        g1.append(g[i]*7)
    else:
        g1.append(g[i]*-7)
'''

pop1 = 10 #initial population density: species 1
pop2 = 10 #initial population density: species 2
strat1 = .5 #initial strategy: species 1
strat2 = .5 #initial strategy: species 2

time = 1000
KM = 100
d = [0.05,0.05]
r = [0.25,0.25]
k = [.2,.5]  # evolvability: how fast the species scale the adaptive landscape

k_curr = [k[0]]
r_curr = [r[0]]
d_curr = [d[0]]

IC = [pop1,pop2,strat1,strat2]

sk = 12.5 # squared value
sa = 2 #
B = 0 # NOT squared value

def evoLV(X, t):
    global k_curr
    global r_curr

    gamma = 0 #g1[int(t)]

#Evolutionary Rescue
    '''if t>4500:
        gamma = 0
    elif t>3900:
        gamma = -4.5
    elif t>3200:
        gamma = 0
    elif t>2500:
        gamma = -4.5
    elif t>1700: #1500
        gamma = 0
    elif t>800:
        gamma = -4.5
    else:
        gamma = 0'''

    '''if t>700:
        gamma = -4
    else:
        gamma = 0'''

#Sinusoidally changing environment
    #gamma = np.sin(t/50)

    x1 = X[0]
    x2 = X[1]
    u1 = X[2]
    u2 = X[3]

    K1 = KM * math.exp(-((u1 - gamma) ** 2) / (2 * sk))
    K2 = KM * math.exp(-((u2 - gamma) ** 2) / (2 * sk))

    a2 = 1 + math.exp(-(u1 - u2 + B) ** 2 / (2 * sa)) - math.exp(-(B ** 2 / (2 * sa)))
    a1 = 1 + math.exp(-(u2 - u1 + B) ** 2 / (2 * sa)) - math.exp(-(B ** 2 / (2 * sa)))

    dx1dt = x1 * (r[0]/K1 * (K1 - a2*x2 - x1) - d[0]*k[0])
    dx2dt = x2 * (r[1]/K2 * (K2 - a1*x1 - x2) - d[1]*k[1])

    dG1dv = (-(u1-gamma)*r[0]*KM*(x1+a2*x2))/(K1*K1*sk)*math.exp(-((u1-gamma)**2)/(2*sk)) + (r[0]*x2*(u1-u2+B))/(K1*sa)*math.exp(-((u1-u2+B)**2)/(2*sa))
    dG2dv = (-(u2-gamma)*r[1]*KM*(a1*x1+x2))/(K2*K2*sk)*math.exp(-((u2-gamma)**2)/(2*sk)) + (r[1]*x1*(u2-u1+B))/(K2*sa)*math.exp(-((u2-u1+B)**2)/(2*sa))

    dv1dt = k[0] * dG1dv
    dv2dt = k[1] * dG2dv

    dxvdt = np.array([dx1dt, dx2dt, dv1dt, dv2dt])
    return dxvdt

intxv = np.array(IC)
pop = odeint(evoLV, intxv, range(time+1))


#Plotting Adaptive Landscape: 3-Dimensional Landscape
gamma = 0
fast = []
slow = []

def fastG(u2, time_G):

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

    x1 = pop[time_G][0]
    x2 = pop[time_G][1]
    u1 = pop[time_G][2]
    a1 = 1 + math.exp(-(u2 - u1 + B) ** 2 / (2 * sa)) - math.exp(-(B ** 2 / (2 * sa)))
    K2 = KM * math.exp(-((u2 - gamma) ** 2) / (2 * sk))
    Gfunc2 = r[1] / K2 * (K2 - a1 * x1 - x2) - d[1] * k[1]
    if Gfunc2<-1:
        Gfunc2=-1
    return Gfunc2

def slowG(u1, time_G):
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

    x1 = pop[time_G][0]
    x2 = pop[time_G][1]
    u2 = pop[time_G][3]
    a2 = 1 + math.exp(-(u1 - u2 + B) ** 2 / (2 * sa)) - math.exp(-(B ** 2 / (2 * sa)))
    K1 = KM * math.exp(-((u1 - gamma) ** 2) / (2 * sk))
    Gfunc1 = r[0] / K1 * (K1 - a2 * x2 - x1) - d[0] * k[0]
    if Gfunc1<-1:
        Gfunc1 = -1
    return Gfunc1

xp = np.arange(-5, 5, .1)
yp = np.arange(0, 1001, 1)
Xp, Yp = np.meshgrid(xp, yp)

for i in yp:
    temp1 = []
    temp2 = []
    for j in xp:
        temp1.append(slowG(j,i))
        temp2.append(fastG(j,i))
    slow.append(temp1)
    fast.append(temp2)
    temp1 = temp2 = []

G_fast=[]
G_slow=[]
for i in yp:
    j = pop[i][3]
    G_fast.append(fastG(j,i))

for i in yp:
    j = pop[i][2]
    G_slow.append(slowG(j,i))

slow = np.array(slow)
fast = np.array(fast)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(Xp, Yp, slow, cmap='Blues')
ax.plot_surface(Xp, Yp, fast, cmap='Oranges')
ax.plot3D(pop[:,3],yp,G_fast,c='greenyellow') #fast
ax.plot3D(pop[:,2],yp,G_slow,c='c') #slow
ax.set_xlabel('Evolutionary Strategy: v')
ax.set_ylabel('Time')
ax.set_zlabel('Fitness: G')
#ax.set_zlim(-1,0.2)
ax.view_init(35, 45)
plt.title('Adaptive Landscape: No Aggressiveness Close',pad=30)
plt.show()


print ('Equilibrium x1: %f' %pop[time][0])
print ('Equilibrium u1: %f' %pop[time][2])

print ('Equilibrium x2: %f' %pop[time][1])
print ('Equilibrium u2: %f' %pop[time][3])

#Obtaining extinction times
for i in range(len(pop[:,1])):
    if (pop[:,1][i])<2:
        print(i)
        print('Fast')
        break


for j in range(len(pop[:,0])):
    if (pop[:,0][j])<2:
        print(j)
        print('Slow')
        break

plt.figure()
plt.subplot(211)
plt.title('No Aggressiveness: Close to Strategy Equilibrium')
plt.plot(pop[:,0],label='k = ' + str(k[0]))
plt.plot(pop[:,1],label='k = ' + str(k[1]))
plt.ylim(ymax=200)
plt.grid(True)
plt.ylabel('Pop Size, x')
plt.subplot(212)
plt.plot(pop[:,2],label='k = ' + str(k[0]))
plt.plot(pop[:,3],label='k = ' + str(k[1]))
plt.grid(True)
plt.ylabel('Indv Strategy, v')
plt.show()