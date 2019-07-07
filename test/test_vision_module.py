""" This module describes the unit tests for our Vision module class. 
Please connect a webcam and start the R2D2 Python bus manager. """

import subprocess
from client.comm import Comm
from common.frame_enum import FrameType
from modules.vision.module.mod import Vision
from modules.vision.module.qr_reader import QrReader
from modules.vision.test.frame_helper import create_frame
from modules.vision.module.video_feed import VideoFeedCV2
from modules.vision.module.camera_properties import CameraProperties
from modules.vision.test.frame_helper import STRING, WIDTH, HEIGHT, X, Y, DISTANCE

FRAME_TUPLE = (bytes(STRING, 'utf-8'), WIDTH, HEIGHT, X, Y, DISTANCE)


def catch(bus: Comm):
    """ listens on the bus for a specific frametype.
    :param frame_type: type of frame to listen for.
    :return: None if it was unable to find a frame of the specified type on the bus.
    """
    data = None
    while bus.has_data():
        frame = bus.get_data()
        data = frame.get_data()
        return data
    return data


class TestVisionModule:
    """ Groups the tests for the vision class, please connect a webcam and
    start the bus manager found in the Python build directory. """

    def test_frame(self):
        """ tests the frame for correctly setting and getting the values. """
        # create a frame and get the data
        frame = create_frame(STRING, WIDTH, HEIGHT, X, Y, DISTANCE)
        data = frame.get_data()
        assert data[1:] == FRAME_TUPLE[1:]

    def test_module(self):
        """ Tests if the module correctly puts a frame on the bus and retrieve it. 
        This test can fail if there is still old data on the bus, restart the manager
        if this happens. """
        module = Vision(Comm(), VideoFeedCV2(
            0), QrReader(), CameraProperties(0, 0))

        module.comm.listen_for([FrameType.QRCODE_DATA])

        # put a frame on the bus from another process (the python build is setup in
        # a way that you can't listen to frames sent by the same OS process, so we do
        # it this way.)
        subprocess.call(['python', 'test/frame_helper.py'])

        data = None
        while data is None:
            data = catch(module.comm)
        module.comm.stop()

        assert data[1:] == FRAME_TUPLE[1:]