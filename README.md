# CURRENTS
Those files are designed to analyse DIP and CAEN files up to end of February

1) split.py ---> Split CAEN files in "per channel" files. Ie each resulting file have only 1 channel in. It is practical to analyse.

2) merge_dip.py ---> merge DIP files to have them match CAEN files if needed. 
                    Sometimes CAEN files are made month per month and DIP every 15 days. So better to match when you analyse.

3) plotSpecificTime.py ----> Plot one CAEN file essentially regardless of DIP files

4) plotTime.py ----> Plot many channels over many monthese regardless of DIP files

5) makeTrees.py  ----> make TTrees out of DIP and CAEN information. There are some hooks to operate with the fact 
                       that sometimes DIP files are not there or are shorter than CAEN files.
                       
6) plotTimeTree.py ----> make TGraphs from TTrees

