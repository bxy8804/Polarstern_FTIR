#!/usr/bin/python2

import mpl_toolkits.basemap as bm
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import numpy as np
import os
import csv
import datetime as dt

ls=20

tro = [18.93, 69.66]
bhv = [8.60, 53.50]
lby = [15.63, 78.22]

path1 = "DSHIP_IFS66"
path2 = "DSHIP_EQX55"
path3 = "ClearSky"

absorption = os.listdir(path1)
emission = os.listdir(path2)

for i in range(len(absorption)):
    absorption[i] = "{}/{}".format(path1, absorption[i])

for i in range(len(emission)):
    emission[i] = "{}/{}".format(path2, emission[i])

def stereographic(lat, lon, time):
    plt.figure()
    
    mapPlot = bm.Basemap(projection='npstere', boundinglat=10, lon_0=0, resolution='i')
    mapPlot.drawcoastlines()
    mapPlot.fillcontinents(color='coral', lake_color='aqua')
    mapPlot.drawparallels(np.arange(-80., 81., 20.))
    mapPlot.drawmeridians(np.arange(-180., 181., 20.))
    mapPlot.drawmapboundary(fill_color='aqua')
    
    #mapPlot.plot(bhv[0], bhv[1], 'go', latlon=True)
    #mapPlot.plot(tro[0], tro[1], 'go', latlon=True)
    #mapPlot.plot(lby[0], lby[1], 'go', latlon=True)

    for i in range(len(lon)):
        if(time[i].month == 5):
            colour = "bo"
            first = mapPlot.plot(lon[i], lat[i], colour, latlon=True, mew=0.2, markersize=10)
        elif(time[i].month == 6):
            colour = "go"
            second = mapPlot.plot(lon[i], lat[i], colour, latlon=True, mew=0.2, markersize=10)
        elif(time[i].month == 7):
            colour = "yo"
            third = mapPlot.plot(lon[i], lat[i], colour, latlon=True, mew=0.2, markersize=10)
        elif(time[i].month == 8):
            colour = "co"
            fourth = mapPlot.plot(lon[i], lat[i], colour, latlon=True, mew=0.2, markersize=10)

    #plt.legend([first, second, third, fourth], ["07-02", "07-03", "07-14", "07-15"])
    #plt.legend(handler_map={first: HandlerLine2D(numpoints=1)}, fontsize=30)

    plt.show()
    plt.close()

def read(files):
    lon = []
    lat = []
    time = []
    ceiling = []
    for element in files:
        f = open(element, "r")
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            try:
                time.append(dt.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"))
                lon.append(float(row[1]))
                lat.append(float(row[2]))
                ceiling.append(float(row[7]))
            except:
                print(row)
                pass

    return lon, lat, time, ceiling
                
if __name__ == '__main__':
    #print(emission)
    lon, lat, time, ceiling = read(absorption)
    stereographic(lat, lon, time)
    #plt.figure()
    #line1, = plt.plot(time, lat, "o", markersize=20, linewidth=5, label="Latitudinal position of Polarstern")
    #plt.xlim([dt.datetime(2017,7,1,0,0), dt.datetime(2017,7,16,0,0)])
    #plt.ylim([79, 83])
    #plt.xlabel("Date", fontsize=30)
    #plt.ylabel(r"Latitude $(^{\circ})$", fontsize=30)
    #plt.grid(True)
    #plt.legend(handler_map={line1: HandlerLine2D(numpoints=1)}, fontsize=30)
    #plt.tick_params(axis='both', labelsize=ls)
    #print(ceiling)
    #x = np.loadtxt("ceiling.txt")
    #n, bins, sd = plt.hist(x, bins=[-1000+i*500 for i in range(103)], normed=100)
    #print(n)
    #print(bins)
    #plt.xlim([-1500, 55000])
    #plt.tick_params(axis='both', labelsize=30)
    #plt.xlabel(r"Ceiling $(\mathrm{ft})$", fontsize=30)
    #plt.ylabel(r"Occurence", fontsize=30)
    #plt.show()
    #plt.close()
