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
from Stats import Stats

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
numClusters = 1
stream_id = None
static_stream_id = None
isWidthUpdated = False
isLengthUpdated = False
staticDevices = {}
dynamicDevices = {}
STATIC_COUNT = 50
TRANSITION_STATE = "transition"
dynamicStream = None
staticStream = None

def doPlotConfiguration(width = 300,length = 300):
    global stream_id, static_stream_id, dynamicStream, staticStream
    py.sign_in('raunaklakhwani','b3fga1fz2k')
    tls.set_credentials_file(username="raunaklakhwani", 
                                 api_key="b3fga1fz2k")
    tls.set_credentials_file(stream_ids=[
            "txik5etrd5",
            "5iv4ntu3x1"
        ])
    stream_ids = tls.get_credentials_file()['stream_ids']

    # Get stream id from stream id list 
    stream_id = stream_ids[0]
    static_stream_id = stream_ids[1]
    # Make instance of stream id object 
    stream = Stream(
        token=stream_id  # (!) link stream id to 'token' key
    )
    staticStream = Stream(token = static_stream_id)
    
    # Initialize trace of streaming plot by embedding the unique stream_id
    trace1 = Scatter(
        x=[],
        y=[],
        mode='markers',
        name = "dynamic",
        stream=stream,
        marker = Marker(color = "yellow")
    )
    
    staticTrace = Scatter(
        x=[],
        y=[],
        mode='markers',
        name = "static",
        stream=staticStream,
        marker = Marker(color = "red")
    )
    
    data = Data([trace1,staticTrace])
    layout = Layout(
                showlegend = True,
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
                    range = [0,length],
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
                    range = [width,0],
                    autorange = False,
                    autotick = False,
                    dtick = 15,
                    tickangle = -45,
                    title = "Y co-ordinate"    
                    )
                )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Test2')
    dynamicStream = py.Stream(stream_id)
    staticStream = py.Stream(static_stream_id)
    dynamicStream.open()
    staticStream.open()
    

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
    global width, height, length, nrow, ncol, isWidthUpdated, isLengthUpdated
    dataDict = {"data" : {}}
    xmlFormat = BeautifulSoup(xml)
    if width is None or width != xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['width']:
        width = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['width']
        isWidthUpdated = True
    else :
        isWidthUpdated = False
    if height is None or height != xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['height']:
        height = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['height']
    if length is None or length != xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['length']:    
        length = xmlFormat.locations.wirelessclientlocation.mapinfo.dimension['length']
        isLengthUpdated = True
    else :
        isLengthUpdated = False
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
        dataDict["data"][index] = deviceInfo
        deviceInfoObject = macDict.get(index)
        if deviceInfoObject is None:
            macDict[index] = [{"data":deviceInfo}]
        else :
            macDict[index].append({"data":deviceInfo})
            
    dataDict["width"] = width
    dataDict["height"] = height
    dataDict["length"] = length
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

def main():
    while True:
        responseDict = getXMLResponse()
        if responseDict['isError'] == False:
            dataDict = getDataFromXML(responseDict['data'])
            identifyStaticDevices(dataDict["data"])
            if isWidthUpdated or isLengthUpdated:
                doPlotConfiguration(width,length)
            print macDict
            generateGraph(dataDict['data'])
            #generateCsv()
            #time.sleep(1)
            print "Done"

def identifyStaticDevices(devices):
    for index,deviceInfo in devices.items():
        updateStaticDynamicStats(deviceInfo)
    
def updateStaticDynamicStats(deviceInfo):
    index = deviceInfo.index
    if staticDevices.get(index) is None and dynamicDevices.get(index) is None:
        stats = Stats(deviceInfo.x,deviceInfo.y,None,None,1,index,None)
        dynamicDevices[index] = stats
    elif staticDevices.get(index) is not None:
        staticDeviceStat = staticDevices.get(index)
        if staticDeviceStat.x == deviceInfo.x and staticDeviceStat.y == deviceInfo.y:
            if staticDeviceStat.count <= STATIC_COUNT:
                staticDeviceStat.count = staticDeviceStat.count + 1
        elif staticDeviceStat.state is not None and staticDeviceStat.state != TRANSITION_STATE:
            staticDeviceStat.oldx = staticDeviceStat.x
            staticDeviceStat.oldy = staticDeviceStat.y
            staticDeviceStat.x = deviceInfo.x
            staticDeviceStat.y = deviceInfo.y
            staticDeviceStat.count = 1
            staticDeviceStat.state = TRANSITION_STATE
        else:
            del staticDevices[index]
            staticDeviceStat.oldx = staticDeviceStat.x
            staticDeviceStat.oldy = staticDeviceStat.y
            staticDeviceStat.x = deviceInfo.x
            staticDeviceStat.y = deviceInfo.y
            staticDeviceStat.count = 1
            staticDeviceStat.state = None
            dynamicDevices[index] = staticDeviceStat
    elif dynamicDevices.get(index) is not None:
        dynamicDeviceStat = dynamicDevices.get(index)
        if dynamicDeviceStat.x == deviceInfo.x and dynamicDeviceStat.y == deviceInfo.y:
            dynamicDeviceStat.count = dynamicDeviceStat.count + 1
            if dynamicDeviceStat.count > STATIC_COUNT:
                del dynamicDevices[index]
                dynamicDeviceStat.count = 1
                staticDevices[index] = dynamicDeviceStat
        else :
            dynamicDeviceStat.oldx = dynamicDeviceStat.x
            dynamicDeviceStat.oldy = dynamicDeviceStat.y
            dynamicDeviceStat.x = deviceInfo.x
            dynamicDeviceStat.y = deviceInfo.y
            dynamicDeviceStat.count = 1
            dynamicDeviceStat.state = None

            
def colorGenerator():
    def r():
        hexRandom = hex(random.randint(0, 255))[2:]
        return hexRandom if len(hexRandom) >= 2 else hexRandom + "0"
    return "#" + r()+ r() + r()
            
def generateGraph(data):
    
    
    static_d = [(stats.x,stats.y) for index,stats in staticDevices.items() if data.get(index) is not None]
    if len(static_d) > 0:
        static_textList = [index for index,stats in staticDevices.items() if data.get(index) is not None]
        static_X = [i[0] for i in static_d]
        static_Y = [i[1] for i in static_d]
        static_scatter = Scatter(x=static_X, y=static_Y, text = static_textList)
        staticStream.write(static_scatter)
        print "Static write"
        
    dynamic_d = [(stats.x,stats.y) for index,stats in dynamicDevices.items() if data.get(index) is not None]
    if len(dynamic_d) > 0:
        dynamic_textList = [index for index,stats in dynamicDevices.items() if data.get(index) is not None]
        ar = numpy.array(dynamic_d)
        k = KMeans(n_clusters=numClusters)
        k.fit(ar)
        dynamic_X = [i[0] for i in dynamic_d]
        dynamic_Y = [i[1] for i in dynamic_d]
        color = [colorGenerator() for i in range(len(dynamic_X))]
        print dynamic_X,dynamic_Y,color,k.labels_,dynamic_d
        labels = k.labels_
        finalColors = [color[i] for i in labels]
        dynamic_scatter = Scatter(x=dynamic_X, y=dynamic_Y, text = dynamic_textList, marker = Marker(color = finalColors))
        dynamicStream.write(dynamic_scatter)
        print zip(labels,finalColors)
    
#     d = [(deviceInfoList[-1]['data'].x, deviceInfoList[-1]['data'].y) for index,deviceInfoList in macDict.items()]
#     textList = [deviceInfoList[-1]['data'].macaddress for index,deviceInfoList in macDict.items()]
#     ar = numpy.array(d)
#     k = KMeans(n_clusters=numClusters)
#     k.fit(ar)
#     X = [i[0] for i in d]
#     Y = [i[1] for i in d]
#     color = [colorGenerator() for i in range(len(X))]
#     labels = k.labels_
#     finalColors = [color[i] for i in labels]
    
    
    
    
    
    
if __name__ == '__main__':
    main()
    print 'Hello'
