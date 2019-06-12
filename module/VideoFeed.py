"""Provides an interface for an OpenCV video stream. """
import cv2


class VideoFeed:
    """ Abstract class that describes methods needed for creating a video feed. """
    def __init__(self):
        """ Raises error if not implemented. """
        raise NotImplementedError

    def get_frame(self):
        """ Raises error if not implemented. """        
        raise NotImplementedError

    def set_device(self, device_id):
        """ Raises error if not implemented. """
        raise NotImplementedError

    def set_resolution(self, x: int, y: int):
        """ Raises error if not implemented. """
        raise NotImplementedError


class VideoFeedCV2(VideoFeed):
    """ Implementation class of the asbstract VideoFeed class. 
    This class uses openCV to start a video stream using device drivers to get to a webcam/camera."""
    def __init__(self, device_id):
        """ Constructor.
        :param device_id: index used for picking which connected camera you want to use. """
        self.device = cv2.VideoCapture(device_id)

    def get_frame(self):
        """ Gets a new frame from the connected device. 
        :return: returns a new frame. """
        _, frame = self.device.read()
        return frame
    
    def set_device(self, device_id: int):
        """ (re)sets the capture device.
        :param device_id: index used for picking which connected camera you want to use. """
        self.device = cv2.VideoCapture(device_id)

    def set_resolution(self, x: int, y: int):
        """ Sets the resolution of the device. 
        :param x: width.
        :param y: height.
        """
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, x)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, y)

    def get_resolution(self):
        """ Gets the resolution of the device. 
        :return: returns a 2 element list containing the width and height of the device. """
        return [int(self.device.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self.device.get(cv2.CAP_PROP_FRAME_HEIGHT))]

    def detach_device(self):
        """ Detaches/releases the device for clean up. 
        :return: returns nothing """
        self.device.release()