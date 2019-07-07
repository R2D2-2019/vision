""" Python module for the Vision module. """
from client.comm import BaseComm
from common.frame_enum import FrameType
from common.frames import FrameQrcodeData


class Vision:
    """ This is the main module class used for every step in the process. 
    See class/activity diagrams for more.  """

    def __init__(self, comm: BaseComm, video_feed, qr_reader, camera_properties):
        """ 
        Vision class constructor. 
        Provides the class with everything it needs to get and process QR codes. 
        :param comm: communication CAN bus
        :param video_feed: The video feed for getting video frames.
        :param qr_reader: The QR reader class we created.
        :param camera_properties: Our camera properties class for calculating the distance.
        """
        self.comm = comm
        self.video_feed = video_feed
        self.qr_reader = qr_reader
        self.cp = camera_properties
        # self.comm.listen_for([FrameType.BUTTON_STATE])

    def reset_video_feed(self, feed):
        """ Use this function to attach a new video feed. """
        self.video_feed = feed

    def reset_reader(self, new_reader):
        """ Use this function to attach a new QR reader. """
        self.qr_reader = new_reader

    def process(self):
        """ The process function that's provided by the template. This generates QR
        codes from a video frame and puts them on the bus by request. """
        while self.comm.has_data():
            frame = self.comm.get_data()

            # if its a request we process the current video feed frame
            if frame.request:
                video_frame = self.video_feed.get_frame()
                self.qr_reader.read_qr_codes(video_frame, self.cp)
                frames = list()
                codes = self.qr_reader.get_qr_codes()

                # if we found codes we make a frame based on the code and add it to the list to send off
                if codes:
                    for code in codes:
                        center = code.get_center_offset()
                        frame = FrameQrcodeData()
                        byte_string = bytes(code.get_value("Data"), 'utf-8')
                        frame.set_data(byte_string, int(code.get_value("Width")), int(code.get_value(
                            "Height")), int(center[0]), int(center[1]), int(code.get_distance()))
                        self.comm.send(frame)

                # send off the frames
                for frame in frames:
                    self.comm.send(frame)

    def stop(self):
        """ Stop function provided by the template. """
        self.comm.stop()
