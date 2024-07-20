import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np


class VideoCamera(object):
    def __init__(self, flip=False, file_type=".jpg", photo_string="stream_photo"):
        self.flip = flip  # Flip frame vertically
        self.file_type = file_type  # Image type i.e. .jpg
        self.photo_string = photo_string  # Name to save the photo

        # Initialize video stream at lower resolution for streaming
        self.vs = PiVideoStream(resolution=(640, 480), framerate=30).start()
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()

    def take_picture(self):
        # Stop the lower resolution video stream
        self.vs.stop()

        # Initialize a new video stream at higher resolution for still capture
        capture = PiVideoStream(resolution=(1920, 1080), framerate=15).start()
        time.sleep(2.0)

        # Capture a frame at high resolution 
        frame = self.flip_if_needed(capture.read())

        # Save the high-resolution still image
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S")  # Get current time
        cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)

        # Stop the high resolution stream
        capture.stop()

        # Restart the lower resolution video stream
        self.vs = PiVideoStream(resolution=(640, 480), framerate=30).start()
        time.sleep(2.0)