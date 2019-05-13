#!/bin/bash

echo "Transferring Project dir over SCP."
scp BEMO.py pi@raspberrypi:/home/pi/Documents/Workspace/
ssh pi@raspberrypi "cd ~/Documents/Workspace/; sudo python BEMO.py"

echo
echo
echo "Retrieving Data"
scp pi@raspberrypi:/home/pi/Documents/Workspace/data.csv data.csv