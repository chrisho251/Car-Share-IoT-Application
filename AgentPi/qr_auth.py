# USAGE
# python3 barcode_scanner_console.py

# Acknowledgement
# This code is adapted from:
# https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
# pip3 install pyzbar

# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import qrcode


class Qr_auth:
    """QR class for QR code authentication"""

    def create_qr(self, message):
        """Function to create QR code"""
        try:
            qr_code = qrcode.make(message)
            qr_code.save("/")
            return True
        except:
            return False

    def read_qr(self):
        """Function to read QR code from IP Webcam"""
        # initialize the video stream and allow the camera sensor to warm up
        print("Looking for valid QR code...")
        vid_stream = VideoStream("http://10.247.193.162:8080/video").start()
        time.sleep(2.0)

        found = set()

        # loop over the frames from the video stream
        while True:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = vid_stream.read()
            frame = imutils.resize(frame, width=400)

            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)

            # loop over the detected barcodes
            for barcode in barcodes:
                # the barcode data is a bytes object so we convert it to a string
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type

                # if the barcode text has not been seen before print it and update the set
                if barcode_data not in found:
                    print("[FOUND] Type: {}, Data: {}".format(
                        barcode_type, barcode_data))
                    found.add(barcode_data)
                    return barcode_data

            # wait a little before scanning again
            time.sleep(1)

        # close the output CSV file do a bit of cleanup
        print("[INFO] cleaning up...")
        vid_stream.stop()
        return barcode_data

if __name__ == "__main__":
    qrauth = Qr_auth()
    qrauth.create_qr("giaminhphamle@gmail.com")
