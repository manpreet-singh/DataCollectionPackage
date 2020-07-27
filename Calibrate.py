import time
import logging
import sys
import os

from Adafruit_BNO055 import BNO055
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)

bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Put the sensor into the NDOF Sensor Fusion mode
bno.set_mode(BNO055.OPERATION_MODE_NDOF)

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

input("Press Enter to continue ...")

print('Reading BNO055 data, press Ctrl-C to quit...')

prevTime = 0
state = GPIO.LOW

while True:
    sys, gyro, accel, mag = bno.get_calibration_status()
    if (time.time()-prevTime) >= 0.25:
        prevTime = time.time()
        if state == GPIO.HIGH:
            state = GPIO.LOW
        else:
            state = GPIO.HIGH

    print('sys: {0} gyro: {1} accel: {2} mag: {3}'.format(sys, gyro, accel, mag))
    GPIO.output(17, state)
