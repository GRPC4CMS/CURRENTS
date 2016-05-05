foldername = "DIP_FILES"
filename = ["20151001_20151010_DIP.dat", "20151011_20151020_DIP.dat","20151021_20151031_DIP.dat"]
outfilename = "20151001_20151030_DIP.dat"

##filename = ["20151101_20151110_DIP.dat", "20151111_20151120_DIP.dat","20151121_20151130_DIP.dat"]
##outfilename = "20151101_20151130_DIP.dat"
##filename = ["20160115_20160125_DIP.dat", "20160126_20160131_DIP.dat"]
##outfilename = "20160115_20160131_DIP.dat"

#filename = ["20160201_20160211_DIP.dat", "20160212_20160229_DIP.dat"]
#outfilename = "20160201_20160229_DIP.dat"

def files():
    n = -1
    while True:
        n += 1
        yield open(foldername + "/" + filename[n], 'r')

	
pat1 = 'dist_1'
pat2 = "===="
pat3 = "Date"

fs = files()
#outfile = next(fs) 
istart = 0

outfile = open(foldername+"/"+outfilename, "write")

for name in filename:
    print name
    with next(fs) as infile:
        print istart
        for line in infile:
            if istart == 0:
                outfile.write(line)        
            else :
                if (pat1 not in line) and (pat2 not in line) and (pat3 not in line) :
                    outfile.write(line)       
                else: 
                    print istart, line
    istart += 1



