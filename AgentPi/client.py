import socket

class Client:  
    HOST = input("Enter IP address of server: ")
    PORT = 65000         # The port used by the server.
    ADDRESS = (HOST, PORT)

    def send_data(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(self.ADDRESS))
            s.connect(self.ADDRESS)
            print("Connected.")

            s.sendall(message.encode("utf-8"))
            data = s.recv(4096)
            print("Received {} bytes of data decoded to: '{}'".format(
                len(data), data.decode("utf-8")))
        return data

if __name__ == "__main__":
    client = Client()
    client.send_data("haha")