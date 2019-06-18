""" Provides a class in which to save qr code data."""


class QrCode:
    """ This class is used to store qr code data and do some simple calculations."""

    def __init__(self, code):
        """ The constructor.
        :param code: A pyzbar decoded qrcode.
        """
        self.data = None
        self.type = code.type
        self.rect = code.rect
        self.polygon = code.polygon
        self.distance = None
        self.parse_data(code.data.decode("utf-8"))

    def calculate_distance(self, camera_properties, frame_height):
        """ Calculate the distance between the qrcode and the camera.
        :param camera_properties: Properties of the camera used in making the frame/picture.
        :param frame_height: Height of the frame/picture in which the qrcode is found.
        :return: Nothing.
        """
        try:
            distance_to_object = (camera_properties.get_focal_length() * self.get_height(
            ) * frame_height) / (self.rect.height * camera_properties.get_sensor_height())
            self.distance = distance_to_object
        # Sometimes something goes wrong in calculating the distance
        # resulting in an ZeroDivisionError.
        # If this is the case nothing should happen.
        # Else the program will crash.
        except ZeroDivisionError:
            self.distance = None

    def get_height(self):
        """ Gets height measurement of the qr code.
        This height value is stored inside of the qr code itself.
        :return: Qr code height.
        """
        try:
            return int(self.data["Height"])
        except ValueError:
            return None

    def parse_data(self, unrefined_data):
        """ Parses the data of the qr code
        :param unrefined_data: A string of data to parse.
        :return: Nothing.
        """
        data_dict = dict()
        data_splits = unrefined_data.split(",")
        for data_split in data_splits:
            data = data_split.split(":")
            data_dict[data[0]] = data[1]
        self.data = data_dict
