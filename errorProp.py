#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
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

def interpolateLin(xAxis, yAxis, xValue):
    for i in range(len(xAxis)):
        if(xValue > xAxis[i] and xValue < xAxis[i+1]):
            a = (yAxis[i+1] - yAxis[i]) / (xAxis[i+1] - xAxis[i])
            b = yAxis[i] - a * xAxis[i]
            return a * xValue + b

if __name__ == "__main__":
    deltaSC = 0.008
    deltaSA = 0.008
    deltaSH = 0.01
    deltaT = 0.2
    fMin = 700
    fMax = 1300
    
    #Einlesen des Spektrums des kalten Schwarzkoerpers (gemessen)
    f = open("/home/philipp/Documents/PhD/BB20.DPT", "r")#S_C
    cont = f.readlines()
    f.close()
    
    wavenumberSC = []
    intensitySC = []
    
    i = 0
    for line in cont:
        if(float(line.split(" ")[0]) >= 500 and float(line.split(" ")[0]) <= 2000.0 and i%2==0): 
            wavenumberSC.append(float(line.split(" ")[0]))
            intensitySC.append(float(line.split(" ")[-1]))
        i=i+1

    wavenumberSC = np.array(wavenumberSC)
    intensitySC = np.array(intensitySC)

    #Einlesen des Spektrums des warmen Schwarzkoerpers (gemesse9
    f = open("/home/philipp/Documents/PhD/BB100.DPT", "r")#S_H
    cont = f.readlines()
    f.close()
    
    wavenumberSH = []
    intensitySH = []
    
    i=0
    for line in cont:
        if(float(line.split(" ")[0]) >= 500 and float(line.split(" ")[0]) <= 2000.0 and i%2==0): 
            wavenumberSH.append(float(line.split(" ")[0]))
            intensitySH.append(float(line.split(" ")[-1]))
        i=i+1
       
    wavenumberSH = np.array(wavenumberSH)
    intensitySH = np.array(intensitySH)
    
    #Einlesen des zu kalibrierenden Spektrums
    f = open("/home/philipp/Documents/PhD/Emission.DPT", "r")#S_A
    cont = f.readlines()
    f.close()

    wavenumberSA = []
    intensitySA = []

    for line in cont:
        if(float(line.split(" ")[0]) >= 500 and float(line.split(" ")[0]) <= 2000.0): 
            wavenumberSA.append(float(line.split(" ")[0]))
            intensitySA.append(float(line.split(" ")[-1]))

    wavenumberSA = np.array(wavenumberSA)
    intensitySA = np.array(intensitySA)

    #Einlesen des kalibrierten Spektrums
    f = open("/home/philipp/Documents/PhD/Emission_neu_1448.DPT", "r")#P_A
    cont = f.readlines()
    f.close()
    
    wavenumberPA = []
    intensityPA = []
    
    i=0
    for line in cont:
        if(float(line.split(" ")[0]) >= 500 and float(line.split(" ")[0]) <= 2000.0 and i%2==0):
            wavenumberPA.append(float(line.split(" ")[0]))
            intensityPA.append(float(line.split(" ")[-1]))
        i=i+1
    
    wavenumberPA = np.array(wavenumberPA)
    intensityPA = np.array(intensityPA)

    #print(len(wavenumberSA), len(wavenumberPA))
#yInterpSC = []
#yInterpSA = []
#yInterpSH = []
#yInterpPA = []
#for i in range(fMin, fMax):
#    yInterpSC.append(interpolateLin(wavenumberSC, intensitySC, i))
#    yInterpSA.append(interpolateLin(wavenumberSA, intensitySA, i))
#    yInterpSH.append(interpolateLin(wavenumberSH, intensitySH, i))
#    yInterpPA.append(interpolateLin(wavenumberPA, intensityPA, i))

#yInterpSC = np.array(yInterpSC)
#yInterpSA = np.array(yInterpSA)
#yInterpSH = np.array(yInterpSH)
#yInterpPA = np.array(yInterpPA)

#Berechnung der Planck-Funktion fuer den warmen Schwarzkoerper
#bbHot = np.array([blackbodyStep(temp=thot, freq=i) for i in wavenumberPA])
#bbHotWN = np.array(wavenumberPA)

#Berechnung der Planck-Funktion fuer den kalten Schwarzkoerper
#bbCold = np.array([blackbodyStep(temp=tcold, freq=i) for i in wavenumberPA])
#bbColdWN = np.array(wavenumberPA)

#Berechnung der partiellen Ableitungen
#errdPAdPH = np.array([i for i in dPAdPH(S_A=intensitySA, S_C=intensitySC, S_H=intensitySH)])
#errdPAdPC = np.array([i for i in dPAdPC(S_A=intensitySA, S_C=intensitySC, S_H=intensitySH)])
#errdPAdSA = np.array([i for i in dPAdSA(P_H=bbHot, P_C=bbCold, S_H=intensitySH, S_C=intensitySC)])
#errdPAdSH = np.array([i for i in dPAdSH(S_A=intensitySA, P_H=bbHot, P_C=bbCold, S_H=intensitySH, S_C=intensitySC)])
#errdPAdSC = np.array([i for i in dPAdSC(S_A=intensitySA, P_H=bbHot, S_H=intensitySH, S_C=intensitySC, P_C=bbCold)])

#Berechnung der Fehler Planck-Funktionen (Funktionen des Temperaturfehlers des Schwarzkoerpers)
#deltaPC = np.array([dPdTStep(temp=tcold, freq=i)*deltaT for i in wavenumberPA])
#deltaPH = np.array([dPdTStep(temp=thot, freq=i)*deltaT for i in wavenumberPA])

#Berechnung der partiellen Fehler 
#errdPAdPH = errdPAdPH * deltaPH
#errdPAdPC = errdPAdPC * deltaPC
#errdPAdSA = errdPAdSA * deltaSA
#errdPAdSH = errdPAdSH * deltaSH
#errdPAdSC = errdPAdSC * deltaSC

#Berechnung des Fehlers des kalibrierten Spektrums
#errPAPos = errdPAdPH + errdPAdPC + errdPAdSA + errdPAdSH + errdPAdSC
#errPAPosFKT = intensityPA + errPAPos
#errPANegFKT = intensityPA - errPAPos 

#ratio = []
#for i in range(len(errPAPos)):
#    ratio.append(abs(errPAPos[i]/intensityPA[0]))
    
#plt.plot(wavenumberSC, intensitySC, color="red")
#plt.plot(wavenumberSH, intensitySH, color="red")
#plt.plot(wavenumberSA, intensitySA, color="blue")
#plt.plot(wavenumberPA, intensityPA, color="green")
#plt.plot(wavenumberPA, errPAPosFKT, color="red")
#plt.plot(wavenumberPA, errPANegFKT, color="red")
#plt.plot(wavenumberPA, ratio, color="black")
#plt.plot(wavenumberPA, errPAPos)
#plt.errorbar(wavenumberPA, intensityPA, yerr=errPAPos, linestyle="-", fmt='+', ecolor="black")
#plt.grid(True)
#plt.xlim([fMin, fMax])
#plt.ylim([-0.05,0.31])
#plt.ylim([0,1])
#plt.show()
