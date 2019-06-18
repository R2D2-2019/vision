"""Provedes an interface to get qrcodes from an image"""

from pyzbar import pyzbar
from qr_code import QrCode


class QrReader:
    """ The QrReader class reads the qr codes from a frame"""

    def __init__(self):
        """ The contstructor.
        It creates a list for the qrcodes to be put into.
        """
        self.codes = list()

    def read_qr_codes(self, frame, camera_properties=None):
        """ Reads the qrcodes in the frame.
        :param frame: The image from which the qrcodes must be read.
        :param camera_properties: The properties of the camera.  
        :return: Nothing.
        """
        codes = pyzbar.decode(frame)

        # Create the qrcodes
        for code in codes:
            self.codes.append(QrCode(code))
        # Calculate distance if possible
        if camera_properties:
            for code in self.codes:
                code.calculate_distance(camera_properties, frame.shape[0])

    def get_qr_codes(self):
        """ Gets the qrdoes found in the frame.
        :return: Returns a list of found qr codes.
        """
        if self.codes:
            return self.codes
        return None
