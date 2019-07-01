from time import sleep
import keyboard as kb
import cv2

from modules.vision.module.video_feed import VideoFeedCV2
from modules.vision.module.camera_properties import CameraProperties
from modules.vision.module.qr_reader import QrReader

def main():
    vf = VideoFeedCV2(0)
    qr = QrReader()
    cp = CameraProperties(4.3, 4.2)

    codes_seen = dict()
    score = 0

    while True:
        if kb.is_pressed('esc'):
            break
        
        frame = vf.get_frame()
        qr.read_qr_codes(frame, cp)
        codes = qr.get_qr_codes()
        if codes:
            for code in codes:
                message = code.get_value("Data")
                if message not in codes_seen:
                    codes_seen[message] = code
                    print(message)
                    score += 1
                    print("New score: {}".format(score))