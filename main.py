#!/usr/bin/python

import os
from spectrum import spectrum
    
path = "/home/philippr/testcali/calibrated"

spectra = os.listdir(path)

for i in range(len(spectra)):
    if(spectra[i] == "Emission_20170703_0939.0_95_12.5.kali"):
        plotting = "{}/{}".format(path, spectra[i])
    spectra[i] = "{}/{}".format(path, spectra[i])
    print(i, spectra[i])

a = spectrum([plotting])
a.plotSpec(wnmin=500, wnmax=2000, ymin=-0.0, ymax=0.1)
