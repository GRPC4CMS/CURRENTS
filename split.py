foldername = "201601"
filename = "20160101_20160131_CAEN_HV"

def files():
    n = -2
    while True:
        n += 1
        if (n == -1) :
	   yield open('trash.part', 'w')
	else: 
	   yield open(foldername + "/" + filename+'000%d.part' % n, 'w')

	
pat = 'dist_1:CAEN/CaenCrateCMS/'
fs = files()
outfile = next(fs) 

with open(foldername+"/"+filename+".dat", "read") as infile:
    for line in infile:
        if pat not in line:
            outfile.write(line)
        else:
	    outfile = next(fs)
	    outfile.write(line)
            items = line.split(pat)

