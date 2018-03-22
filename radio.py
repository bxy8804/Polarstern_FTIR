#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import datetime as dt
import numpy as np

class radiosonde:
    def __init__(self, filename):
        self.__names = []
        self.__fname = filename
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

    def writeToFile(self, filename, column):
        '''
        Filename ist der Name der Datei, in welche geschrieben werden soll. Column sind die Spalten, welche geschrieben werden sollen (Liste). Zum Gucken, welche
        Größe zu welcher Column gehört, showHeader() aufrufen
        '''
        
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
        fs = 30
        ls = 30
        plt.figure()
        plt.plot(self.__columns[columnX], self.__columns[columnY], lw=2)
        plt.ylabel(self.__names[columnY], fontsize=fs)
        plt.xlabel(self.__names[columnX], fontsize=fs)
        plt.tick_params(labelsize=ls)
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
        
    def interpolateSFIT(self):

        f = open("reference.prf", "r")
        cont = f.readlines()
        f.close()

        altitudes = []
        temperatures = []
        pressure = []
        
        #Depending on the shape of reference.prf
        
        #Hier müssen später die Werte ausgetauscht werden und dann in die neue reference-Datei geschrieben werden
        raw_alt = cont[2:11]
        raw_temp = cont[22:31]
        raw_pres = cont[12:21]
        
        for element in raw_alt:
            for element2 in element.split(" "):
                try:
                    altitudes.append(float(element2)*1000)
                except:
                    pass

        for element in raw_pres:
            for element2 in element.split(" "):
                try:
                    pressure.append(float(element2))
                except:
                    pass
        
        for element in raw_temp:
            for element2 in element.split(" "):
                try:
                    temperatures.append(float(element2)-273.15)
                except:
                    pass
                

        temperatureRadio = list(reversed(self.__columns[3]))
        altitudeRadio = list(reversed(self.__columns[2]))
        
        temperatureRadioNew = []
            
        #print(temperatures)
        #print(temperatureRadio)
        
        print(altitudes)
        print(altitudeRadio)
            
        for element in altitudes:
#                #print(element)
            for i in range(len(temperatureRadio)):
                if(altitudeRadio[i] < (element + 20) and altitudeRadio[i] > (element - 20)):
                    temperatureRadioNew.append(temperatureRadio[i])
                    break
                #elif(element > 20500):
                #    temperatureRadioNew.append(temperaturesReversed[counter])
                #    break
                #counter = counter + 1
#
#        reversedTemperatureRadioNew = []
#        for element in reversed(temperatureRadioNew):
#            reversedTemperatureRadioNew.append(element)
#
#        for i in range(0, len(reversedTemperatureRadioNew), 5):
#            try:
#                print("  {:.4E}   {:.4E}   {:.4E}   {:.4E}   {:.4E}".format(float(reversedTemperatureRadioNew[i])+273.15, \
#                                                                            float(reversedTemperatureRadioNew[i+1])+273.15, \
#                                                                            float(reversedTemperatureRadioNew[i+2])+273.15, \
#                                                                            float(reversedTemperatureRadioNew[i+3])+273.15, \
#                                                                            float(reversedTemperatureRadioNew[i+4])+273.15))
#            except:
#                print("  {:.4E}".format(float(reversedTemperatureRadioNew[i])+273.15))

if __name__ == "__main__":
    filename = "Radiosonde/PS170630.w11"
    x = radiosonde(filename)
    x.plot(3,2, xmin=-75, xmax=10, ymin=0, ymax=25000)
    #x.showHeader()
    #x.interpolateSFIT()
