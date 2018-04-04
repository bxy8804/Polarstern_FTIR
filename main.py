#!/usr/bin/python

from spectrum import spectrum

#a = spectrum(["/home/philippr/DISORT_4/disort4.0.98/Emission_20170715_0344.2.kali"])
a = spectrum(["/mnt/procdata/ftir/Equinox_Polarstern/PS106_timestamp/Emission_20170708_1600.0.kali"])#Stratus, clear sky?
#a.plotSpec(wnmin=1400, wnmax=700, ymin=0, ymax=1.2e2, offset=0.004, legend=["06-30-2017 16:40 UTC", "07-14-2017 23:58 UTC", "06-15-2017 07:00 UTC"] )
#a.plotSpec(wnmin=1400, wnmax=700, ymin=0, ymax=1.2e2, offset=0.000)
a.toText("Emission_20170618_0747.0.kali.dat", wnmin=898, wnmax=906, fit=1, fact=1000.0)
