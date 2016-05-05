#Author: Aaron Algoedt
#Date: 7 August 2015
#Contact: aaron.algoedt@ugent.be

#Dependencies Numpy and Matplotlib are necessairy to execute!
import numpy as np
import matplotlib.pyplot as plt
import array

#PYROOT
import ROOT as rt
from ROOT import * 
from os import path

# Import necessary data
##name = raw_input("Give the name of the dat files you want to examine: ")
filenames = ["201507/20150701_20150731_CAEN_HV", "201508/20150801_20150830_CAEN_HV", "201509/20150901_20150930_CAEN_HV", "201510/20151001_20151031_CAEN_HV", "201511/20151101_20151130_CAEN_HV", "201512/20151201_20151231_CAEN_HV", "201601/20160101_20160131_CAEN_HV"]

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


#CAENdata = np.genfromtxt("CAEN_" + name + ".part", skip_header=4 , dtype='str')

 # np.genfromtxt("CAEN_" + name + ".dat", dtype='str')

#Reconstruct CAEN data:

Igraphs = []
Vgraphs = []

Igraphs_comp = []
Vgraphs_comp = []

Igraphs_comp_current = []
Vgraphs_comp_current = []

interrupt = 0;

fs = files()

mchan = 6

channels = range(mchan)

Ihist=TH1F("h","h",1,0,31)
Ihist.SetTitle("")
Ihist.GetXaxis().SetTitle("Time (days)")
Ihist.GetYaxis().SetTitle("Intensity #muA")
Ihist.GetYaxis().SetRangeUser(0,100.)
Ihist.Draw("")
Ihist.SetStats(0)

Vhist=TH1F("h","h",1,0,31)
Vhist.SetTitle("")
Vhist.GetXaxis().SetTitle("Time (s)")
Vhist.GetYaxis().SetTitle("HV (V)")
Vhist.GetYaxis().SetRangeUser(0,8000.)
Vhist.Draw("")
Vhist.SetStats(0)


Ihist_current=TH1F("h","h",1,0,250)
Ihist_current.SetTitle("")
Ihist_current.GetXaxis().SetTitle("Time (days)")
Ihist_current.GetYaxis().SetTitle("Intensity #muA")
Ihist_current.GetYaxis().SetRangeUser(0,100.)
Ihist_current.Draw("")
Ihist_current.SetStats(0)

Vhist_current=TH1F("h","h",1,0,250)
Vhist_current.SetTitle("")
Vhist_current.GetXaxis().SetTitle("Time (s)")
Vhist_current.GetYaxis().SetTitle("HV (V)")
Vhist_current.GetYaxis().SetRangeUser(0,8000.)
Vhist_current.Draw("")
Vhist_current.SetStats(0)

canvas = TCanvas("","",0,0,200,400)
canvas.Divide(1,2)

time0 = 0 # time counter to keep track of history
time = 0

imonth = -1
for month in filenames:
    imonth += 1
    time0 += time # to keep track of time history
    print "time0 = ", time0/86400.

    for channel in channels:	
	print channel
	CAENdata = next(fs) 
        CAENtime =array.array('d')
        CAENi =array.array('d')
        CAENv =array.array('d')

        CAENtime_comp =array.array('d')
        CAENtime_comp_current =array.array('d')
        CAENi_comp =array.array('d')
        CAENv_comp =array.array('d')

        time_temp = 0
        i_temp = 0
        v_temp = 0

        counter = 0
        filter = False
	for entry in CAENdata:
#                if counter > 100:
#                    continue
#		print entry
		yy, mm, dd = entry[0].split(".")
		h, m, s = entry[1].split(":")#
		time = 86400*(int(dd)-1) + 3600*int(h) + 60*int(m) + float(s)
		if(time >= 0):
                    CAENtime.append( time/86400. )
                    CAENi.append( float(entry[3]) )
                    CAENv.append( float(entry[2]) )
                    counter=counter+1
                    if counter%100000 == 0:
                        print counter, "", entry[3], " time = ", time/86400., " time_current = ", (time+time0)/86400.
                        
                    if int(entry[4]) == 0 :
                        if (not filter):
                            filter = True
                            CAENtime_comp.append( time/86400. )
                            CAENtime_comp_current.append( (time + time0)/86400. )
                            CAENi_comp.append( float(entry[3]) )
                            CAENv_comp.append( float(entry[2]) )
                        else :
                            time_temp = time
                            i_temp = float(entry[3])
                            v_temp = float(entry[2])

                    else :
                        if filter:
                            filter = False
                            CAENtime_comp.append( time_temp/86400.) 
                            CAENtime_comp_current.append( (time_temp + time0)/86400. )
                            CAENi_comp.append( i_temp )
                            CAENv_comp.append( v_temp )
                            
                        CAENtime_comp.append( (time)/86400. )
                        CAENtime_comp_current.append( (time+time0)/86400. )
                        CAENi_comp.append( float(entry[3]) )
                        CAENv_comp.append( float(entry[2]) )


        graph1 = TGraph(len(CAENtime),CAENtime, CAENi)
        Igraphs.append(graph1)

        graph1 = TGraph(len(CAENtime),CAENtime, CAENv)
        Vgraphs.append(graph1)

        canvas.cd(1)
        Ihist.SetTitle(chambers[channel])
        Ihist.Draw()
        Igraphs[imonth*mchan+channel].Draw("SAMEPL")


        canvas.cd(2)
        Vgraphs[imonth*mchan+channel].SetMarkerColor(kRed)
        Vgraphs[imonth*mchan+channel].SetLineColor(kRed)
        Vhist.SetTitle(chambers[channel])
        Vhist.Draw()
        Vgraphs[imonth*mchan+channel].Draw("SAMEPL")

        canvas.SaveAs(filenames[imonth]+"_HV"+str(channel)+"_"+chambers[channel]+".pdf")

        # ========================= Compressed one =========================

        graph1 = TGraph(len(CAENtime_comp),CAENtime_comp, CAENi_comp)
        graph1_current = TGraph(len(CAENtime_comp_current),CAENtime_comp_current, CAENi_comp)
        Igraphs_comp.append(graph1)
        Igraphs_comp_current.append(graph1_current)

        graph1 = TGraph(len(CAENtime_comp),CAENtime_comp, CAENv_comp)
        graph1_current = TGraph(len(CAENtime_comp_current),CAENtime_comp_current, CAENv_comp)
        Vgraphs_comp.append(graph1)
        Vgraphs_comp_current.append(graph1_current)


        canvas.cd(1)
        Ihist.SetTitle(chambers[channel])
        Ihist.Draw()
        Igraphs_comp[imonth*mchan+channel].Draw("SAMEPL")


        canvas.cd(2)
        Vgraphs_comp[imonth*mchan+channel].SetLineColor(kRed)
        Vgraphs_comp[imonth*mchan+channel].SetMarkerColor(kRed)
        Vhist.SetTitle(chambers[channel])
        Vhist.Draw()
        Vgraphs_comp[imonth*mchan+channel].Draw("SAMEPL")

        canvas.SaveAs(filenames[imonth]+"_HV"+str(channel)+"_"+chambers[channel]+"_compressed.pdf")



for channel in channels:	

    output = TFile("channel_HV" + str(channel)+"_"+chambers[channel]+"_compressed.root", "RECREATE")
    output.cd()

    canvas.cd(1)
    Ihist_current.SetTitle(chambers[channel])
    Ihist_current.Draw()

    imonth = -1    
    for month in filenames:
        imonth += 1   
        month_num = (imonth+month_start)%12
        year_num = year_start + (imonth+month_start)/12
        Igraphs_comp_current[imonth*mchan+channel].Draw("SAMEPL")
        Igraphs_comp_current[imonth*mchan+channel].Write("I_channel_HV" + str(channel)+"_" + chambers[channel]+"_month_"+str(month_num)+"_"+str(year_num)+"_compressed")

    canvas.cd(2)
    Vhist_current.SetTitle(chambers[channel])
    Vhist_current.Draw()

    imonth = -1    
    for month in filenames:
        imonth += 1  
        month_num = (imonth+month_start)%12
        year_num = year_start + (imonth+month_start)/12
        Vgraphs_comp_current[imonth*mchan+channel].SetLineColor(kRed)
        Vgraphs_comp_current[imonth*mchan+channel].SetMarkerColor(kRed)
        Vgraphs_comp_current[imonth*mchan+channel].Draw("SAMEPL")
        Vgraphs_comp_current[imonth*mchan+channel].Write("V_channel_" + str(channel)+"_"+chambers[channel]+"_month_"+str(month_num)+"_"+str(year_num)+"_compressed")

    canvas.SaveAs("channel_HV" + str(channel)+"_" + chambers[channel]+"_compressed.pdf")

    output.Close()
