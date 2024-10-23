#!/usr/bin/env python3
import cv2
from picamera2 import Picamera2
from libcamera import Transform
from face import detect_face

ESC_KEY = 27

def main():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    transform=Transform(vflip=1, hflip=1)
    preview_config = picam2.create_preview_configuration(
            transform=Transform(hflip=True, vflip=True)
        )
    picam2.configure(preview_config)
    picam2.start()
    
    while cv2.waitKey(1) not in [ord('q'), ESC_KEY]:
        frame = picam2.capture_array()
        detect_face(frame)
        cv2.imshow('preview', frame)
    
    # Release resources
    cv2.destroyAllWindows()
    picam2.stop()
    picam2.close()

main()
