import plotly.tools as tls
import plotly.plotly as py 
from plotly.graph_objs import *
import numpy as np  # (*) numpy for math functions and arrays
import random, time
py.sign_in('raunaklakhwani', 'b3fga1fz2k')
tls.set_credentials_file(username="raunaklakhwani", api_key="b3fga1fz2k")
tls.set_credentials_file(stream_ids=[
                                     "tofp3ckjh2",
        "j5fmnabw7y",
        "vii6b36zch",
        "n5zislq74h",
        "5iv4ntu3x1"
    ])

stream_ids = tls.get_credentials_file()['stream_ids']

# Get stream id from stream id list 
stream_id = stream_ids[1]

# Make instance of stream id object 
stream = Stream(
    token=stream_id,  # (!) link stream id to 'token' key
    maxpoints=10  # (!) keep a max of 80 pts on screen
)

# Initialize trace of streaming plot by embedding the unique stream_id
trace1 = Scatter(
    x=[],
    y=[],
    mode='markers',
    stream=stream  # (!) embed stream id, 1 per trace
)

data = Data([trace1])



layout = Layout(
                showlegend=False,
    xaxis=XAxis(
        showgrid=True,
        zeroline=True,
        showline=True,
        mirror='ticks',
        gridcolor='#bdbdbd',
        gridwidth=2,
        zerolinecolor='#969696',
        zerolinewidth=4,
        linecolor='#636363',
        linewidth=6
    ),
    yaxis=YAxis(
        showgrid=True,
        zeroline=True,
        showline=True,
        mirror='ticks',
        gridcolor='#bdbdbd',
        gridwidth=2,
        zerolinecolor='#969696',
        zerolinewidth=4,
        linecolor='#636363',
        linewidth=6
    )
)
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='axes-hello')


# (@) Make instance of the Stream link object, 
#     with same stream id as Stream id object
print stream_id
s = py.Stream(stream_id)

# (@) Open the stream
s.open()

while True:
    #s.open()
    x = [random.randrange(0, 300) for i in range(10)]
    print s.connected
    y = [random.randrange(0, 300) for i in range(10)]
    print x , y
    r = lambda: str(random.randint(0, 255))
    color = ["#" + r() + r() + r() for i in range(10)]
    s.write(dict(x=x, y=y))
    #next = raw_input("Enter y to continue")
    time.sleep(0.08)
    #if next == "n":
    #    break
    #s.close()
    
s.close()   
print "closed"

