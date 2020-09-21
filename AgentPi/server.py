import socket
import json
import requests
import socket_utils


class Server:
    """Server class to receive json and send appropriate data back to AP"""
    # Empty string means to listen on all IP's on the machine, also works with IPv6.
    HOST = ""
    # Note "0.0.0.0" also works but only with IPv4.
    PORT = 65000  # Port to listen on (non-privileged ports are > 1023).
    ADDRESS = (HOST, PORT)
    test = {"email": "giaminhphamle@gmail.com",
            "password": "696969", "mac_address": "B0:55:08:D5:86:71"}

    def receive_data(self):
        """Function to receive json from AP"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDRESS)
            s.listen()

            print("Listening on {}...".format(self.ADDRESS))

            while True:
                print("Waiting..")
                conn, addr = s.accept()
                with conn:
                    print("Connected to {}\n".format(addr))
                    data = socket_utils.receiveJson(conn)
                    if(not data):
                        break
                    print("Sending data back..")

                    if data["req"] == "validate":
                        msg = self.validate(data["email"], data["password"])
                        conn.sendall(msg.encode("utf-8"))
                    elif data["req"] == "validate_mac":
                        msg = self.validate_mac(
                            data["mac_address"], data["email"])
                        conn.sendall(msg.encode("utf-8"))
                    elif data["req"] == "validate_qr":
                        msg = self.validate_qr(data["email"])
                        conn.sendall(msg.encode("utf-8"))
                    elif data["req"] == "return":
                        msg = self.return_car(data["car_id"])
                        conn.sendall(msg.encode("utf-8"))
                    else:
                        conn.sendall("Invalid user".encode("utf-8"))

                print("Disconnecting from client..")
            print("Closing listening socket..")
        print("Done!")

    def validate(self, email, password):
        """Function to validate user by email and password"""
        # res = requests.get("http://localhost:8080/api/userbyemail/"+email)
        # data = res.json()
        # if not bool(data):
        #     if data["password"] == password.decode("utf-8"):
        #         return "valid"
        #     else:
        #         return "invalid"
        # else:
        #     return "invalid"
        if self.test["email"] == email:
            if self.test["password"] == password:
                return "valid"
            else:
                return "invalid"
        else:
            return "invalid"

    def validate_mac(self, mac_add, email):
        """Function to validate user by email and mac address"""
        # res = requests.get("http://localhost:8080/api/userbyemail/"+email)
        # data = res.json()
        # if not bool(data):
        #     if data["mac_address"] == mac_add.decode("utf-8"):
        #         return "valid"
        #     else:
        #         return "invalid"
        # else:
        #     return "invalid"
        if self.test["mac_address"] == mac_add:
            return "valid"
        else:
            return "invalid"

    def validate_qr(self, email):
        """Function to validate user by email through QR code"""
        res = requests.get("http://localhost:8080/api/userbyemail/"+email)
        data = res.json()
        if not bool(data):
            return "valid"
        else:
            return "invalid"

    def return_car(self, car_id):
        """Function to update car's availability"""
        # res = requests.get("http://localhost:8080/api/cars/"+car_id)
        # data = res.json()
        # res2 = requests.put("http://localhost:8080/api/userbyemail/"+email)
        return "success"

if __name__ == "__main__":
    server = Server()
    server.receive_data()
