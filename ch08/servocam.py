#!/usr/bin/env python3
from datetime import datetime
import cv2
from adafruit_crickit import crickit
from snapshot import save_photo, show_image, set_message
from pan import move_motor, init_motors
from picamera2 import Picamera2
from libcamera import Transform

ESC_KEY = 27
ARROW_KEYS = {81: 'left', 82: 'up', 83: 'right', 84: 'down'}

def handle_key(key, frame, messages):
    if key == ord(' '):
        save_photo(frame)
        set_message(messages, 'saving photo...')
    elif key in ARROW_KEYS.keys():
        move_motor(ARROW_KEYS[key])
        set_message(messages, f'moving {ARROW_KEYS[key]}...')

def main():
    init_motors()
    
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    transform=Transform(vflip=1, hflip=1)
    preview_config = picam2.create_preview_configuration(
            transform=Transform(hflip=True, vflip=True)
        )
    # picam2.configure("preview")
    picam2.configure(preview_config)
    picam2.start()

    messages = []
    while (key := cv2.waitKey(1)) not in [ord('q'), ESC_KEY]:
        frame = picam2.capture_array()
        handle_key(key, frame, messages)
        show_image(frame, messages)

    # Release resources
    cv2.destroyAllWindows()
    picam2.stop()
    picam2.close()


main()
