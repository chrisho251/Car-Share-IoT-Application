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


class qr_auth:

    def create_qr(self, message):
        try:
            qr_code = qrcode.make(message)
            qr_code.save("/qrimages/")
            return True
        except:
            return False

    def read_qr(self):
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
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                # if the barcode text has not been seen before print it and update the set
                if barcodeData not in found:
                    print("[FOUND] Type: {}, Data: {}".format(
                        barcodeType, barcodeData))
                    found.add(barcodeData)

            # wait a little before scanning again
            time.sleep(1)

        # close the output CSV file do a bit of cleanup
        print("[INFO] cleaning up...")
        vid_stream.stop()

if __name__ == "__main__":
    qrauth = qr_auth()
    qrauth.read_qr()
