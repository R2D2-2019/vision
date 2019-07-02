from time import sleep
from sys import platform
import signal

from client.comm import Comm
from modules.vision.module.mod import Vision

from modules.vision.module.video_feed import VideoFeedCV2
from modules.vision.module.camera_properties import CameraProperties
from modules.vision.module.qr_reader import QrReader

SHOULD_STOP = False


def main():

    print("Starting application...\n")
    vision = Vision(Comm(), VideoFeedCV2(0), QrReader(),
                    CameraProperties(4.3, 4.2))
    print("Module created...")

    while not SHOULD_STOP:
        vision.process()
        sleep(0.05)

    vision.stop()


def stop(signal, frame):
    """
    Stops the process and  stops the listening to incoming frames
    :return:
    """
    global SHOULD_STOP
    SHOULD_STOP = True


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)

if __name__ == "__main__":
    main()
