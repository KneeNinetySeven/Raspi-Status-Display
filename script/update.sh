#!/bin/bash

echo ++     Pulling changes from GitHub
git pull
echo

echo ++     Installing python dependencies
sudo -H pip install -r requirements.txt
echo

sudo systemctl daemon-reload && sudo systemctl restart display