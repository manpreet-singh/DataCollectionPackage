import time
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
# import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)
fxos = adafruit_fxos8700.FXOS8700(i2c)
fxas = adafruit_fxas21002c.FXAS21002C(i2c)

while True:
    accel_x, accel_y, accel_z = fxos.accelerometer
    mag_x, mag_y, mag_z = fxos.magnetometer
    print('Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(accel_x, accel_y, accel_z))
    print('Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(mag_x, mag_y, mag_z))
    # Delay for a second.
    time.sleep(1.0)