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
&& sudo apt install python3 python3-pip i2c-tools python3-pip libopenjp2-7 -y
echo

echo ++    Searching for I2C devices...
sudo i2cdetect -y 1
echo


echo ++     Installing basic python dependencies
pip install smbus adafruit-circuitpython-ssd1306 pillow==8.2.0 numpy adafruit-blinka psutil
