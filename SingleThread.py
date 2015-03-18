from urllib2 import Request, urlopen, URLError
import urllib2
import time
import sys
import threading
from bs4 import BeautifulSoup
from datetime import datetime
from DeviceInfo import DeviceInfo
import math
import csv

URL = "http://ctaoapp.cisco.com:8070/api/contextaware/v1/location/clients"
username = "learning"
password = "learning"
interval = 5
machineIndex = 0
machineIndexDict = {}
macDict = {}
lengthOfEachCell = 10
widthOfEachCell = 10
width = None
height = None
length = None
thresholdDistance = 2

def getIndexFromMachineIndexDict(macaddress):
    global machineIndex
    if machineIndexDict.get(macaddress) is None:
        machineIndexDict[macaddress] = machineIndex
        index = machineIndex
        machineIndex = machineIndex + 1
    else :
        index = machineIndexDict[macaddress]
    
    return index

def getBlock(x, y):
    '''
    Returns the block info(in the form of tuple) on the basis of x and y coordinate
    '''
    row = int(math.ceil(float(x) / lengthOfEachCell))
    col = int(math.ceil(float(y) / widthOfEachCell))
    return (row, col)


def getDataFromXML(xml):
    '''
    Gets the parameter from the xml data and returns the dict with four keys in it. 
    Height, Width, Length, mobileDevicesList
    '''
    global width, height, length
    dataDict = {}
    xmlFormat = BeautifulSoup(xml)
    if width is None:
        width = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['width']
    if height is None:
        height = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['height']
    if length is None:    
        length = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['length']
        
    for wirelessclientlocation in xmlFormat.find_all("wirelessclientlocation"):
        
        macaddress = wirelessclientlocation['macaddress']
        index = getIndexFromMachineIndexDict(macaddress)
            
        x = wirelessclientlocation.mapcoordinate['x']
        y = wirelessclientlocation.mapcoordinate['y']
        macaddress = wirelessclientlocation['macaddress']
        firstlocatedtime = parseDate(wirelessclientlocation.statistics['firstlocatedtime'])
        lastlocatedtime = parseDate(wirelessclientlocation.statistics['lastlocatedtime'])
        block = getBlock(x, y)
        
        deviceInfo = DeviceInfo(x, y, macaddress, firstlocatedtime, lastlocatedtime, index, block)
        deviceInfoObject = macDict.get(index)
        if deviceInfoObject is None:
            macDict[index] = [{"data":deviceInfo}]
        else :
            macDict[index].append({"data":deviceInfo})
       
        
def parseDate(stringDate):
    '''
    Gets the date in the string format 2015-03-17T00:27:33.437+0000 and converts it into 2015-03-17 00:27:33 and then returns the date_object
    '''
    stringDate = stringDate[0:10] + " " + stringDate[11:19]
    date_object = datetime.strptime(stringDate, "%Y-%m-%d %H:%M:%S")
    return date_object

def getXMLResponse():
    '''
     Returns the response from the URL specified
    '''
    responseDict = {}
    try :
        p = urllib2.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, URL, username, password)
        handler = urllib2.HTTPBasicAuthHandler(p)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        page = urllib2.urlopen(URL).read()
        responseDict['data'] = page
        responseDict['isError'] = False
    except URLError, e:
        responseDict['data'] = e
        responseDict['isError'] = True
        print e
    
    return responseDict

def generateCsv():
    with open("/Users/ronaklakhwani/abc.csv", "w+") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["index", "macaddess", "x", "y", "row", "col", "firstlocatedtime", "lastlocatedtime"])
        for index, macList in macDict.items():
            deviceInfo = macList[len(macList) - 1]['data']
            writer.writerow([deviceInfo.index, deviceInfo.macaddress, deviceInfo.x, deviceInfo.y, deviceInfo.block[0], deviceInfo.block[1], deviceInfo.firstlocatedtime, deviceInfo.lastlocatedtime])
        
    
def main():
    while True:
        responseDict = getXMLResponse()
        if responseDict['isError'] == False:
            getDataFromXML(responseDict['data'])
            print macDict
            generateCsv()
    
if __name__ == '__main__':
    main()
    
