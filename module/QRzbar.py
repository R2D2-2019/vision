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

    def get_offset(self, barcode):
        (x, y, w, h) = barcode.rect
        res = self.vf.get_resolution()
        center = self.get_center(barcode)
        offset_x, offset_y, = center[0] - res[0]/2, center[1] - res[1]/2
        return [offset_x, offset_y]

    def get_center(self, barcode):
        (x, y, w, h) = barcode.rect
        center_x, center_y = x+(w/2), y+(h/2)
        return [center_x, center_y]

    def get_tag(self, barcode):
        return barcode.data.decode("utf-8")

    def render_tag(self, frame, barcode):
        (x, y, w, h) = barcode.rect
        cv2.putText(frame, self.get_tag(barcode), (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    def render_box(self, frame, barcode):
        v2s = barcode.polygon
        # if it's not a square which consists of 4 vector2's, create a more complex hull
        if len(v2s) > 4:
            hull = cv2.convexHull(
                np.array([v2 for v2 in v2s], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = v2s
            # draw 4 lines (rectangle) around the QR code based on the vector2's the hull contains
            for offset, value in enumerate(hull):
                cv2.line(frame, hull[offset], hull[(
                    offset+1) % len(hull)], (255, 0, 0), 3)
                center = self.get_center(barcode)
                cv2.circle(frame, (int(center[0]), int(
                    center[1])), 5, (255, 0, 0), 3)

    def render(self):
        cv2.imshow(self.title, self.frame)
        cv2.waitKey(1)

    def update(self):
        self.frame = self.vf.get_frame()
        barcodes = pyzbar.decode(self.frame)
        for barcode in barcodes:
            tag = self.get_tag(barcode)
            self.render_tag(self.frame, barcode)
            self.render_box(self.frame, barcode)


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
