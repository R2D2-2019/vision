"""Provides a camera properties class"""

class CameraProperties:
    """ 
    A class that holds the camera property information. 
    """

    def __init__(self, focal_length=None, sensor_height=None, is_pycam=False):
        """ 
        Construct a new CameraProperties object.

        :param focal_length: The focal length of the camera in millimeters
        :param sensor_height: The height of the physical sensor in millimeters
        :param is_pycam: Whether the camera is a PyCAM or not
        :return: Returns nothing
        """
        self.focal_length = focal_length
        self.sensor_height = sensor_height
        self.is_pycam = is_pycam

    def set_focal_length(self, focal_length):
        """ 
        Sets a new value for the focal length.
        :param focal_length: The new focal length of the camera in millimeters
        :return: Returns nothing
        """
        self.focal_length = focal_length

    def set_sensor_height(self, sensor_height):
        """ 
        Sets a new value for the sensor height.
        :param sensor_height: The new height of the physical sensor in millimeters
        :return: Returns nothing
        """
        self.sensor_height = sensor_height

    def set_is_pycam(self, is_pycam):
        """ 
        Sets a value for is_pycam.
        :param is_pycam: The new boolean value for whether the camera is a PyCAM or not
        :return: Returns nothing
        """
        self.is_pycam = is_pycam

    def get_focal_length(self):
        """
        Gets the focal length
        :return: Returns the focal length of the camera in millimeters
        """
        return self.focal_length

    def get_sensor_height(self):
        """
        Gets the sensor height
        :return: Returns the sensor height of the camera in millimeters
        """
        return self.sensor_height

    def get_is_pycam(self):
        """
        Gets the is_pycam value
        :return: Returns a boolean whether the camera is a PyCAM
        """
        return self.is_pycam