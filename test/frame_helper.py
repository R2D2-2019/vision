""" This module acts as a helper script for putting a frame on the R2D2 Python
CAN bus. """

from client.comm import Comm
from common.frames import FrameQrcodeData

STRING = "TEST"
WIDTH, HEIGHT = 200, 100
X, Y = 5, 5
DISTANCE = 20


def create_frame(string, width, height, x, y, distance):
    """ Helper function for creating a new CAN bus frame. 
    :param string: string message you want to send.
    :param width: width of the qr code in pixels.
    :param height: height of the qr code in pixels.
    :param x: center pixel coordinate on the x axis.
    :param y: center pixel coordinate on the y axis.
    param distance: distance in milimeter to the QR code.
    :return: Ret urns the created frame. """
    frame = FrameQrcodeData()
    byte_string = bytes(string, 'utf-8')
    frame.set_data(byte_string, width, height, x, y, distance)
    return frame


def main():
    """ Main function that gets executed when we call the script,
    probably from a subprocess. """
    comm = Comm()
    frame = create_frame(STRING, WIDTH, HEIGHT, X, Y, DISTANCE)
    comm.send(frame)
    comm.stop()


main()
