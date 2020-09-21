import socket, json, requests
import socket_utils

class Server:
    HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
                 # Note "0.0.0.0" also works but only with IPv4.
    PORT = 65000 # Port to listen on (non-privileged ports are > 1023).
    ADDRESS = (HOST, PORT)
    test = {"email": "giaminhphamle@gmail.com", "password": "696969"}

    def receive_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDRESS)
            s.listen()

            print("Listening on {}...".format(self.ADDRESS))
            conn, addr = s.accept()
            with conn:
                print("Connected to {}\n".format(addr))

                while True:
                    data = socket_utils.receiveJson(conn)
                    if(not data):
                        break
                    print("Received data")
                    print("Sending data back..")
                    
                    if data["req"] == "validate":
                        msg = self.validate(data["email"], data["password"])
                        conn.sendall(msg.encode("utf-8"))
                    elif data["req"] == "validate_mac":
                        msg = self.validate_mac(data["mac_address"])
                    else:
                        conn.sendall("Invalid user".encode("utf-8"))

                print("Disconnecting from client..")
            print("Closing listening socket..")
        print("Done!")

    def validate(self, email, password):
        # res = requests.get("http://localhost:8080/api/userbyemail/"+email)
        # data = res.json()
        # if not data:
        #     return "valid"
        # else:
        #     return "invalid"
        if self.test["email"] == email:
            if self.test["password"] == password:
                return "valid"
            else:
                return "invalid"
        else:
            return "invalid"

    def validate_mac(self, mac_add):


if __name__ == "__main__":
    server = Server()
    server.receive_data()
