import plotly.plotly as py
from plotly.graph_objs import *
import random, time
from sklearn.cluster import KMeans
import numpy
numClusters = 40
d = []
for i in range(200):
    d.append((random.randrange(0,100),random.randrange(0,100)))
print d
#d = [(102, 209), (62, 75), (235, 151), (99, 221), (5, 207), (50, 176), (215, 267), (29, 183), (244, 266), (85, 224), (123, 175), (15, 165), (236, 205), (206, 100), (264, 160), (63, 95), (141, 45)]
#d = [(1,1),(2,2),(3,3),(14,14),(16,16),(28,29),(29,16)]
ar = numpy.array(d)
k = KMeans(n_clusters=numClusters)

k.fit(ar)
print k.inertia_
X = [i[0] for i in d]
Y = [i[1] for i in d]


names = k.labels_
completeTrace = []
for setitem in range(numClusters):
    x = [index for index,value in enumerate(names) if value == setitem]
    X = [i[0] for i in ar[x]]
    Y = [i[1] for i in ar[x]]
    trace = Scatter(
                    x=X,
                    y=Y,
                    name = setitem,
                    mode='markers',
                    stream=dict(token='j5fmnabw7y')
                    )
    completeTrace.append(trace)
    

# trace1 = Scatter(
#     x=X,
#     y=Y,
#     name = k.labels_,
#     mode='markers',
#     stream=dict(token='j5fmnabw7y')
#     )
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
                title = "Y co-ordinate"    )
)
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='axes-lines')
