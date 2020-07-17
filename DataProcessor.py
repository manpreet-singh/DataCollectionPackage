import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

from networktables import NetworkTables

style.use('dark_background')

NetworkTables.initialize(server='192.168.0.37')
nt = NetworkTables.getTable('IMU_Data')

fig = plt.figure()
plt.title('Magnetometer Data')

ax1 = fig.add_subplot(4, 1, 1)
ax2 = fig.add_subplot(4, 1, 2)
ax3 = fig.add_subplot(4, 1, 3)
head = fig.add_subplot(4, 1, 4)

time = []
xs = []
ys = []
zs = []
hs = []


def animate(i, time, xs, ys, zs, hs):
    t = nt.getNumber('time', 0)
    mag_x = nt.getNumber('mag_x', 0)
    mag_y = nt.getNumber('mag_y', 0)
    mag_z = nt.getNumber('mag_z', 0)

    heading = np.arctan2(mag_y, mag_x) * 180 / np.pi

    time.append(t)
    xs.append(mag_x)
    ys.append(mag_y)
    zs.append(mag_z)
    hs.append(heading)

    xlabel = '{:.2f}'.format(mag_x)
    ylabel = '{:.2f}'.format(mag_y)
    zlabel = '{:.2f}'.format(mag_z)
    hlabel = '{:.2f}'.format(heading)

    time = time[-100:]
    xs = xs[-100:]
    ys = ys[-100:]
    zs = zs[-100:]
    hs = hs[-100:]

    ax1.clear()
    ax1.plot(time, xs, 'salmon')
    ax1.annotate(xlabel,
                 (time[-1], xs[-1]),
                 textcoords='offset points',
                 xytext=(30, 0),
                 ha='right')

    ax2.clear()
    ax2.plot(time, ys, 'palegreen')
    ax2.annotate(ylabel,
                 (time[-1], ys[-1]),
                 textcoords='offset points',
                 xytext=(30, 0),
                 ha='right')

    ax3.clear()
    ax3.plot(time, zs, 'lightskyblue')
    ax3.annotate(zlabel,
                 (time[-1], zs[-1]),
                 textcoords='offset points',
                 xytext=(30, 0),
                 ha='right')

    head.clear()
    head.plot(time, hs, 'gold')
    head.annotate(hlabel,
                  (time[-1], hs[-1]),
                  textcoords='offset points',
                  xytext=(30, 0),
                  ha='right')


ani = animation.FuncAnimation(fig, animate, fargs=(time, xs, ys, zs, hs))
plt.show()
