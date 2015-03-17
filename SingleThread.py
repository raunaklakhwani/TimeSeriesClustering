from urllib2 import Request, urlopen, URLError
import urllib2
import time
import sys
import threading
from bs4 import BeautifulSoup
from datetime import datetime
from DeviceInfo import DeviceInfo

URL = "http://ctaoapp.cisco.com:8070/api/contextaware/v1/location/clients"
username = "learning"
password = "learning"
interval = 5
macDict = {}


def getDataFromXML(xml):
    '''
    Gets the parameter from the xml data and returns the dict with four keys in it. 
    Height, Width, Length, mobileDevicesList
    '''
    dataDict = {}
    xmlFormat = BeautifulSoup(xml)
    mobileDevicesList = []
    dataDict['width'] = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['width']
    dataDict['height'] = xmlFormat.wirelessclientlocation.mapinfo.dimension['height']
    dataDict['length'] = xmlFormat.wirelessclientlocation.mapinfo.dimension['length']
    for wirelessclientlocation in xmlFormat.find_all("wirelessclientlocation"):
        mobileDeviceDict = {}
        mobileDeviceDict['x'] = wirelessclientlocation.mapcoordinate['x']
        mobileDeviceDict['y'] = wirelessclientlocation.mapcoordinate['y']
        mobileDeviceDict['macaddress'] = wirelessclientlocation['macaddress']
        mobileDeviceDict['firstlocatedtime'] = parseDate(wirelessclientlocation.statistics['firstlocatedtime'])
        mobileDeviceDict['lastlocatedtime'] = parseDate(wirelessclientlocation.statistics['lastlocatedtime'])
        mobileDevicesList.append(mobileDeviceDict)
        
        deviceInfo = DeviceInfo(mobileDeviceDict['x'], mobileDeviceDict['y'], mobileDeviceDict['macaddress'], mobileDeviceDict['firstlocatedtime'], mobileDeviceDict['lastlocatedtime'])
        deviceInfoObject = macDict.get(mobileDeviceDict['macaddress'])
        if deviceInfoObject is None:
            macDict[mobileDeviceDict['macaddress']] = deviceInfo
        elif deviceInfo == deviceInfoObject : 
            macDict[mobileDeviceDict['macaddress']] = deviceInfo
            
    dataDict['mobileDevicesList'] = mobileDevicesList
    return dataDict
    
        
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
    
        
def callRestApiPeriodically():
    '''
    Calls the rest api Periodically
    '''
    while True:
        responseDict = getXMLResponse()
        #print responseDict
        if responseDict['isError'] == False:
            dataDict = getDataFromXML(responseDict['data'])
            print dataDict
        time.sleep(interval)      

def main():
    while True:
        responseDict = getXMLResponse()
        if responseDict['isError'] == False:
            dataDict = getDataFromXML(responseDict['data'])
            print dataDict
    
if __name__ == '__main__':
    main()
    