import cv2
import numpy as np
import argparse
import imutils

cap = cv2.VideoCapture(1)

while(1):
	ret, frame = cap.read()
	#gray_vid = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
	#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	hsv_vid = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	kernel = np.ones((5,5), np.uint8)

	hsv_vid = cv2.morphologyEx(hsv_vid, cv2.MORPH_OPEN, kernel)
	#edged_frame = cv2.Canny(gray_vid, 150, 200, 5)
	lower_red = np.array([0,0,0])
	upper_red = np.array([50,100,50])
	mask = cv2.inRange(hsv_vid, lower_red, upper_red)
	mask = cv2.erode(mask, kernel)
	mask = cv2.dilate(mask, kernel)
	#res = cv2.bitwise_and(edged_frame, edged_frame, mask = mask)

	mask1 = cv2.resize(mask, (960,540))
	#res1 = cv2.resize(res, (960,540))
	edges = cv2.resize(frame, (960,540))

	
	#cv2.imshow('res', res1)
	cv2.imshow('edges', edges)
	cv2.imshow('mask', mask1)
	k = cv2.waitKey(5)
	if k==27:
		break
	
cap.release()
cv2.destroyAllWindows()
