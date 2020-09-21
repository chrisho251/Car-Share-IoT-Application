#!/usr/bin/env python3
#reference : code from the lecture
import time
import bluetooth
from sense_hat import SenseHat
from client import Client

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
            client = Client()
            client.send_data({"mac-address":device_address})
            return "Success"
        else:
            print("Could not find target device nearby...")
            return "Failed"

#Execute program
main()
