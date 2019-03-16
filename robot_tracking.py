import cv2
import numpy as np
import argparse
import imutils

#def move_bot():
#	
 
while(1):
	cap = cv2.VideoCapture(1)
	ret, frame = cap.read()
	gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
	edged_frame = cv2.Canny(gray_vid,150,200,5)
	_, threshold = cv2.threshold(edged_frame, 150, 200, 0)
	im2, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt, 0.07*cv2.arcLength(cnt, True), True)
		M = cv2.moments(cnt)
		if M["m00"] != 0:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			if len(approx) == 3:
				cv2.drawContours(edged_frame, [cnt], 0, (255), 5)
				cv2.circle(edged_frame, (cX, cY), 5, (255), -1)
		else:
			cX, cY = 0, 0
	
	#denoised = cv2.GaussianBlur(edged_frame,(5,5),0)
    #Testing finding triangles:
	#triangles = find_triangles(edged_frame)
	
	cv2.imshow('Edges',edged_frame)
	cv2.imshow('Original',frame)
	k= cv2.waitKey(5)
	if k==27:
		break
cap.release()
cv2.destroyAllWindows()
