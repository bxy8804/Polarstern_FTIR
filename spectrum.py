#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import readopus
import errorProp
import luftfeuchtigkeit
import os

ls=30
fs=30

def find(arr, keyword):
    for i in range(len(arr)):
        if(keyword == arr[i]):
            return i

def extractFilenames(report, start, stop, delimiter, kali=False, jump=-1):
    f = open(report, "r")
    cont = f.readlines()
    f.close()
    spectra = []
    for i in range(len(cont)):
        if(i >= start-1 and i <= stop-1 and not kali):
            spectra.append("{}/{}".format(cont[i].split(delimiter)[-1][:-1], cont[i].split(delimiter)[0]))
        elif(i >= start-1 and i <= stop-1 and kali):
            spectra.append("{}/{}.kali".format(cont[i].split(delimiter)[-1][:-1], cont[i].split(delimiter)[0]))
    return spectra

def readTemperatureFromReport(report, line, delimiter):
    f = open(report, "r")
    cont = f.readlines()
    f.close()
    spectra = []
    for i in range(len(cont)):
        if(i == line):
            return 273.15+int(cont[i-1].split(delimiter)[2])
    return -100

class spectrum:
    '''
    Class for several operations with OPUS spectra:
    readTemperatures(klimalogg, device): Reads temperatures from a TFA Dostmann KlimaLogg Device
    getTimeindex(spectrum): Reads the time when the spectra were were recorded
    plotSpec(wnmin, wnmax, ymin, ymax): Plots the OPUS spectrum with respect to the wavenumber 
    corrSpec(wnmin, wnmax, showPlot):
    getTemperatureByTimeindex(timeindex):
    getStd():
    errorTotalPower():
    opusToSfit():
    printTags():

    '''
    
    def __init__(self, spectra):
        self.__temperatures = []
        self.__rH = []
        self.__aH = []
        self.__timeindex = []
        self.__opusFile = []
        self.__names = spectra
        self.__device = ""
        for element in spectra:
            self.__opusFile.append(readopus.opus(element))
        
    def readKlimalogg(self, klimalogg, device, deviceRH=None):
        number = len(device)
        f = open(klimalogg, "r")
        klimaloggFile = f.readlines()
        f.close()
        header = klimaloggFile[0].split(";")
        data = klimaloggFile[1:]
        temp = []
        rH = []
        aH = []
        for i in range(number):
            index = find(header, device[i])
            if(deviceRH != None):
                indexRH = find(header, deviceRH[i])
            self.__temperatures = []
            #self.__device = device[i][1:3]
            for element in data:
                timeindex = element.split(";")[0]
                try:
                    temperature = float(element.split(";")[index].split('"')[1])
                    if(deviceRH != None):
                        hum = float(element.split(";")[indexRH].split('"')[1])
                except ValueError:
                    print("ValueError at {}".format(timeindex))
                    pass
                year = int(timeindex.split("-")[0])
                month = int(timeindex.split("-")[1])
                day = int(timeindex.split("-")[2].split(" ")[0])
                hour = int(timeindex.split(" ")[1].split(":")[0])-2
                minute = int(timeindex.split(":")[1])
                #Haesslich
                if(hour == -2):
                    hour = 22
                elif(hour == -1):
                    hour = 23
                if(hour == 0 or hour == 1):
                    day = day + 1
                if(month == 5 or month == 7 and day == 32):
                    day = 1
                    month = month + 1
                elif(month == 6 and day == 31):
                    day = 1
                    month = month + 1
                    temp.append(temperature)
                    if(deviceRH != None):
                        rH.append(hum)
                        aH.append(luftfeuchtigkeit.wassergehalt(hum, temperature))
            self.__temperatures.append([dt.datetime(year, month, day, hour, minute), temp])
            if(deviceRH != None):
                self.__rH.append([dt.datetime(year, month, day, hour, minute), rH])
                self.__aH.append([dt.datetime(year, month, day, hour, minute), aH])
                rH = []
                aH = []
            temp = []
        return

    def getTimeindex(self):
        for i in range(len(self.__opusFile)):
            try:
                for j in self.__opusFile[i].header.keys():
                    if("TIM" in self.__opusFile[i].header[j].keys() and "DAT" in self.__opusFile[i].header[j].keys()):
                        time = self.__opusFile[i].header[j]["TIM"]
                        date = self.__opusFile[i].header[j]["DAT"]
                        #date = spectrum.header[i]["DAT"]
                        year = int(date.split("/")[0])
                        month = int(date.split("/")[1])
                        day = int(date.split("/")[2])
                        hour = int(time.split(":")[0])
                        minute = int(time.split(":")[1])
                        self.__timeindex.append(dt.datetime(year, month, day, hour, minute))
                        break
            except:
                date = self.__names[i].split("_")[-2]
                time = self.__names[i].split("_")[-1]
                print("{} {:02d} {:02d} {} {} 0\n".format(int(date[0:4]), int(date[4:6]), int(date[6:8]), int(time[0:2]), int(time[2:4])))

                
        return self.__timeindex

    def plotSpec(self, wnmin=None, wnmax=None, ymin=None, ymax=None, legend=None, offset=0.0, lw=1):
        plt.figure()
        for i in range(len(self.__opusFile)):
            spc=[]
            if(wnmin != None and wnmax != None):
                plt.xlim([wnmin, wnmax])
            if(ymin != None and ymax != None):
                plt.ylim([ymin, ymax])
            for j in self.__opusFile[i].spc:
                spc.append((j+offset)*1e3)
                #spc.append(j)
            if(legend != None):
                plt.plot(self.__opusFile[i].spcwvn, spc, label=legend[i], lw=lw)
            else:
                plt.plot(self.__opusFile[i].spcwvn, spc, lw=lw)
        plt.grid(True)
        plt.tick_params(labelsize=ls)
        plt.xlabel(r"Wavenumber ($\mathrm{cm^{-1}}$)", fontsize=fs)
        plt.ylabel(r"Radiance ($\mathrm{mW/(m^2 \cdot sr \cdot cm^{-1})}$)", fontsize=fs)
        #plt.ylabel("Intensity (arb. Unit)", fontsize=fs)
        #plt.xlabel("OPD (cm)", fontsize=fs)
        plt.legend(fontsize=fs, loc=2)
        #plt.savefig("{}_all.svg".format(self.__names[2]))
        plt.show()
        plt.close()
        return

    def blackbody(self, temp, wnmin=0, wnmax=2000, ymin=-1, ymax=1, plot=True):
        bb = []
        for i in self.__opusFile[0].spcwvn:
            bb.append(errorProp.blackbodyStep(temp, i))

        plt.figure()
        plt.plot(self.__opusFile[0].spcwvn, bb, label="Theoretical")
        for j in range(len(self.__opusFile)):
            plt.plot(self.__opusFile[j].spcwvn, self.__opusFile[j].spc, label="Measurement {}".format(self.__names[j]))
        plt.xlim([wnmin, wnmax])
        plt.ylim([ymin, ymax])
        plt.legend()
        plt.grid(True)
        if(plot):
            plt.show()
        plt.close()
        return [self.__opusFile[0].spcwvn, self.__opusFile[0].spc, bb]

    def corrSpec(self, wnmin=0, wnmax=2000, humidity=False, showPlot=True):
        '''
        Calculates the correlation of the spectrum and the temperature inside the device. Returns the correlation coefficitient R^2 and shows a plot I(T) if wanted
        '''
        intensity = []
        sumIntensities = []
        temperatures = []
        aH = []
        wavenumber = self.__opusFile[0].spcwvn
        self.getTimeindex()
        #print(self.__timeindex)
        for j in range(len(self.__opusFile)):
            for i in range(len(self.__opusFile[j].spcwvn)):
                if(self.__opusFile[j].spcwvn[i] >= wnmin and self.__opusFile[j].spcwvn[i] <= wnmax):
                    intensity.append(self.__opusFile[j].spc[i])
            intensity = np.array(intensity)
            sumIntensities.append(sum(intensity))
            intensity = []
            if(humidity):
                aH.append(self.getAHByTimeindex(self.__timeindex[j], 0)*1.5 + self.getAHByTimeindex(self.__timeindex[j], 1)*1.0)
            temperatures.append(self.getTemperaturesByTimeindex(self.__timeindex[j]))

        #print(temperatures) 
        if(showPlot):
            plt.figure()
            #plt.title(self.__names[0][:-2])
            if(humidity):
                plt.plot(aH, sumIntensities, "o", label=r"$R^2 = {:0.2f}$".format(np.corrcoef(aH, sumIntensities)[1][0]**2))
                plt.xlabel(r"absolute Humidity ($\mathrm{g \cdot m^{-3}}$)")
            else:
                plt.plot(temperatures, sumIntensities, "o", label=r"$R^2 = {:0.2f}$".format(np.corrcoef(temperatures, sumIntensities)[1][0]**2))
                plt.xlabel("Temperature C", fontsize=fs)
            plt.legend(loc=1, fontsize=fs)
            plt.ylabel("Sum Intensites", fontsize=fs)
            plt.tick_params(labelsize=ls)
            plt.grid()
            plt.savefig("{}_{}_corr.svg".format(self.__names[2], self.__device))
            plt.show()
            plt.close()
        if(humidity):
            return np.corrcoef(aH, sumIntensities)[1][0]**2
        else:
            return np.corrcoef(temperatures, sumIntensities)[1][0]**2

    def plotIntVsTime(self, wnmin=800, wnmax=1100):
        intensity = []
        sumIntensities = []
        times = []
        aH = []
        self.getTimeindex()
        for j in range(len(self.__opusFile)):
            for i in range(len(self.__opusFile[j].spcwvn)):
                if(self.__opusFile[j].spcwvn[i] >= wnmin and self.__opusFile[j].spcwvn[i] <= wnmax):
                    intensity.append(self.__opusFile[j].spc[i])
            intensity = np.array(intensity)
            sumIntensities.append(sum(intensity))
            aH.append(self.getAHByTimeindex(self.__timeindex[j], 0))
            intensity = []
            times.append(self.__timeindex[j])

        plt.figure()
        plt.subplot(211)
        plt.plot(sumIntensities, times, "x", color="red")
        plt.grid(True)
        plt.ylabel("Time (red)", fontsize=fs)
        #plt.twinx()
        #plt.plot(times, aH, "x", color="magenta")
        #plt.xlabel("Time", fontsize=fs)
        plt.subplot(212)
        plt.plot(sumIntensities, aH, "x", color="green")
        plt.xlabel("Sum Intensities", fontsize=fs)     
        plt.ylabel("relative Humidity (green)", fontsize=fs)
        plt.grid(True)
        plt.show()
        plt.close()
        return
    
    def getTemperaturesByTimeindex(self, timeindex, index):
        '''
        Returns the temperature of the KlimaLoggPro at the given time cd index. If there is no temperature at the given time index, it returns -999
        '''
        print(self.__temperatures[0])
        exit(-1)
        for element in self.__temperatures:
            if(timeindex == element[0]):
                return element[1][index]
        return -999

    def getAHByTimeindex(self, timeindex, index):
        print(self.__aH[0])
        for element in self.__aH:
            if(timeindex == element[0]):
                return element[1][index]
        return -999
    
    def getStd(self):
        arrayGenerator1 = range(len(self.__opusFile[0].spc))
        arrayGenerator2 = range(len(self.__opusFile))
        array = [[] for i in range(len(self.__opusFile[0].spc))]
        avg = []
        std = []
        for i in arrayGenerator1:
            for j in arrayGenerator2:
                array[i].append(self.__opusFile[j].spc[i])

        for i in arrayGenerator1:
            std.append(np.std(array[i]))

        return np.array(std)

    def getVertrauensbereich(self):
        std = self.getStd()
        return std / np.sqrt(len(self.__opusFile))

    def getWvn(self, index=0):
        return np.array(self.__opusFile[index].spcwvn)

    def getSpc(self, index=0):
        return np.array(self.__opusFile[index].spcwvn)
           
    #Delta T_H und Delta T_C sind durch den Fehler der Infrarotkamera FLIR E40 gegeben
    def errorTotalPower(self, deltaS_C, deltaS_H, deltaS_A, THot, TCold, deltaT_H=2.0, deltaT_C=2.0, plot=True, wnmin=1, wnmax=2000, ymax=None, ymin=None):
        '''
        Calculate an error propagation for a calibrated spectrum. Takes cold blackbody (first spec), hot blackbody (second spec), emission spectrum (third spec) and the calibrated spectrum (forth spec). See ErrorTotalPower.pdf (German only)
        '''
        ColdBB_spc = []
        HotBB_spc = []
        Emission_spc = []
        Calibrated_spc = []
        ColdBB_wvn = []
        HotBB_wvn = []
        Emission_wvn = []
        Calibrated_wvn = []
        deltaS_C_spc = []
        deltaS_H_spc = []
        deltaS_A_spc = []
        for i in range(len(self.__opusFile[3].spcwvn)):
            if(self.__opusFile[3].spcwvn[i] > wnmin and self.__opusFile[3].spcwvn[i] < wnmax):
                ColdBB_spc.append(self.__opusFile[0].spc[i])
                HotBB_spc.append(self.__opusFile[1].spc[i])
                Emission_spc.append(self.__opusFile[2].spc[i])
                Calibrated_spc.append(self.__opusFile[3].spc[i])
                ColdBB_wvn.append(self.__opusFile[0].spcwvn[i])
                HotBB_wvn.append(self.__opusFile[1].spcwvn[i])
                Emission_wvn.append(self.__opusFile[2].spcwvn[i])
                Calibrated_wvn.append(self.__opusFile[3].spcwvn[i])
                deltaS_C_spc.append(deltaS_C[i])
                deltaS_H_spc.append(deltaS_H[i])
                deltaS_A_spc.append(deltaS_A[i])
                
        ColdBB_spc = np.array(ColdBB_spc)
        HotBB_spc = np.array(HotBB_spc)
        Emission_spc = np.array(Emission_spc)
        Calibrated_spc = np.array(Calibrated_spc)
        deltaS_C_spc = np.array(deltaS_C_spc)
        deltaS_H_spc = np.array(deltaS_H_spc)
        deltaS_A_spc = np.array(deltaS_A_spc)

        #First, the theoretical blackbody functions (Planck's function) have to be calculated
        PlanckCold_spc = np.array([errorProp.blackbodyStep(temp=TCold, freq=i) for i in ColdBB_wvn])
        PlanckCold_wvn = np.array(ColdBB_wvn)
        PlanckHot_spc = np.array([errorProp.blackbodyStep(temp=THot, freq=i) for i in HotBB_wvn])
        PlanckHot_wvn = np.array(HotBB_wvn)

        #Calculate the errors of the planck functions. These errors are caused by errors in the blackbody temperature
        deltaP_C = np.array([errorProp.dPdTStep(temp=TCold, freq=i)*deltaT_C for i in HotBB_wvn])
        deltaP_H = np.array([errorProp.dPdTStep(temp=THot, freq=i)*deltaT_H for i in HotBB_wvn])

        #Calculate partial derivatives
        errdPAdPH = np.array([i for i in errorProp.dPAdPH(S_A=Emission_spc, S_C=ColdBB_spc, S_H=HotBB_spc)])
        errdPAdPC = np.array([i for i in errorProp.dPAdPC(S_A=Emission_spc, S_C=ColdBB_spc, S_H=HotBB_spc)])
        errdPAdSA = np.array([i for i in errorProp.dPAdSA(P_H=PlanckHot_spc, P_C=PlanckCold_spc, S_H=HotBB_spc, S_C=ColdBB_spc)])
        errdPAdSH = np.array([i for i in errorProp.dPAdSH(S_A=Emission_spc, P_H=PlanckHot_spc, P_C=PlanckCold_spc, S_H=Emission_spc, S_C=ColdBB_spc)])
        errdPAdSC = np.array([i for i in errorProp.dPAdSC(S_A=Emission_spc, P_H=PlanckHot_spc, S_H=HotBB_spc, S_C=ColdBB_spc, P_C=PlanckCold_spc)])

        #Calculate the error terms
        errdPAdPH = errdPAdPH * deltaP_H
        errdPAdPC = errdPAdPC * deltaP_C
        errdPAdSA = errdPAdSA * deltaS_A_spc
        errdPAdSH = errdPAdSH * deltaS_H_spc
        errdPAdSC = errdPAdSC * deltaS_C_spc

        errPA = np.abs(errdPAdPH) + np.abs(errdPAdPC) + np.abs(errdPAdSA) + np.abs(errdPAdSH) + np.abs(errdPAdSC)
        errPAPosFKT = Calibrated_spc + errPA
        errPANegFKT = Calibrated_spc - errPA
        relErrPA = (errPA / Calibrated_spc)

        if(plot):
            plt.figure()
            plt.plot(Calibrated_wvn, Calibrated_spc, "g", label="Calibrated spectrum")
            plt.plot(Calibrated_wvn, errPAPosFKT, "r", label="Error calibrated spectrum")
            plt.plot(Calibrated_wvn, errPANegFKT, "r")
            plt.grid(True)
            #plt.legend(loc=1, fontsize=fs)
            plt.xlim([wnmin, wnmax])
            if(ymax == None and ymin == None):
                plt.ylim([min(errPANegFKT)*0.9, max(errPAPosFKT)*1.1])
            else:
                plt.ylim([ymin, ymax])
            plt.xlabel(r"Wavenumber ($\mathrm{cm^{-1}}$)", fontsize=fs)
            plt.ylabel(r"Intensity ($\mathrm{W cm^{2}sr cm^{-1}}$)",fontsize=fs)
            plt.tick_params(labelsize=ls)
            plt.savefig("{}.absErr.svg".format(self.__names[2]), size="2000x1500")
            plt.close()
            plt.figure()
            plt.plot(Calibrated_wvn, relErrPA)
            plt.xlim([wnmin, wnmax])
            plt.ylim([min(relErrPA)*0.9,max(relErrPA)*1.1])
            plt.xlabel(r"Wavenumber ($\mathrm{cm^{-1}}$)", fontsize=fs)
            plt.ylabel(r"Relative error (1)", fontsize=fs)
            plt.tick_params(labelsize=ls)
            plt.grid(True)
            plt.savefig("{}.relErr.svg".format(self.__names[2]))
            plt.close()
        return errPA, relErrPA

    def opusToSfit(self, angle, rEarth, lat, lon, snr, year=None, month=None, day=None, hour=None, minute=None, comment="Empty", wnmin=0, wnmax=2000):#All parameters except wnmin and wmnax are lists
        '''
        Converts Opus-File(s) to a SFIT4 readable format:
        ANGLE RADIUSOFEARTH LATITUDE LONGITUDE SNR
        YEAR MONTH DAY HOUR MINUTE SECOND
        COMMENT
        FIRSTWAVENUMBER LASTWAVENUMBER STEPSIZE STEPS
        INTENSITY[0]
        .
        .
        .
        '''
        numOfSpec = len(angle) #Number of spectra which have to be converted
        lastWavenumber = 0
        #Calculate the first wavenumber, the stepwidth and the last wavenumber for the SFIT4 file
        for i in range(numOfSpec):

            for j in range(len(self.__opusFile[i].spcwvn)):
                if(self.__opusFile[i].spcwvn[j] > wnmin):
                    firstWavenumber = self.__opusFile[i].spcwvn[j]
                    secondWavenumber = self.__opusFile[i].spcwvn[j+1]
                    stepSize = secondWavenumber - firstWavenumber
                    break
            for k in range(j, len(self.__opusFile[i].spcwvn)):
                if(self.__opusFile[i].spcwvn[k] > wnmax):
                    lastWavenumber = self.__opusFile[i].spcwvn[k-1]
                    break
            if(lastWavenumber == 0):
                lastWavenumber = self.__opusFile[i].spcwvn[-1]
            steps = int((lastWavenumber - firstWavenumber) / stepSize)

            #Create the file
            fname = "{}_sfit4.dpt".format(self.__names[i])
            f = open(fname, "w")
            f.write("{} {} {} {} {}\n".format(angle[i], rEarth[i], lat[i], lon[i], snr[i]))

            #Choose the date and time:
            #1. Given as parameter
            #2. Given as filename
            #3. From the OPUS file (won't work with spectra which were calibrated in OPUS)
            if(year != None and month != None and day != None and hour != None and minute != None):
                f.write("{} {:02d} {:02d} {} {} 0\n".format(year[i], month[i], day[i], hour[i], minute[i]))
            else:
                try:
                    #Example: Emission_20170602_1429.0.kali.0 ->
                    #date[0:4] = year = 2017
                    #date[4:6] = month = 06
                    #date[6:8] = day = 02
                    #time[0:2] = hour = 14
                    #time[2:4] = minute = 29
                    #second = 0 (default)
                    date = self.__names[i].split("_")[-2]
                    time = self.__names[i].split("_")[-1]
                    
                    f.write("{} {:02d} {:02d} {} {} 0\n".format(int(date[0:4]), int(date[4:6]), int(date[6:8]), int(time[0:2]), int(time[2:4])))
                except IndexError:
                    try:
                        f.write("{} {:02d} {:02d} {} {} {}\n".format(self.getTimeindex(self.__opusFile[i]).year, \
                                                                     self.getTimeindex(self.__opusFile[i]).month,\
                                                                     self.getTimeindex(self.__opusFile[i]).day, \
                                                                     self.getTimeindex(self.__opusFile[i]).hour,\
                                                                     self.getTimeindex(self.__opusFile[i]).minute,\
                                                                     self.getTimeindex(self.__opusFile[i]).second))
                    except NameError:
                        print("Give correct date!")
                        f.close()
                        exit(-1)
            f.write("{}\n".format(comment[i]))
            f.write("{:.9f} {:.9f} {:.9f} {}\n".format(firstWavenumber, lastWavenumber, stepSize, steps))
            for g in range(j, k, 1):
                f.write("{:.10f}\n".format(self.__opusFile[i].spc[g]))
            f.close()
                
        return

    def printTags(self):
        '''
        Prints all headers of a OPUS file. For this, the method print_header() of readopus.py is called
        '''
        for i in range(len(self.__opusFile)):
            print("Header {}:\n".format(self.__names[i]))
            self.__opusFile[i].print_header()
        return

    def toText(self, fname, wnmin=0, wnmax=2000, smooth=0.0):
        f = open(fname, "w")
        spectrum = []
        wavenumber = []
        for i in range(len(self.__opusFile[0].spcwvn)):
            if(self.__opusFile[0].spcwvn[i] >= wnmin and self.__opusFile[0].spcwvn[0] <= wnmax):
                wavenumber.append(self.__opusFile[0].spcwvn[i])
                spectrum.append(self.__opusFile[0].spc[i])

        #for j in range(1000):
        #    for i in range(len(spectrum)):
        #        if(i > 0 and np.abs(spectrum[i-1] - spectrum[i]) > smooth):#Lazy evaluation?
        #            spectrum[i] = (spectrum[i-1] + spectrum[i+1]) / 2.0

        for i in range(len(spectrum)):
            f.write("{};{}\n".format(wavenumber[i], spectrum[i]))

        f.close()
        return
