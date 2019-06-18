from qr_code import QrCode
from pyzbar import pyzbar


class QrReader:
    def __init__(self):
        self.codes = list()

    def read_qr_codes(self, frame, camera_properties=None):
        codes = pyzbar.decode(frame)

        # Create the qrcodes
        for code in codes:
            self.codes.append(QrCode(code))
        # Calculate distance if possible
        if camera_properties:
            for code in self.codes:
                print("Frame height: {}".format(frame.shape[0]))
                code.calculate_distance(camera_properties, frame.shape[0])

    def get_qr_codes(self):
        if self.codes:
            return self.codes
        return None
