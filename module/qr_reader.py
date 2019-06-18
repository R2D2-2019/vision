"""Provides an interface to get QR codes from an image"""

from pyzbar import pyzbar
from modules.vision.module.qr_code import QrCode


class QrReader:
    """ The QrReader class reads the QR codes from a frame"""

    def __init__(self):
        """ The contstructor.
        It creates a list for the QR codes to be put into.
        """
        self.codes = list()

    def read_qr_codes(self, frame, camera_properties=None):
        """ Reads the QR codes in the frame.
        :param frame: The image from which the qrcodes must be read.
        :param camera_properties: The properties of the camera.  
        :return: Nothing.
        """
        self.codes = list()
        codes = pyzbar.decode(frame)
        # Create the qrcodes
        for code in codes:
            new_code = QrCode(code)
            new_code.calculate_center_offset(frame.shape[1], frame.shape[0])
            self.codes.append(new_code)
        # Calculate distance if possible
        if camera_properties:
            for code in self.codes:
                code.calculate_distance(camera_properties, frame.shape[0])

    def get_qr_codes(self):
        """ Gets the QR codes found in the frame.
        :return: Returns a list of found qr codes.
        """
        if self.codes:
            return self.codes
        return None
