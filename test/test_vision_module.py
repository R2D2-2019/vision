from client.comm import Comm
from common.frame_enum import FrameType
from common.frames import FrameQrcodeData

from modules.vision.module.mod import Vision
from modules.vision.module.video_feed import VideoFeedCV2
from modules.vision.module.camera_properties import CameraProperties
from modules.vision.module.qr_reader import QrReader

STRING = "TEST"
WIDTH, HEIGHT = 100, 100
X, Y = 5, 5
DISTANCE = 20

FRAME_TUPLE = (bytes(STRING, 'utf-8'), WIDTH, HEIGHT, X, Y, DISTANCE)

def create_frame():
    """ Helper function for creating a new CAN bus frame. 
    :return: Ret urns the created frame. """
    frame = FrameQrcodeData()
    byte_string = bytes(STRING, 'utf-8')
    frame.set_data(byte_string, WIDTH, HEIGHT, X, Y, DISTANCE)
    return frame

class Listener():
    def __init__(self, comm):
        self.comm = comm
        self.comm.listen_for([FrameType.QRCODE_DATA])

    def put(self, frame):
        """ puts a frame on the bus. """
        self.comm.send(frame)

    def catch(self, frame_type):
        """ listens on the bus for a specific frametype.
        :param frame_type: type of frame to listen for.
        :return: None if it was unable to find a frame of the specified type on the bus.
        """
        data = None
        while self.comm.has_data():
            frame = self.comm.get_data()
            data = frame.get_data()
        return data

class VisionDummy(Vision):
    """ Helper class that inherits from the vision module class but adds extra functions for
    explicitly sending data over the bus and catching data from the bus. """
    def put(self, frame):
        """ puts a frame on the bus. """
        self.comm.send(frame)

    def catch(self, frame_type):
        """ listens on the bus for a specific frametype.
        :param frame_type: type of frame to listen for.
        :return: None if it was unable to find a frame of the specified type on the bus.
        """
        data = None
        while self.comm.has_data():
            print("found data")
            frame = self.comm.get_data()
            if frame.type == frame_type:
                data = frame.get_data()
        return data


class TestVisionModule:
    """ Groups the tests for the vision class, please connect a webcam and
    start the bus manager found in the Python build directory. """
    def test_frame(self):
        """ tests the frame for correctly setting and getting the values. """
        # create a frame and get the data
        frame = create_frame()
        data = frame.get_data()
        assert data[1:] == FRAME_TUPLE[1:]

    def test_module(self):
        """ Tests if the module correctly puts a frame on the bus and retrieve it. """

        vd = VisionDummy(Comm(), VideoFeedCV2(0), QrReader(), CameraProperties(0, 0))
        
        frame = create_frame()
        vd.put(frame)

        data = None
        while data is None:
            data = vd.catch(FrameType.QRCODE_DATA)
        
        assert data[1:] == FRAME_TUPLE[1:]