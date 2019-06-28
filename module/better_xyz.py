def line_intersection(line_1, line_2):
    x_diff = (line_1[0][0] - line_1[1][0], line_2[0][0] - line_2[1][0])
    y_diff = (line_1[0][1] - line_1[1][1], line_2[0][1] - line_2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        return None

    d = (det(*line_1), det(*line_2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return [x, y]

# # Get center point of a plane in 3d space
# polygon = [[190,104],[721,342],[189,707],[723,460]]
# slanted_line_1 = [polygon[0], polygon[3]]
# slanted_line_2 = [polygon[1], polygon[2]]
# print(line_intersection(slanted_line_1, slanted_line_2))

# print("==================================================")

# # Get center height of a plane in 3d space
# import copy
# polygon_2 = [[969,236],[1403,89],[969,489],[1403,671]]

# slanted_line_1_2 = [polygon_2[0], polygon_2[3]]
# slanted_line_2_2 = [polygon_2[1], polygon_2[2]]

# upper_line_2 = [polygon_2[0], polygon_2[1]]
# lower_line_2 = [polygon_2[2], polygon_2[3]]
# left_line_2 = [polygon_2[0],polygon_2[2]]
# right_line_2 = [polygon_2[1],polygon_2[3]]

# left_line_height = left_line_2[1][1] - left_line_2[0][1], 
# right_line_height = right_line_2[1][1] - right_line_2[0][1],

# longer_line = [[0]*2]*2
# longer_line[0] = left_line_2[0].copy()
# longer_line[1] = left_line_2[1].copy()

# if left_line_height > right_line_height:
#     longer_line[0] = left_line_2[0].copy()
#     longer_line[1] = left_line_2[1].copy()
# else:
#     longer_line[0] = right_line_2[0].copy()
#     longer_line[1] = right_line_2[1].copy()


# # Move longest line to the middle
# center = line_intersection(slanted_line_1_2, slanted_line_2_2)
# longer_line_center = [(longer_line[0][0] + longer_line[1][0]) / 2, (longer_line[0][1] + longer_line[1][1]) / 2]

# line_diff = center[0] - longer_line_center[0]

# print(polygon_2)
# print(type(left_line_2[0]))
# longer_line[0][0] = longer_line[0][0] + line_diff
# longer_line[1][0] = longer_line[1][0] + line_diff

# print(polygon_2)


# intersect_1 = line_intersection(longer_line, upper_line_2)
# intersect_2 = line_intersection(longer_line, lower_line_2)


# height = intersect_2[1] - intersect_1[1]

# print(height)

print("=============================================")
from math import sqrt
import time
import timeit
# All the lines
#def polygon_measure_toolkit():
polygon = [[512, 565],[999,531],[782,867],[1229,651]]

slanted_line_1 = [polygon[0], polygon[3]]
slanted_line_2 = [polygon[1], polygon[2]]

upper_line_3 = [polygon[0], polygon[1]]
lower_line_3 = [polygon[2], polygon[3]]
left_line_3 = [polygon[0], polygon[2]]
right_line_3 = [polygon[1], polygon[3]]

center = line_intersection(slanted_line_1, slanted_line_2)

upper_lower_vanish = line_intersection(upper_line_3, lower_line_3) 
left_right_vanish = line_intersection(left_line_3, right_line_3) 

line_through_center_horizontal = [[0]*2]*2 
line_through_center_vertical = [[0]*2]*2

if upper_lower_vanish:
    line_through_center_horizontal = [center, upper_lower_vanish]
if left_right_vanish:
    line_through_center_vertical = [center, left_right_vanish]

upper_middle_point = line_intersection(line_through_center_vertical, upper_line_3)
lower_middle_point = line_intersection(line_through_center_vertical, lower_line_3)
left_middle_point = line_intersection(line_through_center_horizontal, left_line_3)
right_middle_point = line_intersection(line_through_center_horizontal, right_line_3)

height_line = [upper_middle_point, lower_middle_point] 
width_line = [left_middle_point, right_middle_point]

height = sqrt(((height_line[0][0] - height_line[1][0])**2) + ((height_line[0][1] - height_line[1][1])**2))
width = sqrt((width_line[0][0] - width_line[1][0])**2 + (width_line[0][1] - width_line[1][1])**2)

# loop_amount = 1000000
# print("time in s: {}".format(timeit.timeit(polygon_measure_toolkit, number = loop_amount)))
# print(height_line)
# print(width_line)
# print(height)
# print(width)

# print(start)
# print(stop)
# print("Time it took to calculate evrything: {}".format(start - stop))
# Show how awesome it is
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
        cv2.line(img=frame, pt1=(polygon[0][0], polygon[0][1]), pt2=(int(left_right_vanish[0]), int(left_right_vanish[1])), color=(255,255,255), thickness=5, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(polygon[1][0], polygon[1][1]), pt2=(int(left_right_vanish[0]), int(left_right_vanish[1])), color=(255,255,255), thickness=5, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(polygon[1][0], polygon[1][1]), pt2=(int(upper_lower_vanish[0]), int(upper_lower_vanish[1])), color=(255,255,255), thickness=5, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(polygon[3][0], polygon[3][1]), pt2=(int(upper_lower_vanish[0]), int(upper_lower_vanish[1])), color=(255,255,255), thickness=5, lineType=8, shift=0)

        # Diagonal
        cv2.line(img=frame, pt1=(polygon[0][0], polygon[0][1]), pt2=(polygon[3][0], polygon[3][1]), color=(0, 128, 255), thickness=5, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(polygon[1][0], polygon[1][1]), pt2=(polygon[2][0], polygon[2][1]), color=(0, 128, 255), thickness=5, lineType=8, shift=0)
        
        # Upper lower left right
        cv2.line(img=frame, pt1=(polygon[0][0], polygon[0][1]), pt2=(polygon[1][0], polygon[1][1]), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(polygon[2][0], polygon[2][1]), pt2=(polygon[3][0], polygon[3][1]), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(polygon[0][0], polygon[0][1]), pt2=(polygon[2][0], polygon[2][1]), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(polygon[1][0], polygon[1][1]), pt2=(polygon[3][0], polygon[3][1]), color=(255, 0, 0), thickness=5, lineType=8, shift=0)

        # Midlines
        cv2.line(img=frame, pt1=(int(height_line[0][0]), int(height_line[0][1])), pt2=(int(height_line[1][0]), int(height_line[1][1])), color=(0, 204, 204), thickness=5, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(int(width_line[0][0]), int(width_line[0][1])), pt2=(int(width_line[1][0]), int(width_line[1][1])), color=(0, 204, 204), thickness=5, lineType=8, shift=0)


