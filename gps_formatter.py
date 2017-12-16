from os import listdir
from os.path import isfile, join
from datetime import datetime as date
from traceback import print_exc
from sys import exit

###### Parameters -- CHANGE AS NEEDED! #####
pathName = "/home/nichole/Documents/SafeTrek/12-7-17/14/Arduino/" # Local path name
outputFile = "/home/nichole/Documents/SafeTrek/12-7-17/14/data_14_2.txt" # File name to write to

# Other initial variable declarations
answer = ""

# Get list of file names
fileNames = [f for f in listdir(pathName) if isfile(join(pathName, f))]
fileNames.sort()

class BadGPS(Exception):
    pass

# Converts GPS coordinates into DDMMSS
def convDDMMSS(par, d):
    try:
        if d == "N" or d == "E":
            multiplier = 1
        elif d == "S" or d == "W":
            multiplier = -1
        else:
            raise BadGPS('Corrupt direction data')
        parNum = float(par)
        DD = int(parNum/100)
        MM = float((par.split('.')[0])[-2:])
        MM += float(par.split('.')[1])*10**(-1*len(par.split('.')[1]))
        MM /= 60
        returnVal = str(multiplier*(DD+MM))
    except:
        returnVal = "-9999"

    return returnVal

def getTime(par):
    try:
        UTCtime = par.split(',')[1]
        if len(UTCtime) >= 6:
            hh = UTCtime[:2]
            mm = UTCtime[2:4]
            ss = UTCtime[4:6]
        else:
            raise BadGPS('Not enough digits')
        if not hh.isdigit() or not mm.isdigit() or not ss.isdigit():
            raise BadGPS('Non-numeric data')
    except BadGPS:
        hh = '99'
        mm = '99'
        ss = '99'
        print 'Time corrupted'

    UTCtime = hh + ':' + mm + ':' + ss
    return UTCtime

def getDate(par):
    try:
        UTCdate = par.split(',')[9]
        if len(UTCdate) >= 6:
            dd = UTCdate[:2]
            mo = UTCdate[2:4]
            yy = UTCdate[4:6]
        else:
            raise BadGPS('Not enough digits')
        if not dd.isdigit() or not mo.isdigit() or not yy.isdigit():
            raise BadGPS('Non-numeric data')
    except BadGPS:
        dd = '99'
        mo = '99'
        yy = '99'
        #print 'Date corrupted'

    UTCdate = yy + '-' + mo + '-' + dd
    return UTCdate

# Get speed
def getSpeed(par):
    try:
        speed = par.split(',')[7]
        if speed != '':
            speed = float(speed)
            speed *= 1.15078 # Convert from knots to mph
        else:
            speed = -9999
    except:
        speed = -9999
    return speed

# Safety Check -- Re-write pre-existing file?
if isfile(outputFile):
    while not (answer == "y" or answer == "Y"):
        print "Warning: %s already exists. Re-write? [y/n]:" %outputFile,
        answer = raw_input()
        if answer == "n" or answer == "N":
            exit("Please change parameters and try again.")

# Open outputFile
compdata = open(outputFile, 'w+')
txtToWrite = 'Latitude,Longitude,Date,Time (UTC),Speed (mph)\n'
compdata.write(txtToWrite)
for i in fileNames:
        f = open(join(pathName, i), 'r')
        f.seek(0)
        print "Opening " + i
        if f.read(1):
            for n, line in enumerate(f):
                try:
                    #print line
                    if line.strip() != "":
                        sentenceType = line.split(',')[0]
                        #print sentenceType
                        if sentenceType == "$GPRMC":
                            lat = convDDMMSS(par=(line.split(',')[3]), d=(line.split(',')[4]))
                            lon = convDDMMSS(par=(line.split(',')[5]), d=(line.split(',')[6]))
                            time = getTime(line)
                            date = getDate(line)
                            speed = getSpeed(line)
                            #print lat + ',' + lon
                            if lat != "-9999" and lon != "-9999":
                                txtToWrite = lat + ',' + lon + ',' + date + ',' + time + ',' + str(speed) + '\n'
                                #print txtToWrite
                                compdata.write(txtToWrite)
                except Exception, e:
                    print "Error: " + e.__class__.__name__ + ' : ' + str(e)
        f.close()

compdata.close()

# Print confirmation message
print "Okay done!"
