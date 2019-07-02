""" Provides a class in which to save QR code data."""

from math import sqrt


class Coordinate:
    """ This class is used to represent x and y values of a coordiante. """

    def __init__(self, x=0, y=0):
        """ The constructor.
        :param x: X value of the coordiante. 
        :param y: Y value of the coordiante.
        :return: Nothing.
        """
        self.x = x
        self.y = y

    def __repr__(self):
        """ Represents the coordinate
        :return: Returns a string with the x and y values.
        """
        return "({}, {})".format(repr(self.x), repr(self.y))

    def __eq__(self, other):
        """Override the default equals operator"""
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return False


class Line:
    """ This class is used to represent two points of a line. """

    def __init__(self, p1=Coordinate(), p2=Coordinate()):
        """ The constructor.
        :param p1: First coordinate of the line. Default = empty coordinate. 
        :param p2: Second coordinate of the line. Default = empty coordinate.
        :return: Nothing.
        """
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        """ Represents the line
        :return: Returns a string with the two coordinates.
        """
        return "{}, {}".format(repr(self.p1), repr(self.p2))

    def __eq__(self, other):
        """Override the default equals operator"""
        if isinstance(other, self.__class__):
            return self.p1 == other.p1 and self.p2 == other.p2
        return False


class QrPolygon:
    """ This class extends the information one gets from the pyzbar polygon."""

    def __init__(self, polygon):
        """ The constructor.

        It creates a lot of lines and calls the calculate_polygon_properties function to calculate more information.
        :param polygon: Either a pyzbar polygon from a qr code, or a list with four coordinates.
        :return: Nothing.
        """
        self.top_left_point = Coordinate(polygon[0].x, polygon[0].y)
        self.bottom_left_point = Coordinate(polygon[1].x, polygon[1].y)
        self.bottom_right_point = Coordinate(polygon[2].x, polygon[2].y)
        self.top_right_point = Coordinate(polygon[3].x, polygon[3].y)

        self.diagonal_tl_br_line = Line(
            self.top_left_point, self.bottom_right_point)
        self.diagonal_tr_bl_line = Line(
            self.top_right_point, self.bottom_left_point)

        self.top_line = Line(self.top_left_point, self.top_right_point)
        self.bottom_line = Line(self.bottom_left_point,
                                self.bottom_right_point)
        self.left_line = Line(self.top_left_point, self.bottom_left_point)
        self.right_line = Line(self.top_right_point, self.bottom_right_point)

        self.center_point = Coordinate()
        self.upper_middle_point = Coordinate()
        self.lower_middle_point = Coordinate()
        self.left_middle_point = Coordinate()
        self.right_middle_point = Coordinate()
        self.middle_height_line = Line()
        self.middle_width_line = Line()
        self.middle_height = 0
        self.middle_width = 0

        self.horizontal_vanish_point = None
        self.vertical_vanish_point = None

        self.horizontal_center_line = Line()
        self.vertical_center_line = Line()

        self.calculate_polygon_properties()

    def line_intersection(self, line_1, line_2):
        """ Calculates the intersection coordinate of two lines.
        :param line_1: A line.
        :param line_2: A line.
        :return: Coordinate of the intersection point.
        :return: Nothing if no point is found.
        """
        x_diff = Coordinate(line_1.p1.x - line_1.p2.x,
                            line_2.p1.x - line_2.p2.x)
        y_diff = Coordinate(line_1.p1.y - line_1.p2.y,
                            line_2.p1.y - line_2.p2.y)

        def det(a, b):
            # Because this function is only used in this particular function,
            # the choice was made to nest this det function in the function
            # that uses it, instead of making it a private class function and
            # to never be used again.
            return a.x * b.y - a.y * b.x

        div = det(x_diff, y_diff)
        if div == 0:
            return None

        d = Coordinate(det(line_1.p1, line_1.p2), det(line_2.p1, line_2.p2))
        x = det(d, x_diff) / div
        y = det(d, y_diff) / div
        return Coordinate(x, y)

    def calculate_polygon_properties(self):
        """ Calculates a lot of polygon properties.
        Calculates the coordinates of the center, the midpoints of the outer boundries, and, if possible, vanish points.
        Calculates the middle height and width line.
        Calculates the height and with of the polygon.
        :return: Nothing.
        """
        self.__calculate_center_point()
        self.__calculate_vanishing_points()
        self.__calculate_vahish_lines()
        self.__calculate_mid_points()
        self.__calculate_mid_lines()
        self.__calculate_middle_height_width()

    def __calculate_center_point(self):
        self.center_point = self.line_intersection(
            self.diagonal_tl_br_line, self.diagonal_tr_bl_line)

    def __calculate_vanishing_points(self):
        self.horizontal_vanish_point = self.line_intersection(
            self.top_line, self.bottom_line)
        self.vertical_vanish_point = self.line_intersection(
            self.left_line, self.right_line)

    def __calculate_vahish_lines(self):
        if self.horizontal_vanish_point:
            self.horizontal_center_line = Line(
                self.center_point, self.horizontal_vanish_point)
        else:
            self.horizontal_center_line = Line(self.center_point, Coordinate(
                self.center_point.x + 10, self.center_point.y))

        if self.vertical_vanish_point:
            self.vertical_center_line = Line(
                self.center_point, self.vertical_vanish_point)
        else:
            self.vertical_center_line = Line(self.center_point, Coordinate(
                self.center_point.x, self.center_point.y + 10))

    def __calculate_mid_points(self):
        self.upper_middle_point = self.line_intersection(
            self.vertical_center_line, self.top_line)
        self.lower_middle_point = self.line_intersection(
            self.vertical_center_line, self.bottom_line)
        self.left_middle_point = self.line_intersection(
            self.horizontal_center_line, self.left_line)
        self.right_middle_point = self.line_intersection(
            self.horizontal_center_line, self.right_line)

    def __calculate_mid_lines(self):
        self.middle_height_line = Line(
            self.upper_middle_point, self.lower_middle_point)
        self.middle_width_line = Line(
            self.left_middle_point, self.right_middle_point)

    def __calculate_middle_height_width(self):
        try:
            self.middle_height = sqrt(((self.middle_height_line.p1.x - self.middle_height_line.p2.x) ** 2) + (
                (self.middle_height_line.p1.y - self.middle_height_line.p2.y) ** 2))
            self.middle_width = sqrt(((self.middle_width_line.p1.x - self.middle_width_line.p2.x)
                                      ** 2) + ((self.middle_width_line.p1.y - self.middle_width_line.p2.y) ** 2))
        except AttributeError:
            pass


class QrCode:
    """ This class is used to store QR code data and do some simple calculations."""

    def __init__(self, code):
        """ The constructor.
        :param code: A pyzbar decoded qrcode.
        """
        self.data = None
        self.type = code.type
        self.rect = code.rect
        self.polygon = QrPolygon(code.polygon)
        self.center_distance = None
        self.center_offset = list()
        self.center_offset_mm = list()

        self.parse_data(code.data.decode("utf-8"))

    def calculate_center_distance(self, camera_properties, frame_height):
        """ Calculate the distance between the QR code and the camera.
        :param camera_properties: Properties of the camera used in making the frame/picture.
        :param frame_height: Height of the frame/picture in which the QR code is found.
        :return: Nothing.
        """
        try:
            distance_to_object = (camera_properties.get_focal_length() * int(self.get_value("Height"))
                                  * frame_height) / (self.polygon.middle_height * camera_properties.get_sensor_height())
            self.center_distance = distance_to_object
        # Sometimes something goes wrong in calculating the distance
        # resulting in an ZeroDivisionError.
        # If this is the case nothing should happen.
        # Else the program will crash.
        except ZeroDivisionError:
            self.center_distance = None

    def calculate_center_offset(self, frame_width, frame_height):
        """ Calculates the offset of the QR code relative to the center of the frame/image.
        :param frame_width: Width of the frame/image.
        :param frame_height: Height of the frame/image.
        :return: Nothing.
        """
        qr_center = self.polygon.center_point
        offset_x = qr_center.x - frame_width/2
        offset_y = qr_center.y - frame_height/2
        self.center_offset = [offset_x, offset_y]

        # if possible calculate the physical offset in millimeters
        try:
            offset_x_mm = (self.get_value("Height") *
                           offset_x) / self.polygon.middle_width
            offset_y_mm = (self.get_value("Width") *
                           offset_y) / self.polygon.middle_height
            self.center_offset_mm = [offset_x_mm, offset_y_mm]
        except TypeError:
            pass

    def get_qr_center(self):
        """ Gets the center coordinates of the QR code.
        :return: QR center coordiantes.
        """
        return self.polygon.center_point

    def get_center_offset(self):
        """ Gets the offset of the center of the QR code relative of the center of the image.
        :return: Center offset.
        """
        if self.center_offset:
            return self.center_offset
        return None

    def get_center_offset_mm(self):
        """ Gets the offset of the center of the QR code relative of the center of the image in millimeters.
        :return: Center offset in millimeters.
        """
        if self.center_offset_mm:
            return self.center_offset_mm
        return None

    def get_center_distance(self):
        """ Gets the distance of the QR code relative to the camera sensor.
        :return: Distance to camera censor in mm.
        """
        if self.center_distance:
            return self.center_distance
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
