""" Tests the behavior of the VideoFeed class. """

import pytest

from modules.vision.module.video_feed import VideoFeedCV2


class TestVideoFeedCV2:
    """ Groups the tests for the VideoFeedCV2 class,
    please connect at least one camera. """

    def test_resolution(self):
        """ Tests if we are able to get and set the resolution correctly. """
        w, h = 640, 480
        vf = VideoFeedCV2(0)
        vf.set_resolution(w, h)
        res = vf.get_resolution()
        assert(res[0] == w)
        assert(res[1] == h)

    def test_open(self):
        """ Tests if the device is correctly opened (requires a connected camera). """
        vf = VideoFeedCV2(0)
        assert(vf.device.isOpened())

    def test_detach(self):
        """ Tests if the device is correctly released (requires a connected camera). """
        vf = VideoFeedCV2(0)
        vf.detach_device()
        assert(not vf.device.isOpened())
