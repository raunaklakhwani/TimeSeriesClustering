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

numClusters = 10

py.sign_in('raunaklakhwani','xl6ac1klno')
tls.set_credentials_file(username="raunaklakhwani", 
                             api_key="xl6ac1klno")
tls.set_credentials_file(stream_ids=[
        "j5fmnabw7y",
        "vii6b36zch",
        "n5zislq74h",
        "5iv4ntu3x1"
    ])
stream_ids = tls.get_credentials_file()['stream_ids']

# Get stream id from stream id list 
stream_id = stream_ids[0]
# Make instance of stream id object 
stream = Stream(
    token=stream_id,  # (!) link stream id to 'token' key
    maxpoints=5000      # (!) keep a max of 80 pts on screen
)
completeTrace = []
data = Data(completeTrace)
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



while True:
    completeTrace = []
    d = []
    for i in range(200):
        d.append((random.randrange(0,100),random.randrange(0,100)))
    
    ar = numpy.array(d)
    k = KMeans(n_clusters=numClusters)
    k.fit(ar)
    X = [i[0] for i in d]
    Y = [i[1] for i in d]
    names = k.labels_
    for setitem in range(numClusters):
        x = [index for index,value in enumerate(names) if value == setitem]
        X = [i[0] for i in ar[x]]
        Y = [i[1] for i in ar[x]]
        trace = Scatter(
                        x=X,
                        y=Y,
                        name = setitem,
                        mode='markers',
                        stream = stream
                        )
        completeTrace.append(trace)
        
    
    