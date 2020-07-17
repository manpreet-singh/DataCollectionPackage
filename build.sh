#!/bin/bash

echo "Transferring Project dir over SCP."
scp DataTransmitter.py pi@raspberrypi:/home/pi/Documents/Workspace/
ssh -ttt pi@raspberrypi "cd ~/Documents/Workspace/; sudo python DataTransmitter.py"

echo
echo
echo "Retrieving Data"
scp pi@raspberrypi:/home/pi/Documents/Workspace/data.csv data.csv

#cp data.csv ~/Documents/MATLAB/data.csv