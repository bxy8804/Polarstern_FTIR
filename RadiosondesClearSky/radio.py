#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import datetime as dt
import numpy as np

class radiosonde:
    def __init__(self, filename):
        self.__names = []
        f = open(filename,"r")
        cont = f.readlines()
        f.close()

        #Nicht schoen
        #9: Pressure (hPa)
        #14: Time after launch (s)
        #15: Geopotential height (gmp)
        #16: Temperature (C)
        #17: Relative Humidity (%)
        #18: Horizontal wind direction (deg)
        #19: Horizontal wind speed (m/s)
        #72: NumberOfLevels LaunchTime(Decimal) Longitude(deg) Latitude(deg)
        #86: Werte Radiosonde
        headerNames = [9, 14, 15, 16, 17, 18, 19]
        for i in headerNames:
            self.__names.append(cont[i][:-2])

        line72 = []
        for i in cont[72].split(" "):
            if(i != ""):
                line72.append(i)
        
        date = cont[6].split(" ")
        time = line72[1]
        hour = np.trunc(float(time))
        minute = (float(time) - np.trunc(float(time))) * 60.0
        self.__starttime = dt.datetime(int(date[0]), int(date[1]), int(date[2]), int(hour), int(minute)) 

        self.__lon = float(line72[2])
        self.__lat = float(line72[3])

        self.__columns = [[] for i in range(len(headerNames))]
        x = []

        length = len(cont[86:])
        values = []
        for k in range(length):
            for i in cont[86+k].split(" "):
                if(i != ""):
                    x.append(i)
            values.append(x)
            x = []
            
        for j in range(len(headerNames)):
            for i in range(len(values)):
                self.__columns[j].append(float(values[i][j]))

        #for i in range(len(cont[0].split(" "))):
        #    for j in range(len(self.__columns)):              
        #        try:
        #            self.__columns[i].append(float(cont[j].split("\t")[i]))
        #        except:
        #            pass


    def writeToFile(self, filename, column):
        f = open(filename, "w")
        x = len(column)
        for j in range(x):
            f.write("{};".format(self.__names[j]))
        f.write("\n")
                    
        for i in range(len(self.__columns[column[0]])):
            for j in range(x):
                f.write("{};".format(self.__columns[column[j]][i]))
            f.write("\n")
        f.close()
        return

    def plot(self, columnX, columnY, xmin, xmax, ymin, ymax):
        plt.figure()
        plt.plot(self.__columns[columnX], self.__columns[columnY])
        plt.ylabel(self.__names[columnY])
        plt.xlabel(self.__names[columnX])
        plt.xlim([xmin, xmax])
        plt.ylim([ymin, ymax])
        plt.grid(True)
        plt.show()
        plt.close()

    def showHeader(self):
        for i in range(len(self.__names)):
            print("{}: {}".format(i, self.__names[i]))

    def getElement(self, column, element):
        return self.__columns[column][element]

    def getStarttime(self):
        return self.__starttime

    def returnTemp(self):
        return self.__columns[3]

    def returnAlt(self):
        return self.__columns[2]

    def returnPressure(self):
        return self.__columns[0]

if __name__ == "__main__":
    filename = "/media/philipp/Volume/Backup Polarstern/Messdaten/Radiosondenaufstiege/PS106_2/NILU_EDT/PS170705.w06"
    x = radiosonde(filename)
    x.writeToFile("/home/philipp/Documents/Polarstern/Python/Radiosonde/17_07_05.csv", [0,1,2,3])
    x.plot(3,2, xmin=-75, xmax=10, ymin=0, ymax=25000)
    x.showHeader()
    #print(x.getElement(0,-1))
    #print(x.getStarttime())
