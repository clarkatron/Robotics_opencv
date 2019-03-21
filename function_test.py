import cv2
import numpy as np
import argparse
import imutils

cap = cv2.VideoCapture(1)
circles = []
count = 0

while (count < 10):
	ret, frame = cap.read()
	#gray_vid = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
	#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	hsv_vid = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	kernel = np.ones((5,5), np.uint8)
	print (circles)
	hsv_vid = cv2.morphologyEx(hsv_vid, cv2.MORPH_OPEN, kernel)
	#edged_frame = cv2.Canny(gray_vid, 150, 200, 5)
	lower_red = np.array([50,70,100])
	upper_red = np.array([100,255,255])
	mask = cv2.inRange(hsv_vid, lower_red, upper_red)
	mask = cv2.erode(mask, kernel)
	mask = cv2.dilate(mask, kernel)
	#res = cv2.bitwise_and(edged_frame, edged_frame, mask = mask)
	gray = cv2.GaussianBlur(mask,(5,5),0)
	gray = cv2.medianBlur(gray, 5)
	
	rows = gray.shape[0]
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows/8,param1=100, param2=20, minRadius=10, maxRadius=40)	
	count = count +1	

if circles is not None:
	circles = np.uint16(np.around(circles))
	for i in circles[0, :]:
		center = (i[0], i[1])
		print('x: ' + str(i[0]) + ' y: ' + str(i[1]))
		# circle center
		cv2.circle(mask, center, 1, (0, 100, 100), 3)
		# circle outline
		radius = i[2]
		cv2.circle(mask, center, radius, (255, 0, 255), 3)
print(circles)
mask1 = cv2.resize(mask, (960,540))
#res1 = cv2.resize(res, (960,540))
edges = cv2.resize(frame, (960,540))


#cv2.imshow('res', res1)
cv2.imshow('edges', edges)
cv2.imshow('mask', mask1)
k = cv2.waitKey(5)

	
cap.release()
cv2.destroyAllWindows()
