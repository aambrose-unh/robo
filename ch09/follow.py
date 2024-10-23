#!/usr/bin/env python3
import cv2
from picamera2 import Picamera2
from libcamera import Transform
from face import detect_face
from adafruit_crickit import crickit

ESC_KEY = 27
GREEN = (0, 255, 0)
IMG_WIDTH = 640
IMG_HEIGHT = 480
LEFT_X = int((IMG_WIDTH / 2) - 50)
RIGHT_X = int((IMG_WIDTH / 2) + 50)
PAN = dict(servo=crickit.servo_1, min=30, max=110, start=70, range=142)
ANGLE_STEP = 2
MOVE = dict(L=ANGLE_STEP, C=0, R=-ANGLE_STEP)

def get_zone(face_x):
    if face_x <= LEFT_X:
        return 'L'
    elif face_x <= RIGHT_X:
        return 'C'
    else:
        return 'R'

def move_motor(face_x):
    zone = get_zone(face_x)
    change = MOVE[zone]
    if change and PAN['min'] <= PAN['servo'].angle + change <= PAN['max']:
        PAN['servo'].angle += change

def init_motors():
    PAN['servo'].actuation_range = PAN['range']
    PAN['servo'].angle = PAN['start']

def check_capture_device(cap):
    assert cap.isOpened(), 'Cannot open camera'
    assert cap.get(cv2.CAP_PROP_FRAME_WIDTH) == IMG_WIDTH, 'wrong width'
    assert cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == IMG_HEIGHT, 'wrong height'

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
    picam2.configure(preview_config)
    picam2.start()
    
    while cv2.waitKey(1) not in [ord('q'), ESC_KEY]:
        frame = picam2.capture_array()
        center = detect_face(frame)
        if center:
            move_motor(center[0])
        cv2.rectangle(frame, (LEFT_X, -1), (RIGHT_X, IMG_HEIGHT), GREEN)
        cv2.imshow('preview', frame)
    
    # Release resources
    cv2.destroyAllWindows()
    picam2.stop()
    picam2.close()

main()
