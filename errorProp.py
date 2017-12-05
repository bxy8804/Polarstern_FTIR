#!/usr/bin/python3

import numpy as np

h = 6.626070040e-34#Js
c = 299792458#ms-1
k = 1.38064852e-23#JK-1

tcold = 283.15#K
thot = 373.15#K

def blackbody(temp=273.15, freqMin=1, freqMax=1000, step=1):#Use Opus Blackbody Function
    for i in range(freqMin,freqMax, step):
        yield ((2*10**8*h * c**2 * i**3)/(np.exp(100*i*h*c/(k*temp))-1))
        
def dPdT(temp=273.15, freqMin=1, freqMax=1000, step=1):
    for i in range(freqMin, freqMax, step):
        x1 = 2*10**10 * h**2 * c**3
        x2 = 100*h*c/(k*temp)
        x3 = k*temp**2
        yield np.abs(x1*i**4*np.exp(x2*i)/(x3 * (np.exp(x2*i)-1)**2))

def blackbodyStep(temp=273.15, freq=1):#Use Opus Blackbody Function
    if(freq == 0):
        return 0
    else:
        return ((2*10**8*h * c**2 * freq**3)/(np.exp(100*freq*h*c/(k*temp))-1))

def dPdTStep(temp=273.15, freq=1):
    x1 = 2*10**10 * h**2 * c**3
    x2 = 100*h*c/(k*temp)
    x3 = k*temp**2
    if(freq == 0):
        return 0
    else:
        return np.abs(x1*freq**4*np.exp(x2*freq)/(x3 * (np.exp(x2*freq)-1)**2))

def dPAdPH(S_A, S_C, S_H):
    for i in range(len(S_A)):
        if(S_H[i] == S_C[i]):
            print("hier")
        yield np.abs((S_A[i] - S_C[i]) / (S_H[i] - S_C[i]))

def dPAdPC(S_A, S_C, S_H):
    for i in range(len(S_A)):
        yield np.abs(1 + (S_C[i] - S_A[i]) / (S_H[i] - S_C[i]))

def dPAdSA(P_H, P_C, S_H, S_C):
    for i in range(len(S_H)):
        yield np.abs((P_H[i] - P_C[i]) / (S_H[i] - S_C[i]))

def dPAdSH(S_A, P_H, P_C, S_H, S_C):
    a = -S_A * P_H / (S_H - S_C)**2
    b = S_A * P_C / (S_H - S_C)**2
    c = S_C * P_H / (S_H - S_C)**2
    d = - S_C * P_C / (S_H - S_C)**2
    for i in range(len(S_A)):
        yield np.abs(a[i]+b[i]+c[i]+d[i])

def dPAdSC(S_A, P_H, S_H, S_C, P_C):
    a = S_A * P_H / (S_H - S_C)**2
    b = -S_A * P_C / (S_H - S_C)**2
    c = - P_H / (S_H - S_C)
    d = - S_C * P_H / (S_H - S_C)**2
    e = P_C / (S_H - S_C)
    f = S_C * P_C / (S_H - S_C)**2
    for i in range(len(S_A)):
        yield np.abs(a[i]+b[i]+c[i]+d[i]+e[i]+f[i])