import time
import cv2
import numpy as np
from pyzbar import pyzbar
from video_feed import VideoFeedCV2


class QRDetectionZbar:
    def __init__(self, title):
        self.title = title
        self.frame = None
        self.vf = VideoFeedCV2(0)
        time.sleep(2.0)
        self.vf.set_resolution(1280, 720)

    def render(self):
        cv2.imshow(self.title, self.frame)
        cv2.waitKey(1)

    def update(self):
        self.frame = self.vf.get_frame()


def main():
    app = QRDetectionZbar("App")

    while True:
        app.update()
        app.render()

        # detects if we close the window
        if cv2.getWindowProperty(app.title, cv2.WND_PROP_VISIBLE) < 1:
            break

    app.vf.detach_device()
    cv2.destroyAllWindows()


main()
