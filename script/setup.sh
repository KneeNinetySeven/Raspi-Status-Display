#!/bin/bash

echo ++    I2C Checks
if [ $(sudo raspi-config nonint get_i2c) -eq 1 ]; then
	echo Enabling I2C
	sudo raspi-config nonint do_i2c 0
else
	echo I2C is already enabled
fi
sudo adduser $USER i2c
echo

echo ++    Installing dependencies
sudo apt update -y \
&& sudo apt install git python3 python3-pip i2c-tools libopenjp2-7 -y
echo

echo ++    Loading scripts...
git clone https://github.com/KneeNinetySeven/Raspi-Status-Display.git
mv Raspi-Status-Display status-display
cd status-display
echo

echo ++    Searching for I2C devices...
sudo i2cdetect -y 1
echo


echo ++     Installing basic python dependencies
sudo -H pip3 install -r requirements.txt
echo

echo ++     Installing system services
chmod +x script/setup.sh
chmod +x script/update.sh
sudo ln -s $(pwd)/display.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable display && sudo systemctl start display
touch logs/status-display.log
echo

echo '#####################################################'
echo '# Finished. Systemctl daemon is installed and running. '
echo '# You could increase the I2C bus baud rate. dtparam=...,i2c_arm_baudrate=400000 in /boot/config.txt has been tested successfully.'
echo '#####################################################'
