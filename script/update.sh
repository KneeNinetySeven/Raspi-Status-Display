#!/bin/bash

echo ++     Pulling changes from GitHub
git pull
echo

echo ++     Installing python dependencies
sudo -H pip install -r requirements.txt
echo

echo ++     reload system daemons and restart display
sudo systemctl daemon-reload 
sudo systemctl restart display
echo

echo "UPDATE FINISHED."