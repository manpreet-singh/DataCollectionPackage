import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

import numpy as np

import getpass

from pyquaternion import Quaternion

data = np.genfromtxt('data.csv', delimiter=',')

print(data[1][4:8])

x_axis = np.array([1, 0, 0])
y_axis = np.array([0, 1, 0])
z_axis = np.array([0, 0, 1])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.quiver(0, 0, 0, x_axis[0], x_axis[1], x_axis[2], length=0.1, normalize=True)
ax.quiver(0, 0, 0, y_axis[0], y_axis[1], y_axis[2], length=0.1, normalize=True)
ax.quiver(0, 0, 0, z_axis[0], z_axis[1], z_axis[2], length=0.1, normalize=True)


def animate(i, x, y, z):
    if i is not 1:
        print('\nInputs: ')
        print('x: {0} y: {1} z: {2}'.format(x, y, z))

        # Initialize Quaternion using form: a + bi + cj + dk
        q = Quaternion(a=data[i][7], b=data[i][4], c=data[i][5], d=data[i][6])

        # Rotate the X Y and Z axis according to the quaternion q
        x = q.rotate(x)
        y = q.rotate(y)
        z = q.rotate(z)
        print('q: {}'.format(q))

        ax.clear()
        ax.quiver(0, 0, 0, x[0], x[1], x[2], length=0.1, normalize=True, color='red')
        ax.quiver(0, 0, 0, y[0], y[1], y[2], length=0.1, normalize=True, color='green')
        ax.quiver(0, 0, 0, z[0], z[1], z[2], length=0.1, normalize=True, color='blue')
        # ax.quiver(0, 0, 0, -data[i][8], -data[i][9], -data[i][10], length=0.1, normalize=True, color='magenta')

        print('\nRotated Output:')
        print('x: {0} y: {1} z: {2}'.format(x, y, z))


# Set up formatting for the movie files
writer = animation.PillowWriter(fps=10)
ani = animation.FuncAnimation(fig, animate, fargs=(x_axis, y_axis, z_axis), frames=900)
# ani.save('c://Users/{}/Desktop/animation.gif'.format(getpass.getuser()), writer=writer)
plt.show()
