import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def compare_graph(func1,func2,_range):
    x = list(_range)
    y = list(map(lambda x:func1(x),x))
    z = list(map(lambda x:func2(x),x))

    plt.plot(x, y, 'r') 
    plt.plot(x, z, 'b') 
    # plt.plot(t, c, 'g') # plotting t, c separately 
    plt.show()


def show_graph(data_file):
    graph_data = open(data_file,'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)
    plt.show()