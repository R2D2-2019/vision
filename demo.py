"""
This file consists of the demo for the Vision module.
"""
from time import sleep
import keyboard as kb
import cv2

from modules.vision.module.video_feed import VideoFeedCV2
from modules.vision.module.camera_properties import CameraProperties
from modules.vision.module.qr_reader import QrReader

class Demo:
    """
    Class that describes an interface to the vision demo.
    """
    def __init__(self):
        """
        Constructor, doesn't take any parameters.
        """
        self.vf = VideoFeedCV2(0)
        self.qr = QrReader()
        self.cp = CameraProperties(4.3, 4.2)
        self.codes_seen = dict()
        self.score = 0

    def render_score(self, frame):
        """
        Render's the current score on a video frame.
        :param frame: video frame we obtained from the video feed.
        :return: void
        """
        res = self.vf.get_resolution()
        cv2.putText(frame, "score: {}".format(self.score), (20, res[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def add_code(self, code):
        """
        Adds a QR code to the 'seen' dict if it's not already in it.
        :param code: code to add to the dict.
        :return: void
        """
        message = code.get_value("Data")
        if message not in self.codes_seen:
            self.codes_seen[message] = code
            self.score += 1

    def render_code(self, frame, code):
        """
        Renders a square around the code and the text it contains on the frame.
        :param frame: video frame to render to.
        :param code: QR code to use.
        :return: void
        """
        message = code.get_value("Data")
        (x, y, w, h) = code.rect
        distance = code.get_center_distance()
        res = self.vf.get_resolution()
        code_width = code.polygon.middle_width / (res[0]/2)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.putText(frame, message, (x , y-10), cv2.FONT_HERSHEY_SIMPLEX, code_width, (255,0,0), 2)

    def run(self):
        """
        Runs the (blocking) demo loop. 
        :return: void
        """
        while True:
            if kb.is_pressed('esc'):
                break
            
            frame = self.vf.get_frame()
            self.qr.read_qr_codes(frame, self.cp)
            codes = self.qr.get_qr_codes()
            if codes:
                for code in codes:
                    self.render_code(frame, code)
                    self.add_code(code)
            self.render_score(frame)

            cv2.imshow("Demo", frame)
            cv2.waitKey(1)

def main():
    demo = Demo()
    demo.run()

main()