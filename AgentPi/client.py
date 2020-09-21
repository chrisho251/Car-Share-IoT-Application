import socket
import socket_utils

class Client:
    """Client class to send data through socket from AP"""
    HOST = ""
    PORT = 65000         # The port used by the server.
    ADDRESS = (HOST, PORT)

    def send_data(self, obj):
        """Function to send json through socket"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(self.ADDRESS))
            s.connect(self.ADDRESS)
            print("Connected.")

            socket_utils.sendJson(s,obj)
            data = s.recv(4096)
            print("Data received")
        return data

    def validate(self, email, password):
        """Function to request validation from server"""
        obj = {"req": "validate", "email": email, "password": password}
        return self.send_data(obj)

    def validate_mac(self, mac_add, email):
        """Function to request validation from server using mac address"""
        obj = {"req": "validate_mac", "mac_address": mac_add, "email": email}
        return self.send_data(obj)

    def validate_qr(self, email):
        """Function to request validation from server using QR code"""
        obj = {"req": "validate_qr", "email": email}
        return self.send_data(obj)

    def return_car(self, car_id):
        """Function to request change to car's availability"""
        obj = {"req": "return", "car_id": car_id}
        return self.send_data(obj)

if __name__ == "__main__":
    client = Client()
    client.send_data("haha")
