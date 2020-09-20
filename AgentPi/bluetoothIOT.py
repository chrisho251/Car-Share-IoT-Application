#!/usr/bin/env python3
#reference : code from the lecture
import bluetooth
import os
import time
from sense_hat import SenseHat

# Main function
def main():
    user_name = input("Enter your name: ")
    device_name = input("Enter the name of your phone: ")
    search(user_name, device_name)
    
# Search for device based on device's name
def search(user_name, device_name):
    while True:
        device_address = None
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        time.sleep(3) #Sleep three seconds 
        nearby_devices = bluetooth.discover_devices()

        for mac_address in nearby_devices:
            if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                device_address = mac_address
                break
        if device_address is not None:
            print("Hi {}! Your phone ({}) has the MAC address: {}".format(user_name, device_name, device_address))
            sense = SenseHat()
            temp = round(sense.get_temperature()-0.1, 2)
            if temp <40.60 :
                sense.show_message("Temperature lower than min temperature")
            elif temp >= 40.60 and temp <= 40.80:
                sense.show_message("Hi {}! Current Temp is {}*c".format(user_name, temp), scroll_speed=0.05)
            else:
                sense.show_message("Temperature higher than min temperature")
        else:
            print("Could not find target device nearby...")

#Execute program
main()
