import BaseModelsSchema as s
from typing import List

class TwoPrey(s.BaseModel):
    ModelSchema = s.Schema(
        '', 
        List[s.SchemaObject]
        [
            s.SchemaObject('', '', 0, False)
        ])

    def __init__(self):
        pass

# import numpy as np
# from scipy.integrate import *
# import matplotlib.pyplot as plt
# import math
# from mpl_toolkits.mplot3d import Axes3D
# from mpl_toolkits import mplot3d

# #Two Prey, One Predator System

# # Model Parameters
# pop1 = 10 #prey 1
# pop2 = 10 #prey 2
# pop3 = 10 #predator
# strat1 = 2.1
# strat2 = 2
# strat3 = 0

# time = 1000
# KM = 100
# r1 = 0.25
# r2 = 0.25
# r3 = 0.25
# c = 0.25
# k = [.5,.5,.5]

# IC = [pop1,pop2,pop3,strat1,strat2,strat3]

# sk = 2
# sa = 10
# sb = 10
# sr = 10

# bM = 0.5
# rM = 0.25

# def evoLV(X, t):

#     x1 = X[0]
#     x2 = X[1]
#     y = X[2]
#     u1 = X[3]
#     u2 = X[4]
#     mu = X[5]

#     K1 = KM*math.exp(-(u1**2)/sk)
#     K2 = KM*math.exp(-(u2**2)/sk)

#     b1 = bM*math.exp(-((u1-mu)**2)/sb)
#     b2 = bM*math.exp(-((u2-mu)**2)/sb)

#     r1 = rM#*math.exp(-(u1-mu)**2/sr)
#     r2 = rM#*math.exp(-(u2-mu)**2/sr)

#     a1 = math.exp(-(u1-u2)**2/sa)
#     a2 = math.exp(-(u2-u1)**2/sa)

#     dx1dt = x1 * (r1/K1*(K1-x1-a1*x2)-b1*y)
#     dx2dt = x2 * (r2/K2*(K2-x2-a2*x1)-b2*y)
#     dydt = y * (r3*(1-(y/(c*(b1*x1+b2*x2)))))

#     dK1dv = (-2*u1*KM/sk)*math.exp(-(u1**2)/sk)
#     dK2dv = (-2*u2*KM/sk)*math.exp(-(u2**2)/sk)

#     db1dv = (-2*bM*(u1-mu)/sb)*math.exp(-((u1-mu)**2)/sb)
#     db2dv = (-2*bM*(u2-mu)/sb)*math.exp(-((u2-mu)**2)/sb)

#     db3dv = (-2*bM*(mu-u1)/sb)*math.exp(-((mu-u1)**2)/sb)
#     db4dv = (-2*bM*(mu-u2)/sb)*math.exp(-((mu-u2)**2)/sb)

#     da1dv = (-2*(u1-u2)/sa)*math.exp(-((u1-u2)**2)/sa)
#     da2dv = (-2*(u2-u1)/sa)*math.exp(-((u2-u1)**2)/sa)

#     dr1dv = 0#(-2*rM*(u1-mu)/sr)*math.exp(-((u1-mu)**2)/sr)
#     dr2dv = 0#(-2*rM*(u2-mu)/sr)*math.exp(-((u2-mu)**2)/sr)

#     dG1dv = r1/K1*(dK1dv-da1dv*x2)+(K1-x1-a1*x2)/(K1**2)*(K1*dr1dv-r1*dK1dv)-y*db1dv
#     dG2dv = r2/K2*(dK2dv-da2dv*x1)+(K2-x2-a2*x1)/(K2**2)*(K2*dr2dv-r2*dK2dv)-y*db2dv
#     dG3dv = (r3*y/c)*(x1*db3dv+x2*db4dv)/((b1*x1+b2*x2)**2)

#     du1dt = k[0] * dG1dv
#     du2dt = k[1] * dG2dv
#     dmudt = k[2] * dG3dv

#     dxvdt = np.array([dx1dt,dx2dt,dydt, du1dt,du2dt, dmudt])
#     return dxvdt

# intxv = np.array(IC)
# pop = odeint(evoLV, intxv, range(time+1))

# print ('Population Prey1: %f' %pop[time][0])
# print ('Strategy Prey1: %f' %pop[time][3])

# print ('Population Prey2: %f' %pop[time][1])
# print ('Strategy Prey2: %f' %pop[time][4])

# print ('Population Predator: %f' %pop[time][2])
# print ('Strategy Predator: %f' %pop[time][5])

# plt.figure()
# plt.subplot(211)
# plt.title('Predator-Prey Dynamics: Speciation')
# plt.plot(pop[:,0],label='Prey 1')
# plt.plot(pop[:,1],label='Prey 2')
# plt.plot(pop[:,2],label='Predator')
# plt.legend()
# #plt.ylim(ymax=50)
# plt.grid(True)
# plt.ylabel('Pop Density')
# plt.subplot(212)
# plt.plot(pop[:,3],label='k = ' + str(k[0]))
# plt.plot(pop[:,4],label='k = ' + str(k[1]))
# plt.plot(pop[:,5],label='k = ' + str(k[2]))
# plt.grid(True)
# plt.ylabel('Indv Strategy')
# plt.show()

# time_G = 1000

# prey1 = []
# prey2 = []
# pred = []

# def prey1G(u1):
#     x1 = pop[time_G][0]
#     x2 = pop[time_G][1]
#     y = pop[time_G][2]
#     u2 = pop[time_G][4]
#     mu = pop[time_G][5]
#     r1 = rM#*math.exp(-(u1-mu)**2/sr)
#     a1 = math.exp(-(u1-u2)**2/sa)
#     b1 = bM*math.exp(-((u1-mu)**2)/sb)
#     K1 = KM*math.exp(-(u1**2)/sk)
#     prey1 = r1/K1*(K1-x1-a1*x2)-b1*y
#     return prey1

# def prey2G(u2):
#     x1 = pop[time_G][0]
#     x2 = pop[time_G][1]
#     y = pop[time_G][2]
#     u1 = pop[time_G][3]
#     mu = pop[time_G][5]
#     r2 = rM#*math.exp(-(u2-mu)**2/sr)
#     a2 = math.exp(-(u2-u1)**2/sa)
#     b2 = bM*math.exp(-((u2-mu)**2)/sb)
#     K2 = KM * math.exp(-(u2 ** 2) / sk)
#     prey2 = r2/K2*(K2-x2-a2*x1)-b2*y
#     return prey2

# def predG(mu):
#     x1 = pop[time_G][0]
#     x2 = pop[time_G][1]
#     y = pop[time_G][2]
#     u1 = pop[time_G][3]
#     u2 = pop[time_G][4]
#     b1 = bM*math.exp(-((u1-mu)**2)/sb)
#     b2 = bM*math.exp(-((u2-mu)**2)/sb)
#     pred = r3*(1-(y/(c*(b1*x1+b2*x2))))
#     return pred

# scale=2.5

# for i in np.arange(-scale,scale,.1):
#     prey1.append(prey1G(i))
#     prey2.append(prey2G(i))
#     pred.append(predG(i))

# plt.plot(np.arange(-scale,scale,.1),prey1,label='Prey 1')
# plt.plot(np.arange(-scale,scale,.1),prey2,label='Prey 2')
# plt.plot(np.arange(-scale,scale,.1),pred,label='Predator')
# plt.plot(pop[time_G][3],prey1G(pop[time_G][3]),marker='o',color='purple')
# plt.plot(pop[time_G][4],prey2G(pop[time_G][4]),marker='o',color='red')
# plt.plot(pop[time_G][5],predG(pop[time_G][5]),marker='o',color='darkgreen')
# plt.title('Adaptive Landscape: Predator-Prey Speciation')
# plt.xlabel('Evolutionary Strategy: v')
# plt.legend()
# plt.ylim(-.06,.005)
# plt.ylabel('Fitness: G')
# plt.show()