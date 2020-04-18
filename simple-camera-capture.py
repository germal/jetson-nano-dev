import cv2
import time


CAM_ID = 2

cam = cv2.VideoCapture(CAM_ID)
if cam.isOpened() == False:
    print ("Can't Open the CAM(%d)" % (CAM_ID))
    exit()

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

prevTime = 0
while True:
    ret, frame = cam.read()

    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime

    fps = 1 / sec if sec != 0 else 0
    
    cv2.putText(frame, "FPS: %0.1f" % fps, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
    cv2.imshow("VideoFrame", frame)

    keyCode = cv2.waitKey(30) & 0xFF
    if (cv2.waitKey(30) & 0xFF) == 27:
        break

cam.release()
cv2.destroyAllWindows()
