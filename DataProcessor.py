import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib import style
from networktables import NetworkTables

style.use('dark_background')

# Connect to the Raspberry Pi
NetworkTables.initialize(server='192.168.0.37')
nt = NetworkTables.getTable('IMU_Data')

# Initialize the plots
fig = plt.figure()

ax1 = fig.add_subplot(4, 1, 1)
ax2 = fig.add_subplot(4, 1, 2)
ax3 = fig.add_subplot(4, 1, 3)
head = fig.add_subplot(4, 1, 4)

ts = []
xs = []
ys = []
zs = []
hs = []


def animate(i, time, x_s, y_s, z_s, h_s):
    # Read the transmitted data from the Raspberry Pi
    t = nt.getNumber('time', 0)
    mag_x = nt.getNumber('mag_x', 0)
    mag_y = nt.getNumber('mag_y', 0)
    mag_z = nt.getNumber('mag_z', 0)

    # Calculate Heading
    heading = np.arctan2(mag_y, mag_x) * 180 / np.pi + 180

    time.append(t)
    x_s.append(mag_x)
    y_s.append(mag_y)
    z_s.append(mag_z)
    h_s.append(heading)

    x_label = '{:.2f}'.format(mag_x)
    y_label = '{:.2f}'.format(mag_y)
    z_label = '{:.2f}'.format(mag_z)
    h_label = '{:.2f}'.format(heading)

    time = time[-100:]
    x_s = x_s[-100:]
    y_s = y_s[-100:]
    z_s = z_s[-100:]
    h_s = h_s[-100:]

    x_dev = np.std(x_s)
    y_dev = np.std(y_s)
    z_dev = np.std(z_s)
    h_dev = np.std(h_s)

    print('xdev={0:.2f} ydev={1:.2f} zdev={2:.2f} hdev={3:.2f}'.format(x_dev, y_dev, z_dev, h_dev))

    ax1.clear()
    ax1.set_title('X Axis')
    ax1.set_ylabel('$\mu$T')
    ax1.plot(time, x_s, 'salmon')
    ax1.annotate(x_label,
                 (time[-1], x_s[-1]),
                 textcoords='offset points',
                 xytext=(30, 0),
                 ha='right')

    ax2.clear()
    ax2.set_title('Y Axis')
    ax2.set_ylabel('$\mu$T')
    ax2.plot(time, y_s, 'palegreen')
    ax2.annotate(y_label,
                 (time[-1], y_s[-1]),
                 textcoords='offset points',
                 xytext=(30, 0),
                 ha='right')

    ax3.clear()
    ax3.set_title('Z Axis')
    ax3.set_ylabel('$\mu$T')
    ax3.plot(time, z_s, 'lightskyblue')
    ax3.annotate(z_label,
                 (time[-1], z_s[-1]),
                 textcoords='offset points',
                 xytext=(30, 0),
                 ha='right')

    head.clear()
    head.plot(time, h_s, 'gold')
    head.set_title('Heading')
    head.set_ylabel('Degrees From North')
    head.annotate(h_label,
                  (time[-1], h_s[-1]),
                  textcoords='offset points',
                  xytext=(30, 0),
                  ha='right')

    # plt.tight_layout()


ani = animation.FuncAnimation(fig, animate, fargs=(ts, xs, ys, zs, hs))
plt.show()
