import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

file_name = None

def animate(i):
    if file_name is not None: 
        graph_data = open(file_name,'r').read()
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

def show_graph(data_file):
    global file_name 
    file_name = data_file
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()