#!/usr/bin/env python3
#reference : code from the lecture
import time
import bluetooth
from sense_hat import SenseHat
from client import Client

class BluetoothIOT:
    # Main function
    def main(self):
        user_name = input("\nEnter your email: ")
        device_name = input("Enter the name of your phone: ")
        return self.search(user_name, device_name)
        
    # Search for device based on device's name
    def search(self,user_name, device_name):
        while True:
            device_address = None
            print("Searching for device..")
            time.sleep(2) #Sleep 2 seconds 
            nearby_devices = bluetooth.discover_devices()

            for mac_address in nearby_devices:
                if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                    device_address = mac_address
                    break
            if device_address is not None:
                print("Hi {}! Your phone ({}) has the MAC address: {}".format(user_name, device_name, device_address))
                return {"mac_address": device_address, "email": user_name}
            else:
                print("Could not find target device nearby...")
                return ""

if __name__ == "__main__":
    blu = BluetoothIOT()
    blu.main()
