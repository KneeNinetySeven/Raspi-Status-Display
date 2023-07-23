#!/bin/bash

systemctl is-active --quiet display
serviceStatus=$?

echo ++     Pulling changes from GitHub
git checkout . #To avoid any git issues, no local changes should be made when using the update script.
git pull
echo

echo ++     Installing python dependencies
sudo -H pip3 install -r requirements.txt
echo

echo ++     Reload system daemons
sudo systemctl daemon-reload 
echo

if [[ serviceStatus -eq 0 ]]
then
    echo ++     System service in use. Restarting...
    sudo systemctl restart display
    echo 
else 
    echo ++     System service inactive. 
    echo 
fi

echo "UPDATE FINISHED."