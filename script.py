import sys
import datetime

fileName= sys.argv[1]

import datetime

#   May 04 15:52:05 2022

def convertStringToTimeObject(givenTime):
    
    date_time_obj = datetime.datetime.strptime(givenTime,'%b %d %H:%M:%S %Y')
    
    return date_time_obj
    

with open(fileName, 'r') as f:
    
    f_contents= f.readlines()
    
    info={}
    
    maxTimeToProcessData= datetime.timedelta(0)
    minTimeToProcessData= datetime.timedelta(days=100)
    
    for l in f_contents:
        
        s= l.split(']')
        
        # print(s)
        
        device= s[2][2:]
        status= s[-1].split(' ')[-1][0:-1]
        logType= s[1][2:]
        time= s[0][1:]
        timeObj= convertStringToTimeObject(time)
        
        
        if device not in info:
            info[device]= { "connectedCount": 0, "errorCount": 0, "successCount": 0 ,"connectStartTime":""}
        
        if status=="Connected":
            info[device]["connectedCount"]+=1
            info[device]["connectStartTime"]=timeObj
        
        if logType=="ERROR":
            info[device]["errorCount"]+=1
            
        if status=="SUCCSESS":
            info[device]["successCount"]+=1
            
        if status=="Disconnected":
            timeTakenToProcessData= timeObj - info[device]["connectStartTime"]
            
            maxTimeToProcessData=max(maxTimeToProcessData,timeTakenToProcessData)
            minTimeToProcessData=min(minTimeToProcessData,timeTakenToProcessData)
    
    errorDeviceCount=0
    successSentDataDeviceCount=0
    
    print()
    
    for device in info:
        print("Device {} connected {} times.".format(device,info[device]["connectedCount"]))
        if info[device]["errorCount"]:
            errorDeviceCount+=1
            
        if info[device]["successCount"]:
            successSentDataDeviceCount+=1
            
    
    print("\n{} devices encounter error".format(errorDeviceCount))
    
    print("\n{} devices succesfully sent data".format(successSentDataDeviceCount))
    
    maxDays, maxHours, maxMinutes , maxSeconds= maxTimeToProcessData.days, maxTimeToProcessData.seconds // 3600, maxTimeToProcessData.seconds // 60 % 60,maxTimeToProcessData.seconds % 60
    
    print("\nMax Time Taken to Process Data is {} days, {} hours, {} minutes, {} seconds".format(maxDays,maxHours,maxMinutes,maxSeconds))
    
    minDays, minHours, minMinutes, minSeconds = minTimeToProcessData.days, minTimeToProcessData.seconds // 3600, minTimeToProcessData.seconds // 60 % 60, minTimeToProcessData.seconds % 60
    
    print("\nMin Time Taken to Process Data is {} days, {} hours, {} minutes, {} seconds\n".format(minDays,minHours,minMinutes,minSeconds))
    
    