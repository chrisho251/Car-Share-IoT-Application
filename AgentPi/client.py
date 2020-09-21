import socket
import socket_utils

class Client:
    HOST = input("Enter IP address of server: ")
    PORT = 65000         # The port used by the server.
    ADDRESS = (HOST, PORT)

    def send_data(self, obj):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(self.ADDRESS))
            s.connect(self.ADDRESS)
            print("Connected.")

            socket_utils.sendJson(s,obj)
            data = s.recv(4096)
            print("Received {} bytes of data decoded to: '{}'".format(
                len(data), data.decode("utf-8")))
        return data

    def validate(self, email, password):
        obj = {"req": "validate", "email": email, "password": password}
        return self.send_data(obj)

    def validate_mac(self, mac_add):
        obj = {"req": "validate_mac", "mac_address": mac_add}
        return self.send_data(obj)

if __name__ == "__main__":
    client = Client()
    client.send_data("haha")
