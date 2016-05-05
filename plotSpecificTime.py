#Author: Aaron Algoedt
#Date: 9 August 2015
#Contact: aaron.algoedt@ugent.be

#Dependencies Numpy and Matplotlib are necessairy to execute!
import numpy as np
import matplotlib.pyplot as plt

name = str(raw_input("Give the name of the dat files you want to examine: "))
begin = float(raw_input("Give the start date that you want to plot in seconds: "))
end = float(raw_input("Give the end date that you want to plot in seconds: "))

CAENdata = np.genfromtxt("CAEN_" + name + ".dat", dtype='str')
ADSdata = np.genfromtxt("ADS_" + name + ".dat", dtype='str')

#Reconstruct CAEN data:
CAENtime = []
CAENcurr = []

for entry in CAENdata:
	yy, mm, dd = entry[0].split(".")
	h, m, s = entry[1].split(":")
	time = 86400*(int(dd) - 20) + 3600*int(h) + 60*int(m) + float(s)
	if(time >= 0):
		CAENtime.append( time )
		CAENcurr.append( float(entry[3]) )

#Reconstruct ADS data:
ADStime = []
ADScurr = []
counter = 0
for entry in ADSdata:
        counter = counter+1
	yy, mm, dd = entry[0].split(".")
	h, m, s = entry[1].split(":")
	ADStime.append( 86400*(int(dd) - 20) + 3600*int(h) + 60*int(m) + float(s) )
	ADScurr.append( float(entry[2]) )
        if counter == 10000:
                break
#Make a plot of both currents in function of the time since 20 July 2015.
plt.figure(figsize=(15,8),dpi=100)
plt.plot(CAENtime, CAENcurr, "b-", label="CAEN")
plt.plot(ADStime, ADScurr, "r--", label="ADS")
plt.title("CAEN and ADS current of " + name + " in fuction of the time for July 2015\n")
plt.xlabel("Time (seconds since 20 July)")
plt.ylabel("Current ($\mu$A)")
plt.legend()
plt.yscale("log")
plt.xlim([begin,end])
plt.savefig("Time_CAEN-ADS_" + name + "_specific.png")
