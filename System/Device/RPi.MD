#Raspberry Pi
https://www.youtube.com/watch?v=Ykx9eacAwIM
https://www.webnist.de/temperatur-sensor-ds1820-am-raspberry-pi-mit-python/

GPIO
https://www.raspberrypi.org/documentation/usage/gpio-plus-and-raspi2/README.md

sudo lsmod
sudo modprobe wire 
sudo modprobe w1-gpio 
sudo modprobe w1-therm
add to
sudo nano /etc/modules
sudo nano /boot/config.txt
# Temperatursensor an 1-Wire
dtoverlay=w1-gpio
gpiopin=4
sensor located at /sys/bus/w1/devices/xxxxxxx