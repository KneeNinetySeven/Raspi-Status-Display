#!/bin/bash

echo ++     Stopping the display service during the update
sudo systemctl stop display 
echo 

echo ++     Pulling changes from GitHub
git checkout . #To avoid any git issues, no local changes should be made when using the update script.
git pull
echo

echo ++     Installing python dependencies
sudo -H pip3 install -r requirements.txt
echo

echo ++     reload system daemons and restart display
sudo systemctl daemon-reload 
sudo systemctl restart display
echo

echo "UPDATE FINISHED."