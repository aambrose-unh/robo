#!/usr/bin/env python3
import os
import cv2
from picamera2 import Picamera2
from libcamera import Transform

IMG_PATH = os.environ['XDG_RUNTIME_DIR'] + '/robo_stream.jpg'
TMP_PATH = os.environ['XDG_RUNTIME_DIR'] + '/robo_stream_tmp.jpg'
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

def save_frames(camera):
    counter = 0
    while True:
        counter += 1
        request = camera.capture_request()
        request.save("main", TMP_PATH)
        request.release()
        os.replace(TMP_PATH, IMG_PATH)
        print('frames:', counter, end='\r', flush=True)

def init_camera():
    # Initialize the camera
    camera = Picamera2()
    # Configure the camera for video capture
    video_config = camera.create_video_configuration(
        transform=Transform(hflip=True, vflip=True),
        main={"size":(FRAME_WIDTH, FRAME_HEIGHT)}
        )
    camera.configure(video_config)
    return camera

def main():
    print("Init Camera")
    cap = init_camera()
    cap.start()
    try:
        print("Saving Frames")
        save_frames(cap)
    finally:
        print('releasing video capture device...')
        cap.stop()
        cap.close()

main()
