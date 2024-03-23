import cv2
import numpy as np
import subprocess as sp

fifo_path = 'fifo264.txt'

FFMPEG_BIN = "ffmpeg"
command = [FFMPEG_BIN, '-i', fifo_path, '-pix_fmt', 'bgr24',
           '-vcodec', 'rawvideo', '-an', '-sn', '-f', 'image2pipe', '-']

pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)

while True:
    raw_image = pipe.stdout.read(640 * 480 * 3)
    image = np.frombuffer(raw_image, dtype='uint8')
    image = image.reshape((480, 640, 3))
    if image is not None:
        cv2.imshow('Video', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    pipe.stdout.flush()

cv2.destroyAllWindows()
