#!/usr/bin/python2

from matplotlib.legend_handler import HandlerLine2D
import matplotlib.pyplot as plt
import radio

ls = 20

#f = open("reference.prf", "r")
f = open("radio0703w11.prf", "r")
cont = f.readlines()
f.close()

altitudes = []
altitudesReversed = []
temperatures = []
temperaturesReversed = []
pressure = []

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

x = radio.radiosonde("PS170715.w06")
temperatureRadio = x.returnTemp()
temperatureRadioNew = []
reversedTemperatureRadioNew= []
altitudeRadio = x.returnAlt()
pressureRadio = x.returnPressure()

#print(altitudeRadio)
#print(temperatureRadio[-1])


fig, ax1 = plt.subplots()
#ax1.plot(pressure, altitudes, "r", label="Pressure")
#ax2 = ax1.twiny()
#line1, = ax1.plot(temperatures, altitudes, "b+", markersize=20, mew=2, label="Temperature SFIT4")
#ax1.plot(temperatures, altitudes, "b", linewidth=2)
ax1.plot(temperatureRadio, altitudeRadio, "r", linewidth=2, label="Temerature Radiosonde")
#plt.ylim([0, 25e3])
#plt.show()
#exit(-1)

#Reverse List
for i in reversed(altitudes):
    altitudesReversed.append(i)
counter = 0

for i in reversed(temperatures):
    temperaturesReversed.append(i)

for element in altitudesReversed:
    #print(element)
    for i in range(len(temperatureRadio)):
        if(altitudeRadio[i] < (element + 20) and altitudeRadio[i] > (element - 20)):
            temperatureRadioNew.append(temperatureRadio[i])
            break
        elif(element > 20500):
            temperatureRadioNew.append(temperaturesReversed[counter])
            break
    counter = counter + 1

reversedTemperatureRadioNew = []
for element in reversed(temperatureRadioNew):
    reversedTemperatureRadioNew.append(element)

for i in range(0, len(reversedTemperatureRadioNew), 5):
    try:
        print("  {:.4E}   {:.4E}   {:.4E}   {:.4E}   {:.4E}".format(float(reversedTemperatureRadioNew[i])+273.15, \
                                                                    float(reversedTemperatureRadioNew[i+1])+273.15, \
                                                                    float(reversedTemperatureRadioNew[i+2])+273.15, \
                                                                    float(reversedTemperatureRadioNew[i+3])+273.15, \
                                                                    float(reversedTemperatureRadioNew[i+4])+273.15))
    except:
        print("  {:.4E}".format(float(reversedTemperatureRadioNew[i])+273.15))
    
line2, = ax1.plot(temperatureRadioNew, altitudesReversed, "g+", markersize=20, mew=2, label="Temperature Radiosonde regridded")
ax1.plot(temperatureRadioNew, altitudesReversed, "g", linewidth=2)
plt.legend(handler_map={line2: HandlerLine2D(numpoints=1)}, fontsize=30)
plt.grid(True)
plt.xlim([-90, 10])
#plt.ylim([-1000, 100000])
plt.tick_params(axis='both', labelsize=ls)
plt.xlabel(r"Temperature $(^{\circ}\mathrm{C})$", fontsize=30)
plt.ylabel(r"Altitude $(\mathrm{m})$", fontsize=30)
plt.show()
