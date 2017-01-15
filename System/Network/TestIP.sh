#!/bin/bash

TestIP="192.168.88.199"

# Loop forever (until break is issued)
while true; do

    # Do a simple test for Internet connectivity
    PacketLoss=$(ping "$TestIP" -c 2 | grep -Eo "[0-9]+% packet loss" | grep -Eo "^[0-9]")

    # Exit the loop if ping is no longer dropping packets
    if [ "$PacketLoss" == 0 ]; then
        echo "Connection restored"
        break
    else
        echo "No connectivity"
    fi
done
