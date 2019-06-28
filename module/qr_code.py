""" Provides a class in which to save QR code data."""


class QrCode:
    """ This class is used to store QR code data and do some simple calculations."""

    def __init__(self, code):
        """ The constructor.
        :param code: A pyzbar decoded qrcode.
        """
        self.data = None
        self.type = code.type
        self.rect = code.rect
        self.polygon = code.polygon
        self.distance = None
        self.center_offset = list()

        self.parse_data(code.data.decode("utf-8"))

    def calculate_distance(self, camera_properties, frame_height):
        """ Calculate the distance between the QR code and the camera.
        :param camera_properties: Properties of the camera used in making the frame/picture.
        :param frame_height: Height of the frame/picture in which the QR code is found.
        :return: Nothing.
        """
        try:
            distance_to_object = (camera_properties.get_focal_length() * int(self.get_value("Height"))
                                  * frame_height) / (self.rect.height * camera_properties.get_sensor_height())
            self.distance = distance_to_object
        # Sometimes something goes wrong in calculating the distance
        # resulting in an ZeroDivisionError.
        # If this is the case nothing should happen.
        # Else the program will crash.
        except:
            self.distance = None

    def calculate_center_offset(self, frame_width, frame_height):
        """ Calculates the offset of the QR code relative to the center of the frame/image.
        :param frame_width: Width of the frame/image.
        :param frame_height: Height of the frame/image.
        :return: Nothing.
        """
        qr_center = self.get_qr_center()
        offset_x, offset_y, = qr_center[0] - \
            frame_width/2, qr_center[1] - frame_height/2
        self.center_offset = [offset_x, offset_y]

    def get_qr_center(self):
        """ Gets the center coordinates of the QR code.
        :return: QR center coordiantes.
        """
        (x, y, w, h) = self.rect
        center_x, center_y = x+(w/2), y+(h/2)
        return [center_x, center_y]

    def get_center_offset(self):
        """ Gets the offset of the center of the QR code relative of the center of the image.
        :return: Center offset.
        """
        if self.center_offset:
            return self.center_offset
        return None

    def get_distance(self):
        """ Gets the distance of the QR code relative to the camera sensor.
        :return: Distance to camera censor in mm.
        """
        if self.distance:
            return self.distance
        return None

    def get_value(self, key):
        """ Gets the desired value from the data dictionary.
        :param key: The key to look for. 
        :return: Data value or None if key was not found.
        """
        if key in self.data:
            return self.data[key]
        return None

    def parse_data(self, unrefined_data):
        """ Parses the data of the QR code
        :param unrefined_data: A string of data to parse.
        :return: Nothing.
        """
        data_dict = dict()
        data_splits = unrefined_data.split(",")
        for data_split in data_splits:
            data = data_split.split(":")
            data_dict[data[0]] = data[1]
        self.data = data_dict
