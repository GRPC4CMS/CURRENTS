#!/usr/bin/env python

import os, sys, ROOT, math
import array

def plot (f) :  

    mchan = 6

    channels = range(mchan)
    channels_to_graph =array.array('f')

    for ichan in channels:
        channels_to_graph.append(float(channels[ichan]))

    channels_long = range(mchan*3)

    chambers = ["Empty", "DIF16_LR", "DIF32_HR", "DIF216_LR", "DIF28_LR", "DIF6_LR"]

    satt = ["1", "gt1", "noinfo"]

    Timegraphs = []
    Igraphs = []
    Vgraphs = []
    Attgraphs = []
    Charge = []

    IntegralCharge = array.array('f')

    for ichan in channels_long:
        CAENtime =array.array('f')
        CAENi =array.array('f')
        CAENv =array.array('f')
        CAENatt =array.array('f')
        CAENcharge =array.array('f')

        Timegraphs.append(CAENtime)
        Igraphs.append(CAENi)
        Vgraphs.append(CAENv)
        Attgraphs.append(CAENatt)
        Charge.append(CAENcharge)

        IntegralCharge.append(0)




    fin = ROOT.TFile.Open(f)
    
    mychain_long = fin.Get("t1")

    output = ROOT.TFile("chamber_imon_vmon.root", "RECREATE")

    mychain = mychain_long.CopyTree("(chamber_status > 0)*(source_status != 0)*(attenuator != 0)*(vmon>6000)")

   # mychain = fin.Get("t1")

    entries = mychain.GetEntriesFast()
    
    counter = 0
  
    print "all entries", entries

    time_relative_tmp = 0
    skip = 0

    for event in mychain:
 
#       if counter > 600000: 
#            break
        counter += 1

        source_status = event.source_status
        chamber_status = event.chamber_status        

        chamber = event.chamber

        attenuator = event.attenuator

        time = event.time
        time_relative = float(time)/86400.

        source_status = event.source_status
        imon = event.imon
        vmon = event.vmon

        IntegralCharge[chamber] += imon*5*1e-6


        if (source_status == 0 or chamber_status == 0 or (attenuator < 0.5 and attenuator > -0.5)) :
            continue

 #           if skip == 0:
 #               Timegraphs[chamber].append(float(time_relative))
 #               Igraphs[chamber].append(0)
 #               Vgraphs[chamber].append(0)
 #               Attgraphs[chamber].append(0)
 #               skip = 1
  #          else :
  #              time_relative_tmp = time_relative



#        if skip == 1:
#            Timegraphs[chamber].append(float(time_relative_tmp))
#            Igraphs[chamber].append(0)
#            Vgraphs[chamber].append(0)
#            Attgraphs[chamber].append(0)
#            skip = 0


            
        if attenuator == 1:

            Timegraphs[chamber].append(float(time_relative))

            Igraphs[chamber].append(imon)
            Vgraphs[chamber].append(vmon)
            Attgraphs[chamber].append(attenuator)
            Charge[chamber].append(IntegralCharge[chamber])
        
        elif attenuator > 1.01: 

            Timegraphs[mchan+chamber].append(float(time_relative))

            Igraphs[mchan+chamber].append(imon)
            Vgraphs[mchan+chamber].append(vmon)
            Attgraphs[mchan+chamber].append(attenuator)
            Charge[mchan+chamber].append(IntegralCharge[chamber])

        else :

            Timegraphs[2*mchan+chamber].append(float(time_relative))

            Igraphs[2*mchan+chamber].append(imon)
            Vgraphs[2*mchan+chamber].append(vmon)
            Attgraphs[2*mchan+chamber].append(attenuator)
            Charge[2*mchan+chamber].append(IntegralCharge[chamber])


        if (counter%100000 == 0) :
            print counter, " ", imon, " ", vmon, " time ", float(time_relative), " attenuator ", attenuator
            

        

    for ichan in channels_long:

        if len(Timegraphs[ichan]) < 1:
            continue

        ichamber = ichan%mchan
        iatt = ichan/mchan

        graph1 = ROOT.TGraph(len(Timegraphs[ichan]), Timegraphs[ichan], Igraphs[ichan])
        graph1.Write( "Imon_chamber_" + str(ichamber) + "_" + chambers[ichamber]+"_att" + satt[iatt])

        graph1 = ROOT.TGraph(len(Timegraphs[ichan]), Timegraphs[ichan], Vgraphs[ichan])
        graph1.Write( "Vmon_chamber_" + str(ichamber) + "_" + chambers[ichamber]+"_att" + satt[iatt])

        graph1 = ROOT.TGraph(len(Timegraphs[ichan]), Timegraphs[ichan], Attgraphs[ichan])
        graph1.Write( "Att_chamber_" + str(ichamber) + "_" + chambers[ichamber]+"_att" + satt[iatt])

        graph1 = ROOT.TGraph(len(Timegraphs[ichan]), Charge[ichan], Igraphs[ichan])
        graph1.Write( "Imon_vs_Charge_chamber_" + str(ichamber) + "_" + chambers[ichamber]+"_att" + satt[iatt])

    graph1 = ROOT.TGraph(mchan, channels_to_graph, IntegralCharge)
    graph1.Write( "IntegralCharge")

    output.Close()   




#    hmsubtr_nobtagsf.Fill(msubtr)
#    hmsubtr.Fill(msubtr,btagsf)
#    hnSJBtagged.Fill(nSJBTagged, btagsf)
#    hnSJBtagged_bcUp.Fill(nSJBTagged, btagsf_bcUp)
#    hnSJBtagged_bcDown.Fill(nSJBTagged, btagsf_bcDown)
    #print 'btag sf %s + %s - %s' % (btagsf, btagsf_bcUp, btagsf_bcDown)
  


files = [
#"SignalTree.root" 
"August_January.root"
]

for f in files:
  plot(f)
