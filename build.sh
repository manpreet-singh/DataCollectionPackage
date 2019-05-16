#!/bin/bash

echo "Transferring Project dir over SCP."
scp BEMO.py pi@raspberrypi:/home/pi/Documents/Workspace/
ssh -ttt pi@raspberrypi "cd ~/Documents/Workspace/; sudo python BEMO.py"

echo
echo
echo "Retrieving Data"
scp pi@raspberrypi:/home/pi/Documents/Workspace/data.csv data.csv

cp data.csv "C:\Users\Manpreet Singh\Documents\MATLAB\data.csv"