# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 15:54:21 2017

@author: philippr
"""

import csv
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as bm
import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime as dt
import misc

class report:
    
    def __init__(self, reports):
        self.__reports = reports
        
    def read(files):
    '''
    Einlesen der Messprotokolle
    '''
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
        
    def stereographic(lat, lon, time):
    plt.figure()
    
    mapPlot = bm.Basemap(projection='npstere', boundinglat=10, lon_0=0, resolution='i')
    mapPlot.drawcoastlines()
    mapPlot.fillcontinents(color='coral', lake_color='aqua')
    mapPlot.drawparallels(np.arange(-80., 81., 20.))
    mapPlot.drawmeridians(np.arange(-180., 181., 20.))
    mapPlot.drawmapboundary(fill_color='aqua')
    
    mapPlot.plot(misc.bhv[0], misc.bhv[1], 'go', latlon=True)
    mapPlot.plot(misc.tro[0], misc.tro[1], 'go', latlon=True)
    mapPlot.plot(misc.lby[0], misc.lby[1], 'go', latlon=True)

    for i in range(len(lon)):
        if(time[i].month == 5):
            colour = "bo"
            mapPlot.plot(lon[i], lat[i], colour, latlon=True, mew=0.2, markersize=misc.ms)
        elif(time[i].month == 6):
            colour = "go"
            mapPlot.plot(lon[i], lat[i], colour, latlon=True, mew=0.2, markersize=misc.ms)
        elif(time[i].month == 7):
            colour = "yo"
            mapPlot.plot(lon[i], lat[i], colour, latlon=True, mew=0.2, markersize=misc.ms)
        elif(time[i].month == 8):
            colour = "co"
            mapPlot.plot(lon[i], lat[i], colour, latlon=True, mew=0.2, markersize=misc.ms)

    plt.show()
    plt.close()
