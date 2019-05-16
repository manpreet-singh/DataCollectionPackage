import logging
import sys
import signal
import time

import csv

from Adafruit_BNO055 import BNO055
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)

GPIO.output(17, GPIO.LOW)
time.sleep(0.5)
GPIO.output(17, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(17, GPIO.LOW)
time.sleep(0.5)
GPIO.output(17, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(17, GPIO.LOW)

# Create and configure the BNO sensor connection.
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

iterations = 0

data_file = open("data.csv", mode='w')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

print('Reading BNO055 data, press Ctrl-C to quit...')


def power_off(sig, frame):
    GPIO.output(17, GPIO.LOW)
    sys.exit(0)


signal.signal(signal.SIGINT, power_off)
# signal.signal(signal.SIGKILL, power_off)
# signal.pause()

GPIO.output(17, GPIO.HIGH)
start = time.time()
while True:
    t = time.time() - start
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Other values you can optionally read:
    # Orientation as a quaternion:
    # x,y,z,w = bno.read_quaterion()
    # Sensor temperature in degrees Celsius:
    # temp_c = bno.read_temp()
    # Magnetometer data (in micro-Teslas):
    mag_x, mag_y, mag_z = bno.read_magnetometer()
    # Gyroscope data (in degrees per second):
    # x,y,z = bno.read_gyroscope()
    # Accelerometer data (in meters per second squared):
    accel_x, accel_y, accel_z = bno.read_accelerometer()
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    lin_accel_x, lin_accel_y, lin_accel_z = bno.read_linear_acceleration()
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    # x,y,z = bno.read_gravity()
    # Sleep for a second until the next reading.

    if not accel < 2:
        data_writer.writerow([t, heading, roll, pitch, accel_x, accel_y, accel_z, mag_x, mag_y, mag_z, lin_accel_x,
                              lin_accel_y, lin_accel_z])

        # Print everything out.
        print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F} acc_x={3:0.2F} acc_y={4:0.2F} acc_z={5:0.2F}'.format(
            heading, roll, pitch, lin_accel_x, lin_accel_y, lin_accel_z))

    else:
        print("Calibrating ...")
        print('sys: {0} gyro: {1} accel: {2} mag: {3}'.format(sys, gyro, accel, mag))
