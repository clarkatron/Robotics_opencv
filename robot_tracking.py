import cv2
import numpy as np
import argparse
import imutils
import math


cap = cv2.VideoCapture(1)
board_layout = {}


while(1):
	ret, frame = cap.read()
	gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
	kernel = np.ones((6,6), np.uint8)

	nois_reduce = cv2.morphologyEx(gray_vid, cv2.MORPH_OPEN, kernel)
	#cv2.imshow('stuff',nois_reduce)

	edged_frame = cv2.Canny(nois_reduce, 150, 200, 5)
	#cv2.imshow('edges', edged_frame)
	_, threshold = cv2.threshold(edged_frame, 150, 200, 0)
	im2, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt, 0.04*cv2.arcLength(cnt, True), True)
		
		M = cv2.moments(cnt)
		#print(cnt)
		if M["m00"] != 0:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			
			perimeter = cv2.arcLength(cnt, True)
			area = cv2.contourArea(cnt)
			circularity = 4*math.pi*(area/(perimeter*perimeter))
			print(circularity)
			
			if len(approx) != 3 & len(approx) != 4 & len(approx) != 5:
				#if cnt == 0:
					#board_layout[cnt] = (cX, cY)
				#else:
					#if abs((board_layout[cnt-1][0] - cX) + (board_layout[cnt-1][1] - cY)) > 10:
						#board_layout[cnt] = (cX, cY)
						
				#cv2.drawContours(nois_reduce, [cnt], 0, (255), 5)
				cv2.circle(nois_reduce, (cX, cY), 5, (255), -1)
				
				#print(str(cX) + ',' + str(cY))
		else:
			cX, cY = 0, 0
	
	#denoised = cv2.GaussianBlur(edged_frame,(5,5),0)
    #Testing finding triangles:
	#triangles = find_triangles(edged_frame)
	print(board_layout)
	cv2.imshow('Original',frame)
	cv2.imshow('Contours and edges',nois_reduce)
	
	k = cv2.waitKey(5)
	if k==27:
		break


cap.release()
cv2.destroyAllWindows()
