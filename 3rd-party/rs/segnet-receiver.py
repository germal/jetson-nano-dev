import zmq
import numpy as np
import cv2

context = zmq.Context()
client = context.socket(zmq.SUB)
bind_address="tcp://*:5556"

client.bind(bind_address)
client.setsockopt_string(zmq.SUBSCRIBE, str(''))

while True:
    msg = client.recv()
    src = np.frombuffer(msg, dtype=np.float32).reshape(240, 320, 4)

    cv2.imshow("image", src)
    cv2.waitKey(1)

cv2.destroyAllWindows()
