#Author: Aaron Algoedt
#Date: 7 August 2015
#Contact: aaron.algoedt@ugent.be

#Dependencies Numpy and Matplotlib are necessairy to execute!
import numpy as np
import matplotlib.pyplot as plt
from array import array

#PYROOT
import ROOT as rt
from ROOT import * 
from os import path

# Import necessary data
##name = raw_input("Give the name of the dat files you want to examine: ")
#filenames = ["201508/20150801_20150830_CAEN_HV", "201509/20150901_20150930_CAEN_HV", "201510/20151001_20151031_CAEN_HV", "201511/20151101_20151130_CAEN_HV", "201512/20151201_20151231_CAEN_HV", "201601/20160101_20160131_CAEN_HV"]

#filenames = ["201510/20151001_20151031_CAEN_HV", "201511/20151101_20151130_CAEN_HV", "201512/20151201_20151231_CAEN_HV", "201601/20160101_20160131_CAEN_HV"]

#dip_names = ["DIP_FILES/20151001_20151030_DIP.dat", "DIP_FILES/20151101_20151130_DIP.dat", "DIP_FILES/20151201_20151216_DIP.dat", "DIP_FILES/20160115_20160131_DIP.dat"]

dip_names = ["DIP_FILES/20151001_20151030_DIP.dat", "DIP_FILES/20151101_20151130_DIP.dat", "DIP_FILES/20151001_20151030_DIP.dat", "DIP_FILES/20151101_20151130_DIP.dat", "DIP_FILES/20151201_20151216_DIP.dat", "DIP_FILES/20160115_20160131_DIP.dat"]

filenames = ["201508/20150801_20150830_CAEN_HV", "201509/20150901_20150930_CAEN_HV","201510/20151001_20151031_CAEN_HV", "201511/20151101_20151130_CAEN_HV", "201512/20151201_20151231_CAEN_HV", "201601/20160101_20160131_CAEN_HV"]




year_start = 2015
month_start = 8





chambers = ["Empty", "DIF16_LR", "DIF32_HR", "DIF216_LR", "DIF28_LR", "DIF6_LR"]

def files():

    p = -1
    while True:
        p += 1
        n = -1
        while n < 5:
            n += 1
            yield  np.genfromtxt(filenames[p]+'000%d.part' % n, skip_header=3 , skip_footer=1, dtype='str')


def dip_files():

    p = -1
    while True:
        p += 1
        yield  np.genfromtxt(dip_names[p], skip_header=4 , skip_footer=0, dtype='str')



#CAENdata = np.genfromtxt("CAEN_" + name + ".part", skip_header=4 , dtype='str')

 # np.genfromtxt("CAEN_" + name + ".dat", dtype='str')

#Reconstruct CAEN data:

interrupt = 0;

fs = files()
ds = dip_files()

mchan = 6

channels = range(mchan)

File = TFile( 'August_January.root', 'recreate' )
tree = TTree( 't1', 'tree with histos' )

year = array( 'i', [ 0 ] )
month = array( 'i', [ 0 ] )
day  = array( 'i', [ 0 ] )
hr  = array( 'i', [ 0 ] )
mn  = array( 'i', [ 0 ] )
sec  = array( 'i', [ 0 ] )
time = array( 'i', [ 0 ] )

chamber = array( 'i', [ 0 ] )

chamber_status = array( 'i', [ 0 ] )
imon  = array( 'f', [ 0. ] )
vmon  = array( 'f', [ 0. ] )

Temperature  = array( 'f', [ 0. ] )
Pressure  = array( 'f', [ 0. ] )
Humidity  = array( 'f', [ 0. ] )

source_status  = array( 'i', [ 0 ] )
attenuator  = array( 'f', [ 0. ] )



tree.Branch( 'year', year, 'year/I' )
tree.Branch( 'month', month, 'month/I' )
tree.Branch( 'day', day, 'day/I' )
tree.Branch( 'hr', hr, 'hr/I' )
tree.Branch( 'mn', mn, 'mn/I' )
tree.Branch( 'sec', sec, 'sec/I' )
tree.Branch( 'time', time, 'time/I' )

tree.Branch( 'chamber', chamber, 'chamber/I' )

tree.Branch( 'chamber_status', chamber_status, 'chamber_status/I' )
tree.Branch( 'imon', imon, 'imon/F' )
tree.Branch( 'vmon', vmon, 'vmon/F' )

tree.Branch( 'Temperature', Temperature, 'Temperature/F' )
tree.Branch( 'Pressure', Pressure, 'Pressure/F' )
tree.Branch( 'Humidity', Humidity, 'Humidity/F' )

tree.Branch( 'source_status', source_status, 'source_status/I' )
tree.Branch( 'attenuator', attenuator, 'attenuator/F' )


time0 = 0
time_local = 0

for monthfile in filenames:
    time0 += time_local # to keep track of time history
    print monthfile
    print "time0 = ", time0/86400.

    DIPdata = next(ds)

    lenDIPdata = len(DIPdata)

    for channel in channels:	
	print channel
	CAENdata = next(fs) 

        counter = 0
        dipcounter = 0
        filter = False
	for entry in CAENdata:

            if dipcounter < lenDIPdata:
                       
                yy, mnt, dd = entry[0].split(".")
                hh, mm, ss = entry[1].split(":")#
            
                year[0] = int(yy)
                month[0] = int(mnt)
                day[0] = int(dd)
                hr[0] = int(hh)
                mn[0] = int(mm)
                sec[0] = int(float(ss))
                
                time_local = 86400*(day[0]-1) + 3600*hr[0] + 60*mn[0] + sec[0]
                time[0] = int(time0) + int(time_local)

                chamber[0] = int(channel)
                
                chamber_status[0] = int(entry[4])
                vmon[0] = float(entry[2])
                imon[0] = float(entry[3])


                dipentry = DIPdata[dipcounter]
                yydip, mntdip, dddip = dipentry[0].split(".")
                hhdip, mmdip, ssdip = dipentry[1].split(":")

     
                if ( int(yydip) == year[0] ) and ( int(mntdip) == month[0] ) and ( int(dddip) == day[0] ) and ( int(hhdip) == hr[0] ) and ( int(mmdip) == mn[0]) and ( int(float(ssdip)) == sec[0]):
                    Temperature[0] = float(dipentry[2])
                    Humidity[0] = float(dipentry[4])
                    Pressure[0] = float(dipentry[6])
                    attenuator[0] = float(dipentry[7])
                    source_status[0] = int(dipentry[9])
                    dipcounter+=1

                    tree.Fill()

                    if dipcounter%100000 == 0:
                        print int(yydip), int(mntdip), int(dddip), int(hhdip), int(mmdip), int(float(ssdip))
                        print year[0], month[0], day[0], hr[0], mn[0], sec[0]
                        print counter, "", imon[0], " time = ", time[0]/86400., " time_current = ", time_local/86400.
                        print "Temperature ", Temperature[0], " vmon[0] ",vmon[0], " imon[0] ", imon[0] 

                elif  monthfile == "201508/20150801_20150830_CAEN_HV" or monthfile == "201509/20150901_20150930_CAEN_HV":

                    Temperature[0] = -1.
                    Humidity[0] = -1.
                    Pressure[0] = -1.
                    attenuator[0] = -1.
                    source_status[0] = -1
                    
                    tree.Fill()

                    if counter%100000 == 0:
               
                        print  "No DIP files ", year[0], month[0], day[0], hr[0], mn[0], sec[0]
 
                counter=counter+1
#                        
#                    if int(entry[4]) == 0 :
#                        if (not filter):
#                            filter = True
#                            CAENtime_comp.append( time/86400. )
#                            CAENtime_comp_current.append( (time + time0)/86400. )
#                            CAENi_comp.append( float(entry[3]) )
#                            CAENv_comp.append( float(entry[2]) )
#                        else :
#                            time_temp = time
#                            i_temp = float(entry[3])
#                            v_temp = float(entry[2])





File.Write()
File.Close()
