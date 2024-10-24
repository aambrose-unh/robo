#!/usr/bin/env python3
from datetime import datetime
import cv2
from picamera2 import Picamera2
from libcamera import Transform

ESC_KEY = 27
BLUE = (255, 0, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_POS = (10, 30)
MSG_FRAME_COUNT = 10

def save_photo(frame):
    stamp = datetime.now().isoformat().replace(':', '.')
    cv2.imwrite(f'photo_{stamp}.jpg', frame)

def show_image(frame, messages):
    if messages:
        cv2.putText(frame, messages.pop(), TEXT_POS, FONT, 1, BLUE)
    cv2.imshow('preview', frame)

def set_message(messages, text):
    messages[:] = [text] * MSG_FRAME_COUNT

def main():
    
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    transform=Transform(hflip=1)
    picam2.configure("preview")
    picam2.start()

    try:
        while True:
            im = picam2.capture_array()
            cv2.imshow("Camera", im)

            # Save an image when a key is pressed (e.g., 's')
            key = cv2.waitKey(1)
            messages = []
            if key == ord('s'):
                save_photo(im)
                set_message(messages, 'saving photo...')

            # Exit the loop when 'q' is pressed
            elif key == ord('q'):
                break
                
            show_image(im, messages)
            print("Image saved!")

    finally:
        # Release resources
        cv2.destroyAllWindows()
        picam2.stop()
        picam2.close()
    

if __name__ == "__main__":
    main()
