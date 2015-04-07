from urllib2 import Request, urlopen, URLError
import urllib2
import time
from bs4 import BeautifulSoup
from datetime import datetime
from DeviceInfo import DeviceInfo
import math
import csv
import numpy
from sklearn.cluster import KMeans
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import random

URL = "http://ctaoapp.cisco.com:8070/api/contextaware/v1/location/clients"
username = "learning"
password = "learning"
interval = 5
machineIndex = 0
machineIndexDict = {}
macDict = {}
lengthOfEachCell = 15
widthOfEachCell = 15
nrow = None
ncol = None
width = None
height = None
length = None
thresholdDistance = 2
numClusters = 8
stream_id = None

def doPlotConfiguration():
    global stream_id
    py.sign_in('raunaklakhwani','pbbmsi2kfy')
    tls.set_credentials_file(username="raunaklakhwani", 
                                 api_key="pbbmsi2kfy")
    tls.set_credentials_file(stream_ids=[
            "dnseotxru0"
        ])
    stream_ids = tls.get_credentials_file()['stream_ids']

    # Get stream id from stream id list 
    stream_id = stream_ids[0]
    # Make instance of stream id object 
    stream = Stream(
        token=stream_id  # (!) link stream id to 'token' key
    )
    
    # Initialize trace of streaming plot by embedding the unique stream_id
    trace1 = Scatter(
        x=[],
        y=[],
        mode='markers',
        stream=stream,
        marker = Marker(color = "yellow")
    )
    data = Data([trace1])
    layout = Layout(
                showlegend = False,
                autosize = True,
                height = 800,
                width = 800,
                title = "MAP",
                xaxis=XAxis(
                    zerolinewidth = 4,
                    gridwidth = 1,
                    showgrid = True,
                    zerolinecolor = "#969696",
                    gridcolor = "#bdbdbd",
                    linecolor = "#636363",
                    mirror = True,
                    zeroline = False,
                    showline = True,
                    linewidth = 6,
                    type = "linear",
                    range = [0,300],
                    autorange = False,
                    autotick = False,
                    dtick = 15,
                    tickangle = -45,
                    title = "X co-ordinate"
                    ),
                yaxis=YAxis(
                    zerolinewidth = 4,
                    gridwidth = 1,
                    showgrid = True,
                    zerolinecolor = "#969696",
                    gridcolor = "#bdbdbd",
                    linecolor = "#636363",
                    mirror = True,
                    zeroline = False,
                    showline = True,
                    linewidth = 6,
                    type = "linear",
                    range = [300,0],
                    autorange = False,
                    autotick = False,
                    dtick = 15,
                    tickangle = -45,
                    title = "Y co-ordinate"    
                    )
                )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='axes-lines')

def getIndexFromMachineIndexDict(macaddress):
    '''
    Get the index from the machineIndexdict for the corresponding mac address 
    '''
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
    
    col = math.floor(math.ceil(float(x))/lengthOfEachCell)
    row = math.floor(math.ceil(float(y))/widthOfEachCell)
    #col = int(math.ceil(float(x) / lengthOfEachCell))
    #row = int(math.ceil(float(y) / widthOfEachCell))
    return (row, col)

def getDataFromXML(xml):
    '''
    Gets the parameter from the xml data and returns the dict with four keys in it. 
    Height, Width, Length, mobileDevicesList
    '''
    global width, height, length, nrow, ncol
    dataDict = {}
    xmlFormat = BeautifulSoup(xml)
    if width is None:
        width = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['width']
    if height is None:
        height = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['height']
    if length is None:    
        length = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['length']
    if nrow is None and width is not None:
        nrow = math.ceil(float(width) / widthOfEachCell)
    if ncol is None and length is not None:
        ncol = math.ceil(float(length) / lengthOfEachCell)
        
    for wirelessclientlocation in xmlFormat.find_all("wirelessclientlocation"):
        
        macaddress = wirelessclientlocation['macaddress']
        index = getIndexFromMachineIndexDict(macaddress)
            
        x = wirelessclientlocation.mapcoordinate['x']
        y = wirelessclientlocation.mapcoordinate['y']
        macaddress = wirelessclientlocation['macaddress']
        firstlocatedtime = parseDate(wirelessclientlocation.statistics['firstlocatedtime'])
        lastlocatedtime = parseDate(wirelessclientlocation.statistics['lastlocatedtime'])
        block = getBlock(x, y)
        blockNumber = block[0] * ncol + block[1]
        
        deviceInfo = DeviceInfo(x, y, macaddress, firstlocatedtime, lastlocatedtime, index, block, blockNumber)
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

def main():
    doPlotConfiguration()
    while True:
        responseDict = getXMLResponse()
        if responseDict['isError'] == False:
            getDataFromXML(responseDict['data'])
            print macDict
            generateGraph()
            #generateCsv()
            time.sleep(5)
            print "Done"
            
def colorGenerator():
    def r():
        hexRandom = hex(random.randint(0, 255))[2:]
        return hexRandom if len(hexRandom) >= 2 else hexRandom + "0"
    return "#" + r()+ r() + r()
            
def generateGraph():
    d = [(deviceInfoList[-1]['data'].x, deviceInfoList[-1]['data'].y) for index,deviceInfoList in macDict.items()]
    textList = [deviceInfoList[-1]['data'].macaddress for index,deviceInfoList in macDict.items()]
    ar = numpy.array(d)
    k = KMeans(n_clusters=numClusters)
    k.fit(ar)
    X = [i[0] for i in d]
    Y = [i[1] for i in d]
    color = [colorGenerator() for i in range(len(X))]
    labels = k.labels_
    finalColors = [color[i] for i in labels]
    
    s = py.Stream(stream_id)
    s.open()
    s.write(Scatter(x=X, y=Y, text = textList, marker = Marker(color = finalColors)))
    print zip(labels,finalColors)
    s.close()
    
if __name__ == '__main__':
    main()
    print 'Hello'
