def line_intersection(line_1, line_2):
    x_diff = (line_1[0][0] - line_1[1][0], line_2[0][0] - line_2[1][0])
    y_diff = (line_1[0][1] - line_1[1][1], line_2[0][1] - line_2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line_1), det(*line_2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return [x, y]
    
# Get center point of a plane in 3d space
polygon = [[190,104],[721,342],[189,707],[723,460]]
slanted_line_1 = [polygon[0], polygon[3]]
slanted_line_2 = [polygon[1], polygon[2]]
print(line_intersection(slanted_line_1, slanted_line_2))

print("==================================================")

# Get center height of a plane in 3d space
import copy
polygon_2 = [[969,236],[1403,89],[969,489],[1403,671]]

slanted_line_1_2 = [polygon_2[0], polygon_2[3]]
slanted_line_2_2 = [polygon_2[1], polygon_2[2]]

upper_line_2 = [polygon_2[0], polygon_2[1]]
lower_line_2 = [polygon_2[2], polygon_2[3]]
left_line_2 = [polygon_2[0],polygon_2[2]]
right_line_2 = [polygon_2[1],polygon_2[3]]

left_line_height = left_line_2[1][1] - left_line_2[0][1], 
right_line_height = right_line_2[1][1] - right_line_2[0][1],

longer_line = [[0]*2]*2
longer_line[0] = left_line_2[0].copy()
longer_line[1] = left_line_2[1].copy()

if left_line_height > right_line_height:
    longer_line[0] = left_line_2[0].copy()
    longer_line[1] = left_line_2[1].copy()
else:
    longer_line[0] = right_line_2[0].copy()
    longer_line[1] = right_line_2[1].copy()


# Move longest line to the middle
center = line_intersection(slanted_line_1_2, slanted_line_2_2)
longer_line_center = [(longer_line[0][0] + longer_line[1][0]) / 2, (longer_line[0][1] + longer_line[1][1]) / 2]

line_diff = center[0] - longer_line_center[0]

print(polygon_2)
print(type(left_line_2[0]))
longer_line[0][0] = longer_line[0][0] + line_diff
longer_line[1][0] = longer_line[1][0] + line_diff

print(polygon_2)


intersect_1 = line_intersection(longer_line, upper_line_2)
intersect_2 = line_intersection(longer_line, lower_line_2)


height = intersect_2[1] - intersect_1[1]

print(height)