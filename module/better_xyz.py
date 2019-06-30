from math import sqrt

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

# All the lines
def calculate_polygon_properties(polygon):
    diagonal_lt_rb_line = [polygon[0], polygon[3]]
    diagonal_rt_lb_line = [polygon[1], polygon[2]]

    top_line = [polygon[0], polygon[1]]
    bottom_line = [polygon[2], polygon[3]]
    left_line = [polygon[0], polygon[2]]
    right_line = [polygon[1], polygon[3]]

    center_point = line_intersection(diagonal_lt_rb_line, diagonal_rt_lb_line)

    horizontal_vanish_point = line_intersection(top_line, bottom_line) 
    vertical_vanish_point = line_intersection(left_line, right_line) 

    horizontal_center_line = [center_point, [center_point[0] + 10, center_point[1]]] 
    vertical_center_line = [center_point, [center_point[0], center_point[1] + 10]]

    if horizontal_vanish_point:
        horizontal_center_line = [center_point, horizontal_vanish_point]
    if vertical_vanish_point:
        vertical_center_line = [center_point, vertical_vanish_point]

    upper_middle_point = line_intersection(vertical_center_line, top_line)
    lower_middle_point = line_intersection(vertical_center_line, bottom_line)
    left_middle_point = line_intersection(horizontal_center_line, left_line)
    right_middle_point = line_intersection(horizontal_center_line, right_line)

    height_line = [upper_middle_point, lower_middle_point] 
    width_line = [left_middle_point, right_middle_point]

    height = sqrt(((height_line[0][0] - height_line[1][0])**2) + ((height_line[0][1] - height_line[1][1])**2))
    width = sqrt((width_line[0][0] - width_line[1][0])**2 + (width_line[0][1] - width_line[1][1])**2)

    print(polygon)
    print(center_point)
    print(upper_middle_point)
    print(lower_middle_point)
    print(left_middle_point)
    print(right_middle_point)
    print(height_line)
    print(width_line)
    print(height)
    print(width)

polygon = [[500,500],[700,500],[500,700],[700,700]] # square
polygon = [[500,500],[700,550],[500,700],[700,650]] #vanish point right
polygon = [[500,550],[700,500],[500,650],[700,700]] #vanish point left
polygon = [[550,500],[650,500],[500,700],[700,700]] #vanish point up
polygon = [[500,500],[700,500],[550,700],[650,700]] #vanish point down
polygon = [[512, 565],[999,531],[782,867],[1229,651]] # vanish point yes

calculate_polygon_properties(polygon)

# TODO : Make polygon class so that he values associated with the polygon are contained within the polygon
# TODO : Make the function add the calculated values to the custom polygon class