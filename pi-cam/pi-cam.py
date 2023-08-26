#!/usr/bin/python3
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput
from libcamera import Transform

import io
import logging
import socket
import socketserver
from threading import Condition, Thread
from http import server
from pathlib import Path

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/favicon.ico':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            try:
                f = open('favicon.png', mode='rb')
                self.wfile.write(f.read())
                f.close()
            except IOError:
                logging.debug('StreamingHandler - No favicon')
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with stream_out.condition:
                        stream_out.condition.wait()
                        frame = stream_out.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
          
if __name__ == "__main__":
    f = open('/etc/hostname')
    s = f.read()
    f.close()
    title = s.strip().title()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    local_ip = sock.getsockname()[0]
    sock.close()

    port = 8080
    try:
        p = Path(__file__).with_suffix('.html')
        with p.open('r') as f:
            s = f.read()
        PAGE = s.strip()
    except FileNotFoundError:
        PAGE = '<!DOCTYPE html><html><head><title>HOST</title><meta charset="utf-8"><img src="stream.mjpg" /></body></html>'

    PAGE = PAGE.replace("HOST", title)

    camera = Picamera2()
    video_config = camera.create_video_configuration(main={"size": (1280, 720),"format":"YUV420"}, transform=Transform(vflip=True))
    camera.configure(video_config)
    stream_out = StreamingOutput()
    encoder = MJPEGEncoder(10000000)
    camera.start_recording(encoder, FileOutput(stream_out))
    try:
        address = (local_ip, port)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
    