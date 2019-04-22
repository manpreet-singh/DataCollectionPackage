#!/bin/bash

echo "Transferring Project dir over SCP."
scp BEMO.py pi@192.168.137.50:/home/pi/Documents/Workspace/
ssh pi@192.168.137.50 "cd ~/Documents/Workspace/; sudo python BEMO.py"

echo "\nRetrieving Data"
scp pi@192.168.137.50:/home/pi/Documents/Workspace/data.csv data.csv