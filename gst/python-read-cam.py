import sys
import cv2

def read_cam():
	cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)I420 ! appsink")
	if cap.isOpened():
		cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
	while True:
		ret_val, img = cap.read()
		img2 = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_I420)
		cv2.imshow('demo',img2)
		cv2.waitKey(10)
	else:
		print("camera open failed")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	read_cam()
