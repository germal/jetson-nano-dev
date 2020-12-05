import numpy as np
import cv2
import zmq, sys
import imagezmq
import time

# ethernet: 192.168.0.110
# wifi: 192.168.0.184
image_hub = imagezmq.ImageHub(open_port='tcp://127.0.0.1:5555', REQ_REP=False)

prevTime = 0
while True:

    name, jpg_buffer = image_hub.recv_jpg()
    image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)



    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime

    if sec != 0:
        fps = 1 / (sec)
    else:
        fps = 0
    str_fps = "FPS : %0.1f" % fps

    cv2.putText(image, str_fps, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

    cv2.imshow(name, image)
    cv2.waitKey(1)

