#!/usr/bin/python

'''
dship.py

Script for easy reading and searching the Polarstern dship files

@author: philipp richter <phi.richter@uni-bremen.de>
'''

import mpl_toolkits.basemap as bm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import datetime as dt
import numpy as np
import csv
import calendar as cal


fClasses = 2
alldata = 0
pitchroll = 1
both = 2

year = "17"
month = "07"
day = "24"

def degree2rad(degr):
    return degr * np.pi / 180.0

def getTimes(fname):
    times = []
    f = open(fname, "r")
    report = csv.reader(f, delimiter=",")
    for i in report:
        try:
            times.append(dt.datetime.strptime("{} {} {} {}".format(i[1], year, month, day), "%H:%M:%S %Y %m %d"))
        except:
            pass
    f.close()
    return times
        
class dship:
    
    def __init__(self, path, filename, startDate, endDate):
        '''
        Open the index file. This file contains the names all other DSHIP files
        '''
        self.__path = path
        f = open("{}/{}".format(path, filename), "r")
        cont = f.readlines()
        f.close()

        self.__files = [[],[]]
        self.__startDates = [[], []]
        self.__endDates = [[], []]
        self.__names = [[], []]
        self.__columns = [None, None]
        self.__opened = False
        self.__startDate = startDate
        self.__endDate = endDate
        self.__cache = []
        self.__header = []

        i = 0
        
        for element in cont:
            if("/" in element):
                self.__files[i].append(element[:-1])
                startDate = element.split("/")[0].split("-")[0].split("_")[1]
                endDate = element.split("/")[0].split("-")[1]

                startMonth = int(startDate[:2])
                startDay = int(startDate[2:])

                endMonth = int(endDate[:2])
                endDay = int(endDate[2:])

                self.__startDates[i].append(dt.datetime(2017, startMonth, startDay, 10, 0, 0))
                self.__endDates[i].append(dt.datetime(2017, endMonth, endDay, 10, 0, 0))
                
            elif("" in element):
                i = 1

        #Zum Erstellen der Namenslisten muss je eine Datei geoeffnet und die Header eingelesen werden
        for i in range(fClasses):
            f = open("{}/{}".format(self.__path, self.__files[i][0]))
            cont = f.readlines()
            f.close()
            self.__names[i] = cont[0].split("\t")

       
    def read(self):#Oha, das dauert ja ewig lang. Egal, geht ja nicht um Performance und das sind nunmal ewig viele Daten
        '''
        Opens the DSHIP files corresponding to the requested data and returns nothing.
       startDate and endDate must bei datetime-objects
        '''
        startIndex = 0
        endIndex = 0
        for element in self.__startDates[0]:
            if(self.__startDate > element):
                startIndex = startIndex + 1

        startIndex = startIndex - 1
        for element in self.__endDates[0]:
            if(self.__endDate > element):
                endIndex = endIndex + 1

        for i in range(startIndex, endIndex+1):
            try:
                f = open("{}/{}".format(self.__path, self.__files[0][i]))
                g = open("{}/{}".format(self.__path, self.__files[1][i]))
            except IndexError:
                break
            contAllData = f.readlines()
            contPitchRoll = g.readlines()
            f.close()
            g.close()

            if(i == startIndex):#Im ersten Schleifendurchlauf werden die Listen ordentlich initialisiert
                self.__columns[alldata] = [[] for g in range(len(contAllData))]
                self.__columns[pitchroll] = [[] for g in range(len(contPitchRoll))]

            for j in range(len(contAllData[0].split("\t"))):
                for k in range(len(contAllData)):
                    if(j == 0):#Hier steht immer das Datum. Sonst werde ich boese ;)
                        try:
                            date = contAllData[k].split("\t")[0].split(" ")[0]
                            time = contAllData[k].split("\t")[0].split(" ")[1]
                            
                            year = int(date.split("/")[0])
                            month = int(date.split("/")[1])
                            day = int(date.split("/")[2])
                            
                            hour = int(time.split(":")[0])
                            minute = int(time.split(":")[1])
                            second = int(time.split(":")[2])

                            self.__columns[alldata][j].append(dt.datetime(year, \
                                                             month, \
                                                             day, \
                                                             hour, \
                                                             minute, \
                                                             second))

                            date = contPitchRoll[k].split("\t")[0].split(" ")[0]
                            time = contPitchRoll[k].split("\t")[0].split(" ")[1]
                            
                            year = int(date.split("/")[0])
                            month = int(date.split("/")[1])
                            day = int(date.split("/")[2])
                            
                            hour = int(time.split(":")[0])
                            minute = int(time.split(":")[1])
                            second = int(time.split(":")[2])

                            self.__columns[pitchroll][j].append(dt.datetime(year, \
                                                             month, \
                                                             day, \
                                                             hour, \
                                                             minute, \
                                                             second))
                            

                        except:
                            #print(contAllData[k].split("\t")[0])
                            #print(contPitchRoll[k].split("\t")[0])
                            pass#Hier kommen die Headerzeilen hin
                    else:#Wenn also nicht grad die erste Spalte dran ist
                        try:
                            self.__columns[alldata][j].append(float(contAllData[k].split("\t")[j]))
                            self.__columns[pitchroll][j].append(float(contPitchRoll[k].split("\t")[j]))
                        except:#Falls hier wieder die doofen Header kommen
                            pass

        return
    
    def getCells(self, fC, header):
        '''
        Returns all data under the chosen headers between the chosen dates. Shape of the return value: dim[numberOfHeaders+1(datetime)][numberOfLines]
        '''
        self.__header = header
        self.__cache = [[] for i in range(len(header)+1)]
        for j in range(len(header)):
            for i in range(len(self.__columns[fC][0])):
                if(self.__startDate < self.__columns[fC][0][i] and self.__endDate > self.__columns[fC][0][i]):
                    self.__cache[j].append(self.__columns[fC][header[j]][i])
        #Add datetime
        for i in range(len(self.__columns[fC][0])):
                if(self.__startDate < self.__columns[fC][0][i] and self.__endDate > self.__columns[fC][0][i]):
                    self.__cache[j+1].append(self.__columns[fC][0][i])
        return self.__cache
        
    def showHeader(self):
        for j in range(fClasses):
            for i in range(len(self.__names[j])):
                print("{}: {}".format(i, self.__names[j][i]))
        return

    def printCells(self, fC, datetime):
        '''
        Search for the timestamp datetime in self.__cache and print the cells on the screen
        '''
        for i in range(len(self.__cache[-1])):
            if(datetime == self.__cache[-1][i]):
                for j in range(len(self.__cache)-1):#Last element of self.__cache is datetime
                    print("{}: {}".format(self.__names[fC][self.__header[j]], self.__cache[j][i]))
                    
    def writeCSV(self, fC, datetime, fname, epoch=True):
        f = open(fname, "w")
        head="date time;"
        column_Names = [self.__names[fC][i] for i in self.__header]
        for i in column_Names:
            head = head+"{};".format(i)
        f.write("{}\n".format(head))
        for element in datetime:
            #Convert time to seconds start at epoch
            cal.timegm(element.timetuple())
            for i in range(len(self.__cache[-1])-1):
                element2 = dt.datetime(element.year, \
                                       element.month, \
                                       element.day, \
                                       element.hour, \
                                       element.minute, \
                                       0)#element.second-element.second%10)
                if(element2 == self.__cache[-1][i]):
                    f.write("{};".format(element))
                    for j in range(len(self.__cache)-1):#Last element of self.__cache is datetime
                        f.write("{};".format(self.__cache[j][i]))
            f.write("\n")
        f.close()
        return

    def writeAll(self, fC, fname):
        f = open(fname, "w")
        head="date time;"
        column_Names = [self.__names[fC][i] for i in self.__header]
        for i in column_Names:
            head = head+"{};".format(i)
        f.write("{}\n".format(head))
        for element in datetime:
            #Convert time to seconds start at epoch
            cal.timegm(element.timetuple())
            for i in range(len(self.__cache[-1])-1):
                element2 = dt.datetime(element.year, \
                                       element.month, \
                                       element.day, \
                                       element.hour, \
                                       element.minute, \
                                       0)#element.second-element.second%10)
                if(element2 == self.__cache[-1][i]):
                    f.write("{};".format(element))
                    for j in range(len(self.__cache)-1):#Last element of self.__cache is datetime
                        f.write("{};".format(self.__cache[j][i]))
            f.write("\n")
        f.close()
        return
    
    def plot(self, xlim, ylim):
        '''
        To plot the data, two columns have to be read first using self.getCells
        '''
        plt.figure()
        plt.plot(self.__cache[0], self.__cache[1], "x")
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.show()
        plt.close()
        
    def stereographic(self):
        plt.figure()

        mapPlot = bm.Basemap(projection='npstere', boundinglat=10, lon_0=0, resolution='i')
        mapPlot.drawcoastlines()
        mapPlot.fillcontinents(color='coral', lake_color='aqua')
        mapPlot.drawparallels(np.arange(-80., 81., 20.))
        mapPlot.drawmeridians(np.arange(-180., 181., 20.))
        mapPlot.drawmapboundary(fill_color='aqua')

        mapPlot.plot(bhv[0], bhv[1], 'ro', latlon=True)
        mapPlot.plot(tro[0], tro[1], 'ro', latlon=True)
        mapPlot.plot(lby[0], lby[1], 'ro', latlon=True)

        ps1061_lat = []
        ps1061_lon = []
        ps1062_lat = []
        ps1062_lon = []
        ps107_lat = []
        ps107_lon = []
        
        #Farblich Kennzeichnung der einzelnen Reiseabschnitte
        for i in range(len(self.__cache[-1])):
            if(self.__cache[-1][i] < dt.datetime(2017,6,22,0,0,0)):
                ps1061_lat.append(self.__cache[1][i])
                ps1061_lon.append(self.__cache[0][i])
            elif(self.__cache[-1][i] < dt.datetime(2017,7,20,0,0,0)):
                ps1062_lat.append(self.__cache[1][i])
                ps1062_lon.append(self.__cache[0][i])
            else:
                ps107_lat.append(self.__cache[1][i])
                ps107_lon.append(self.__cache[0][i])

        if(len(ps1061_lon) > 0): 
            mapPlot.plot(ps1061_lon, ps1061_lat, 'b.', latlon=True, mew=0.1)
        if(len(ps1062_lon) > 0):
            mapPlot.plot(ps1062_lon, ps1062_lat, 'r.', latlon=True, mew=0.1)
        if(len(ps107_lon) > 0):
            mapPlot.plot(ps107_lon, ps107_lat, 'g.', latlon=True, mew=0.1)
        plt.show()
        plt.close()

    def getLine(self, line):
        return [self.__cache[i][:][line] for i in range(len(self.__names))]

    def interpolate(self, secondFile):#Das hier muss alles ueberarbeitet werden! Syntax ist aber wohl erstmal okay
        columns = []
        weather = []
        newColumns = [[] for i in range(len(self.__columns))]
        sFile = dship(secondFile)
        lastLine = sFile.getLine(0)
        
        for element in self.__names:
            if("WEATHER" not in element):
                columns.append(element)
            else:
                weather.append(element)

        for i in range(len(self.__columns[0])):
            second1 = self.__columns[0][i].second

            if(i+1 != len(self.__columns[0])):
                second2 = self.__columns[0][i+1].second
            else:
                second2 = lastLine[0].second
                
            grid = [second1+j for j in range(10)]

            year = self.__columns[0][i].year
            month = self.__columns[0][i].month
            day = self.__columns[0][i].day
            hour = self.__columns[0][i].hour
            minute = self.__columns[0][i].minute

            x = datetimePlus10Sec(year, month, day, hour, minute, second1)
            for k in x:
                newColumns[0].append(k)

            #Die Wetterdaten gibt es nur minuetlich, also muss die Interpolation da anders laufen
            for j in range(1,len(columns)):
                if(second2 == 0):
                    second2 = 60
                if(i+1 != len(self.__columns[0])):
                    yEnd = self.__columns[j][i+1]
                else:
                    yEnd = lastLine[j]
                for l in np.interp(grid, [second1, second2], [self.__columns[j][i], yEnd]):
                    newColumns[j].append(l)
            #Jetzt sind die vollen Sekunden doppelt....
            
            #Wetterdaten nur alle sechs Durchlaeufe
            if(i % 6 == 0):
                secondGrid = [r for r in range(60)]
                for h in range(len(columns), len(columns)+len(weather)):
                    if(i+6 != len(self.__columns[0])):
                        yEnd = self.__columns[j][i+6]
                    else:
                        yEnd = lastLine[j]
                    for o in np.interp(secondGrid, [0, 60], [self.__columns[h][i], yEnd]):
                        newColumns[h].append(o)
          #              for o in range(60):
          #                  newColumns[h].append(self.__columns[h][i])
        self.__columns = newColumns
        return
        
if __name__ == "__main__":
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    path = "/home/philipp/Arbeit/Backup Polarstern/DSHIP/"
    filename = "index.dat"
    day = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", \
           "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", \
         "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", \
         "31"]
    #month = ["05", "06", "07", "08"]
    #month = ["07","06"]
    #gc.enable()
    #for m in month:
    #    for d in day:
    #        try:
    start = dt.datetime(2017, 7, 23,0,0,0)#UTC
    end = dt.datetime(2017, 8, 19,0,0,0)#UTC
    x = dship(path,filename, start, end)
    x.read()
    ceiling = []
    date = []
    lat = []
    #x.stereographic()
    #times = getDatetime("/home/philippr/Arbeit/Polarstern/IFS66_Sorted/PS106", "{}{}{}".format(year, m, d), year, m, d)#"{}_{}_fertig/atmosphere".format(m, d), year, m, d)
    y = x.getCells(alldata, [0,4,9]) #Read Lon, lat, time
    for element in y[2]:
        ceiling.append(element)
    for element in y[0]:
        date.append(element)
    for element in y[1]:
        lat.append(element)
    plt.figure()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.semilogy(date, ceiling, "kx")
    #plt.plot(lat, ceiling, "kx")
    plt.tick_params(axis='both', labelsize=20)
    plt.ylim([-999, 50000])
    #plt.xlim([55, 78])
    #plt.xlabel(r"Latitude ($^{\circ}$)", fontsize=30)
    plt.xlabel("Date", fontsize=30)
    plt.ylabel(r"Ceiling ($\mathrm{ft}$)", fontsize=30)
    plt.grid(True)
    plt.show()
    plt.close()
    #x.getCells(alldata, [5,4,7,8])
    #x.printCells(
    #x.writeCSV(alldata, times, "dship_all.csv", epoch=True)
    x.showHeader()
                #x = None
                #gc.collect()
            #except:
            #    print(m, d)
                
