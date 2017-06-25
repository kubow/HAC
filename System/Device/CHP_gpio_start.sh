#!/bin/bash

# Enable pin exposure 
gpio_enable()
{
	echo "hooray"
}

sudo sh -c 'echo 408 > /sys/class/gpio/export'
sudo sh -c 'echo 409 > /sys/class/gpio/export'
