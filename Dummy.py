from urllib2 import Request, urlopen, URLError
import urllib2
import time
import sys
import threading
from bs4 import BeautifulSoup
from datetime import datetime

URL = "http://ctaoapp.cisco.com:8070/api/contextaware/v1/location/clients"
username = "learning"
password = "learning"
interval = 1

def getDataFromXML(xml):
    dataDict = {}
    xmlFormat = BeautifulSoup(xmlString)
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
   
    dataDict['mobileDevicesList'] = mobileDevicesList
    return dataDict
    
        
def parseDate(stringDate):
    stringDate = stringDate[0:10] + " "  + stringDate[11:19]
    date_object = datetime.strptime(stringDate,"%Y-%m-%d %H:%M:%S")
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





if __name__ == '__main__':
    responseDict = getXMLResponse()
    xmlString = responseDict['data']
    xmlFormat = BeautifulSoup(xmlString)
    a = getDataFromXML(xmlString)
    print 'Hello'
    
    