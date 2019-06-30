from math import sqrt

class Coordinate:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}, {}".format(repr(self.x), repr(self.y))

class Line:
    def __init__(self, p1 = Coordinate(), p2 = Coordinate()):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return "{}, {}".format(repr(self.p1), repr(self.p2))


class QrPolygon:
    def __init__(self, corner_points):
        self.top_left_point = corner_points[0]
        self.top_right_point = corner_points[1]
        self.bottom_left_point = corner_points[2]
        self.bottom_right_point = corner_points[3]

        self.diagonal_tl_br_line = Line(self.top_left_point, self.bottom_right_point)
        self.diagonal_tr_bl_line = Line(self.top_right_point, self.bottom_left_point)

        self.top_line = Line(self.top_left_point, self.top_right_point)
        self.bottom_line = Line(self.bottom_left_point, self.bottom_right_point)
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

        self.horizontal_vanish_point = Coordinate()
        self.vertical_vanish_point = Coordinate()

        self.horizontal_center_line = Line()
        self.vertical_center_line = Line()

        self.calculate_polygon_properties()


    def line_intersection(self, line_1, line_2):
        x_diff = Coordinate(line_1.p1.x - line_1.p2.x, line_2.p1.x - line_2.p2.x)
        y_diff = Coordinate(line_1.p1.y - line_1.p2.y, line_2.p1.y - line_2.p2.y)

        def det(a, b):
            return a.x * b.y - a.y * b.x

        div = det(x_diff, y_diff)
        if div == 0:
            return None

        d = Coordinate(det(line_1.p1, line_1.p2), det(line_2.p1, line_2.p2))
        x = det(d, x_diff) / div
        y = det(d, y_diff) / div
        return Coordinate(x, y)


    def calculate_polygon_properties(self):
        self.center_point = self.line_intersection(self.diagonal_tl_br_line, self.diagonal_tr_bl_line)

        self.horizontal_vanish_point = self.line_intersection(self.top_line, self.bottom_line)
        self.vertical_vanish_point = self.line_intersection(self.left_line, self.right_line)

        if self.horizontal_vanish_point:
            self.horizontal_center_line = Line(self.center_point, self.horizontal_vanish_point)
        else:
            self.horizontal_center_line = Line(self.center_point, Coordinate(self.center_point.x + 10, self.center_point.y))

        if self.vertical_vanish_point:
            self.vertical_center_line = Line(self.center_point, self.vertical_vanish_point)
        else:
            self.vertical_center_line = Line(self.center_point, Coordinate(self.center_point.x, self.center_point.y + 10))

        self.upper_middle_point = self.line_intersection(self.vertical_center_line, self.top_line)
        self.lower_middle_point = self.line_intersection(self.vertical_center_line, self.bottom_line)
        self.left_middle_point = self.line_intersection(self.horizontal_center_line, self.left_line)
        self.right_middle_point = self.line_intersection(self.horizontal_center_line, self.right_line)

        self.middle_height_line = Line(self.upper_middle_point, self.lower_middle_point)
        self.middle_width_line = Line(self.left_middle_point, self.right_middle_point)

        self.middle_height = sqrt(((self.middle_height_line.p1.x - self.middle_height_line.p2.x)** 2) + ((self.middle_height_line.p1.y - self.middle_height_line.p2.y)**2))
        self.middle_width = sqrt(((self.middle_width_line.p1.x - self.middle_width_line.p2.x)** 2) + ((self.middle_width_line.p1.y - self.middle_width_line.p2.y)**2))



polygon = QrPolygon([Coordinate(500, 500),
                     Coordinate(700, 550),
                     Coordinate(500, 700),
                     Coordinate(700, 650)])  # vanish point right

polygon = QrPolygon([Coordinate(500, 550),
                     Coordinate(700, 500),
                     Coordinate(500, 650),
                     Coordinate(700, 700)])  # vanish point left

polygon = QrPolygon([Coordinate(550, 500),
                     Coordinate(650, 500),
                     Coordinate(500, 700),
                     Coordinate(700, 700)])  # vanish point up

polygon = QrPolygon([Coordinate(512, 565),
                     Coordinate(999, 531),
                     Coordinate(782, 867),
                     Coordinate(1229, 651)])  # vanish point up right

polygon = QrPolygon([Coordinate(500, 500),
                     Coordinate(700, 500),
                     Coordinate(500, 700),
                     Coordinate(700, 700)])  # square


polygon = QrPolygon([Coordinate(500, 500),
                     Coordinate(700, 500),
                     Coordinate(550, 700),
                     Coordinate(650, 700)])  # vanish point down


import timeit
loop_amount = 1000
print("time in s: {}".format(timeit.timeit(polygon.calculate_polygon_properties, number = loop_amount)))


import cv2
import numpy as np

frame = np.zeros((1080, 1920, 3), np.uint8)
while True:
    cv2.imshow("preview", frame)

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    else:
        # Vanishing points
        try:
            cv2.line(img=frame, pt1=(polygon.top_left_point.x, polygon.top_left_point.y), pt2=(int(polygon.vertical_vanish_point.x), int(polygon.vertical_vanish_point.y)), color=(255,255,255), thickness=5, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(polygon.top_right_point.x, polygon.top_right_point.y), pt2=(int(polygon.vertical_vanish_point.x), int(polygon.vertical_vanish_point.y)), color=(255,255,255), thickness=5, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(polygon.top_right_point.x, polygon.top_right_point.y), pt2=(int(polygon.horizontal_vanish_point.x), int(polygon.horizontal_vanish_point.y)), color=(255,255,255), thickness=5, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(polygon.bottom_right_point.x, polygon.bottom_right_point.y), pt2=(int(polygon.horizontal_vanish_point.x), int(polygon.horizontal_vanish_point.y)), color=(255,255,255), thickness=5, lineType=8, shift=0)
        except:
            pass


        # Diagonal
        try:
            cv2.line(img=frame, pt1=(polygon.diagonal_tl_br_line.p1.x, polygon.diagonal_tl_br_line.p1.y), pt2=(polygon.diagonal_tl_br_line.p2.x, polygon.diagonal_tl_br_line.p2.y), color=(0, 128, 255), thickness=5, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(polygon.diagonal_tr_bl_line.p1.x, polygon.diagonal_tr_bl_line.p1.y), pt2=(polygon.diagonal_tr_bl_line.p2.x, polygon.diagonal_tr_bl_line.p2.y), color=(0, 128, 255), thickness=5, lineType=8, shift=0)
        except:
            pass


        # Upper lower left right
        try:
            cv2.line(img=frame, pt1=(polygon.top_left_point.x, polygon.top_left_point.y), pt2=(polygon.top_right_point.x, polygon.top_right_point.y), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(polygon.bottom_left_point.x, polygon.bottom_left_point.y), pt2=(polygon.bottom_right_point.x, polygon.bottom_right_point.y), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(polygon.top_left_point.x, polygon.top_left_point.y), pt2=(polygon.bottom_left_point.x, polygon.bottom_left_point.y), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(polygon.top_right_point.x, polygon.top_right_point.y), pt2=(polygon.bottom_right_point.x, polygon.bottom_right_point.y), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
        except:
            pass


        # Midlines
        try:
            cv2.line(img=frame, pt1=(int(polygon.middle_height_line.p1.x), int(polygon.middle_height_line.p1.y)), pt2=(int(polygon.middle_height_line.p2.x), int(polygon.middle_height_line.p2.y)), color=(0, 204, 204), thickness=5, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(int(polygon.middle_width_line.p1.x), int(polygon.middle_width_line.p1.y)), pt2=(int(polygon.middle_width_line.p2.x), int(polygon.middle_width_line.p2.y)), color=(0, 204, 204), thickness=5, lineType=8, shift=0)
        except:
            pass

# TODO : Make polygon class so that he values associated with the polygon are contained within the polygon
# TODO : Make the function add the calculated values to the custom polygon class
# TODO : Add documentation
