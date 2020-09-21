#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/struct.html
import socket, json, struct, sys, os

# This method is used to send the json over socket
def sendJson(sock, obj):
    """ This method is used to send the json over socket
    :param (object)object
    """
    json_string = json.dumps(obj)
    data = json_string.encode("utf-8")
    json_length = struct.pack("!i", len(data))
    sock.sendall(json_length)
    sock.sendall(data)

# This method is used to receive a json from socket
def receiveJson(sock):
    """ This method is used to receive a json from socket
    :param (object)socket
    """
    buffer = sock.recv(4)
    if buffer:
        print('Data received')
        json_length = struct.unpack("!i", buffer)[0]
        # Reference: https://stackoverflow.com/a/15964489/9798310
        buffer = bytearray(json_length)
        view = memoryview(buffer)
        while json_length:
            nbytes = sock.recv_into(view, json_length)
            view = view[nbytes:]
            json_length -= nbytes

        json_string = buffer.decode("utf-8")
        return json.loads(json_string)
