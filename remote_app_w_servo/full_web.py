#!/usr/bin/env python3
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.log import enable_pretty_logging
from datetime import datetime
from os.path import dirname
import os
import asyncio
import base64
import motor
from pan import move_motor, init_motors

from watcher import FileWatcher

IMG_PATH = os.environ['XDG_RUNTIME_DIR'] + '/robo_stream.jpg'
POLL_DELAY = 1 / 60
CONTENT_TYPE = 'multipart/x-mixed-replace;boundary=image-boundary'
BOUNDARY = b'--image-boundary\r\n'
JPEG_HEADER = b'Content-Type: image/jpeg\r\n\r\n'


DEBUG = bool(os.environ.get('ROBO_DEBUG'))
TEMPLATE_PATH = (dirname(__file__) + '/templates')

class MainHandler(RequestHandler):
    async def get(self):      
        stamp = datetime.now().isoformat()
        watcher = FileWatcher(IMG_PATH)
        while True:
            if watcher.has_changed():
                img_bytes = open(IMG_PATH, 'rb').read()
                # Convert the image bytes to a base64 string
                img_bytes = base64.b64encode(img_bytes).decode('utf-8')
                self.render('full.html', stamp=stamp, image_data=img_bytes)
            await asyncio.sleep(POLL_DELAY)


class DriveHandler(RequestHandler):
    async def post(self, name):
        if "pan" in name:
            direction = name.replace("pan_","")
            print(f"{direction=}")
            move_motor(direction)
        else:
            func = getattr(motor, name)
            func()
        self.redirect('/')


async def main():
    init_motors()
    settings = dict(debug=DEBUG, template_path=TEMPLATE_PATH)
    app = Application([
        ('/', MainHandler),
        ('/([a-z_]*)', DriveHandler),
    ],
    **settings)
    app.listen(9000)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()

asyncio.run(main())