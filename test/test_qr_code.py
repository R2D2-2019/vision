import cv2

from modules.vision.module.qr_reader import QrReader
from modules.vision.module.qr_code import Coordinate
from modules.vision.module.qr_code import Line
from modules.vision.module.camera_properties import CameraProperties


def get_code():
    frame = cv2.imread("../test/opencv_frame.png")

    cam_prop = CameraProperties(4.3, 3.5, False)
    reader = QrReader()
    reader.read_qr_codes(frame, cam_prop)
    codes = reader.get_qr_codes()
    code = codes[0]
    return code


def test_polygon():
    code = get_code()

    # Check corder coordinates
    assert code.polygon.top_left_point == Coordinate(395, 93)
    assert code.polygon.top_right_point == Coordinate(565, 90)
    assert code.polygon.bottom_left_point == Coordinate(406, 260)
    assert code.polygon.bottom_right_point == Coordinate(587, 256)

    # Check points point
    assert int(code.polygon.center_point.x) == 488
    assert int(code.polygon.center_point.y) == 172

    # Check middle height and width
    assert int(code.polygon.middle_height) == 167
    assert int(code.polygon.middle_width) == 175


def test_qr_code():
    code = get_code()

    code_data = {'Height': '100', 'Width': '100', 'Data': 'Hi mom!'}
    assert code.data == code_data
    assert code.type == "QRCODE"
    assert code.rect.left == 395
    assert code.rect.top == 90
    assert code.rect.width == 192
    assert code.rect.height == 170
    assert int(code.center_distance) == 352
    assert int(code.center_offset[0]) == 168
    assert int(code.center_offset[1]) == -67
    assert int(code.center_offset_mm[0]) == 95
    assert int(code.center_offset_mm[1]) == -40
