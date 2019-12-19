import datetime
import sys

dt = datetime.datetime.now()
month = dt.month
filename = "data/" + str(month) + ".txt"
allDays = 0
allHours = 0.
doneDays = 0
doneHours = 0.
todayBegin = 0.
todayEnd = 0.
todayDuration = 0.
todayGo = 0.


def init():
    global allDays, allHours, doneDays, doneHours, filename, dt
    dt = datetime.datetime.now()
    print("file: "+filename)
    try:
        file = open(filename, 'r')
    except IOError:
        file = open(filename, 'w')
        file.write("23;184-45;\n")
        file.write("0;0-0;\n")
        file.write(str(dt.day)+";"+dt.strftime("%H-%M")+";"+dt.strftime("%H-%M")+";0-0;\n")
                    
    file = open(filename, 'r')
    lines = file.readlines()
    if(len(lines)>0):
        s = lines[0].split(";")
        if(len(s)>1):
            allDays = int(s[0])
            allHours = timeToFloat(s[1])
        s = lines[1].split(";")
        if(len(s)>1):
            doneDays = int(s[0])
            doneHours = timeToFloat(s[1])
        s = lines[len(lines)-1].split(";")
        if(int(s[0]) != dt.day):
            file = open(filename, 'a')
            file.write(str(dt.day)+";"+dt.strftime("%H-%M")+";"+dt.strftime("%H-%M")+";0-0;\n")
            doneDays += 1
    file.close()
        
    
"""def getAllDays():
    file = open(filename, 'r')
    line = file.readline()
    s = line.split(";")
    allDays = int(s[0])
    file.close()
    return int(s[0])
    
def getAllHours():
    file = open(filename, 'r')
    line = file.readline()
    s = line.split(";")
    file.close()
    return timeToFloat(s[1])
   
def getDoneDays(line):
    s = line.split(";")
    file.close()
    return int(s[0])
    
def getDoneHours(line):
    s = line.split(";")
    return timeToFloat(s[1])
"""    
def getDoneAverage():
    global doneHours, doneDays, todayDuration
    if doneDays>0:
        return (doneHours-todayDuration)/doneDays
    else:
        return doneHours
    
def getLeftDays():
    global allDays, doneDays
    return allDays - doneDays
    
def getLeftHours():
    global allHours, doneHours
    return allHours - doneHours
    
def getLeftAverage():
    global todayDuration
    return (getLeftHours()+todayDuration)/getLeftDays()
    
def getPercentAll():
    global allHours, doneHours
    return 100*(doneHours/allHours)

def getPercentToday():
    global todayDuration, todayGo, todayBegin
    return 100*((todayDuration)/(todayGo-todayBegin))

def setAllDays(days):
    global allDays, allHours, filename
    allDays = days
    file = open(filename, 'r')
    lines = file.readlines()
    lines[0] = str(allDays)+";"+str(floatToTime(allHours))+";\n"
    file = open(filename, 'w')
    for line in lines:
        file.write(line)
    file.close()
    
def setAllHours(hours):
    global allDays, allHours, filename
    allHours = hours
    file = open(filename, 'r')
    lines = file.readlines()
    lines[0] = str(allDays)+";"+str(floatToTime(allHours))+";\n"
    file = open(filename, 'w')
    for line in lines:
        file.write(line)
    file.close()

def timeToFloat(t):
    s = t.split("-")
    return float(s[0]) + float(s[1])/60

def floatToTime(f):
    iD = f // 1
    lD = ((f-iD)*60) // 1
    s = str(int(iD)) + "-" + str(int(lD))
    return s

def update():
    global todayBegin, todayEnd, doneHours, todayDuration, doneDays, filename, dt, todayGo
    dt = datetime.datetime.now()
    file = open(filename, 'r')
    lines = file.readlines()
    s = lines[len(lines)-1].split(";")
    todayBegin = timeToFloat(s[1])
    todayPrev = timeToFloat(s[2])
    todayEnd = timeToFloat(dt.strftime("%H-%M"))
    doneHours += (todayEnd - todayPrev)
    lines[1] = str(doneDays)+";"+floatToTime(doneHours)+";\n"
    todayDuration = todayEnd - todayBegin
    lines[len(lines)-1] = str(dt.day)+";"+s[1]+";"+dt.strftime("%H-%M")+";"+floatToTime(todayDuration)+";\n"
    file = open(filename, 'w')
    for line in lines:
        file.write(line)
    file.close()
    
    
    time1_4 = 9 - (8.75 - getLeftAverage())
    time5 = 7.75 - (8.75 - getLeftAverage())
    if(dt.weekday()==4):
        todayGo = todayBegin + time5
    else:
        todayGo = todayBegin + time1_4
        
    
init()
update()