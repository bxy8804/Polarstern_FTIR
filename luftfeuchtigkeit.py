#!/usr/bin/python3

import numpy as np

Rw = 461.52

def magnusformel(temp):
    if(temp >= 0):
        c1 = 17.08085
        c2 = 243.175
    else:
        c1 = 17.84362
        c2 = 272.62
    E0 = 610.78
        
    return E0 * np.exp(c1 * temp / (c2 + temp))
        
def wassergehalt(rH, temp):
    return 1000*(magnusformel(temp) * rH) / (Rw * (temp + 273.15))