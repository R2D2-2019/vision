import cv2

class VideoFeed:
    def __init__(self):
        raise NotImplementedError

    def get_frame(self):
        raise NotImplementedError

    def set_stream(self, source):
        raise NotImplementedError

    def set_resolution(self, x: int, y: int):
        raise NotImplementedError


class VideoFeedCV2(VideoFeed):
    def __init__(self, device_id):
        self.device = cv2.VideoCapture(device_id)

    def get_frame(self):
        _, frame = self.device.read()
        return frame
    
    def set_stream(self, source: int):
        self.device = cv2.VideoCapture(source)

    def set_resolution(self, x: int, y: int):
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, x)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, y)

    def get_resolution(self):
        return [int(self.device.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self.device.get(cv2.CAP_PROP_FRAME_HEIGHT))]

    def detach_device(self):
        self.device.release()