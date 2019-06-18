from client.comm import BaseComm
from common.frame_enum import FrameType

import cv2

# TODO: make a PR for this frame type


class FRAMETYPE:
    def __init__(self):
        self.msg = ""
        self.width = 0
        self.height = 0
        self.distance = 0
        self.x_offset = 0
        self.y_offset = 0


class Vision:
    def __init__(self, comm: BaseComm, video_feed, qr_reader, camera_properties):
        self.comm = comm
        self.video_feed = video_feed
        self.qr_reader = qr_reader
        self.cp = camera_properties
        # self.comm.listen_for([FrameType.BUTTON_STATE])

    def reset_video_feed(self, feed):
        self.video_feed = feed

    def reset_reader(self, new_reader):
        self.qr_reader = new_reader

    def process(self):
        # self.comm.send(FrameType.BUTTON_STATE, (1,2,3))

        video_frame = self.video_feed.get_frame()
        cv2.imshow("frame", video_frame)
        cv2.waitKey(1)
        self.qr_reader.read_qr_codes(video_frame, self.cp)

        frames = list()
        codes = self.qr_reader.get_qr_codes()
        if codes:
            for code in codes:
                frame = FRAMETYPE()
                frame.msg = code.get_value("Data")
                frame.width = code.get_value("Width")
                frame.height = code.get_value("Height")
                frame.distance = code.get_distance()
                center = code.get_center_offset()
                if center:
                    frame.x_offset = center[0]
                    frame.y_offset = center[1]
                frames.append(frame)

        if 1:  # TODO: this 'if' should trigger on data request
            for frame in frames:
                print(" width {} height {} distance {} offsetx {} offsety {}".format(
                    frame.width, frame.height, frame.distance, frame.x_offset, frame.y_offset))
                # self.comm.send(frame)

        while self.comm.has_data():
            print(self.comm.get_data())

    def stop(self):
        self.comm.stop()
