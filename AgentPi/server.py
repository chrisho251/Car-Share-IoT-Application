import socket, json, requests
import socket_utils

class Server:
    HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
                 # Note "0.0.0.0" also works but only with IPv4.
    PORT = 65000 # Port to listen on (non-privileged ports are > 1023).
    ADDRESS = (HOST, PORT)
    username = ""
    password = ""

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
                    print("Received data decoded to: '{}'\n".format(data["mac-address"]))
                    print("Sending data back..")
                    if data["req"] == "validate":
                        self.validate(data["username"], data["password"])
                    else:
                        conn.sendall("Invalid user".encode("utf-8"))

                print("Disconnecting from client..")
            print("Closing listening socket..")
        print("Done!")

    def validate(self, username, password):


if __name__ == "__main__":
    server = Server()
    server.receive_data()
