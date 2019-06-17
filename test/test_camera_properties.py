"""
Tests for the camera_properties class
"""
from camera_properties import CameraProperties


def test_camera_constructor():
    """
    This function tests the constructor of CameraProperties
    with its default constructor values and with given parameter values.

    The first part of the test is to test the default constructor.
    The default values should be:
    focal_length = None
    sensor_height = None
    is_pycam = False

    The second part of the test has parameter values
    The values should be:
    focal_length = 4
    sensor_height = 6
    is_pycam = True

    This test should be done to see whether the constructor still functions as it should.
    """
    # First part of the test
    camera1 = CameraProperties()
    assert camera1.focal_length is None
    assert camera1.sensor_height is None
    assert camera1.is_pycam is False

    # Second part of the test
    camera2 = CameraProperties(4, 6, True)
    assert camera2.focal_length is 4
    assert camera2.sensor_height is 6
    assert camera2.is_pycam is True


def test_camera_getters():
    """
    Test the getters
    """
    camera = CameraProperties(4, 6, True)
    assert camera.get_focal_length() is 4
    assert camera.get_sensor_height() is 6
    assert camera.get_is_pycam() is True


def test_camera_setters():
    """
    Test the setters
    """
    camera = CameraProperties()
    camera.set_focal_length(4)
    camera.set_sensor_height(6)
    camera.set_is_pycam(True)
    assert camera.get_focal_length() is 4
    assert camera.get_sensor_height() is 6
    assert camera.get_is_pycam() is True
