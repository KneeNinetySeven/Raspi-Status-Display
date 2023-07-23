# Raspi-Status-Display

A small utility to run on RaspberryPis and display some general purpose pages with host information. 

Suits up well, with my custom 3D printable RaspberryPi Rack Storage [here](https://www.printables.com/de/model/352578-triple-raspberrypi-rack-mount):

[<img src="doc/rackmount_photo.webp" width=80% />](https://www.printables.com/de/model/352578-triple-raspberrypi-rack-mount). 


## Output On Display
The generated output will look like this (as of 05/2023):

![](doc/pages/pages.gif) 

## Sequence
![](doc/pages/Host_Info.png) 
![](doc/pages/Sys_Load.png) 
![](doc/pages/Disk.png) 
![](doc/pages/CPU_Temp.png)

## Installation 
`$> curl -sSL https://raw.githubusercontent.com/KneeNinetySeven/Raspi-Status-Display/main/setup.sh | bash`

## Configuration

Currently supported: SSD1306 compatible with size
WIDTH = 128 
and
HEIGHT = 64
