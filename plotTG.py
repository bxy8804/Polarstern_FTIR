#!/usr/bin/python2

import os
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

TG = "H2O"
TG2 = "O3"
TG3 = "N2O"
TG4 = "CO2"
TG5 = "CH4"
fs = 30
ls = 30

time1 = []
time2 = []
time3 = []
time4 = []
time5 = []
column1 = []
column2 = []
column3 = []
column4 = []
column5 = []

year = 2017
month = 7
day = 3

#Search for all files named "summary"
folder = os.listdir(".")

for element in folder:
    if "Emission" in element:
        try:
            path = "./{}".format(element)
            #print
            #print(path)
            files = os.listdir(path)
            for f in files:
                #print(f)
                if f == "summary":
                    #Read the total column of a trace gas
                    g = open("{}/{}".format(path, f))
                    cont = g.readlines()
                    for element2 in cont:
                        if TG in element2:
                            x = element.split("_")[2][0:4]
                            if(int(x[0:2]) > 10):
                                if(TG in element2):
                                    time1.append(x)
                                    column1.append(float(element2.split(" ")[-1])*1e4)
                        elif TG2 in element2:
                            x = element.split("_")[2][0:4]
                            if(int(x[0:2]) > 10):
                                if(TG2 in element2):
                                    time2.append(x)
                                    column2.append(float(element2.split(" ")[-1])*1e4)
                        elif TG3 in element2:
                            x = element.split("_")[2][0:4]
                            if(int(x[0:2]) > 10):
                                if(TG3 in element2):
                                    time3.append(x)
                                    column3.append(float(element2.split(" ")[-1])*1e4)
                        elif TG4 in element2:
                            x = element.split("_")[2][0:4]
                            if(int(x[0:2]) > 10):
                                if(TG4 in element2):
                                    time4.append(x)
                                    column4.append(float(element2.split(" ")[-1])*1e4)
                        elif TG5 in element2:
                            x = element.split("_")[2][0:4]
                            if(int(x[0:2]) > 10):
                                if(TG5 in element2):
                                    time5.append(x)
                                    column5.append(float(element2.split(" ")[-1])*1e4)
        except:
            pass

plt.figure()
plt.semilogy(time1, column1, ".", markersize=ls/2, label=r"$\mathrm{H_2O}$")
plt.semilogy(time2, column2, ".", markersize=ls/2, label=r"$\mathrm{O_3}$")
plt.semilogy(time3, column3, ".", markersize=ls/2, label=r"$\mathrm{N_2O}$")
plt.semilogy(time4, column4, ".", markersize=ls/2, label=r"$\mathrm{CO_2}$")
plt.semilogy(time5, column5, ".", markersize=ls/2, label=r"$\mathrm{CH_4}$")
plt.xlabel("Time (UTC)", fontsize=fs)
if(TG != "O3"):
    plt.ylabel(r"Total column $(\mathrm{molecules} \cdot \mathrm{m^{-2}})$", fontsize=fs)
else:
    plt.ylabel(r"Total column (DU)", fontsize=fs)
plt.grid(True)
plt.legend(fontsize=fs)
plt.tick_params(axis='both', labelsize=ls)
plt.show()
plt.close()
