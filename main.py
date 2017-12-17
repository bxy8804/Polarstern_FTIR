#!/usr/bin/python

import os
from spectrum import spectrum
    
path = "/home/philipp/Presentation_IUP/testcali/calibrated"
plotting = []
lgd = []
spectra = os.listdir(path)

for i in range(len(spectra)):
    #if(spectra[i] == "Emission_20170703_0939.0_96_13.kali"):
    #    plotting.append("{}/{}".format(path, spectra[i]))
    #    lgd.append("$T_{Hot} = 96\,\mathrm{K}$")
    if(spectra[i] == "Emission_20170703_0939.0_100_13.kali"):
        plotting.append("{}/{}".format(path, spectra[i]))
        lgd.append("$T_{Hot} = 100\,\mathrm{K}$")
    spectra[i] = "{}/{}".format(path, spectra[i])
    print(i, spectra[i])

a = spectrum(plotting)
a.plotSpec(wnmin=700, wnmax=1300, ymin=-0.01, ymax=0.05, legend=lgd)
