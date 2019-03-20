import cv2
import numpy as np
import argparse
import imutils
import socket

not_using_opencv = True

Class Robot_Track:
	cap = cv2.VideoCapture(1)
	
	board_layout = 
	
	def current_board():
		#get image data for current game board
		for i in range (0, 9)
			ret, frame = cap.read()
			gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
			
			kernel = np.ones((6,6), np.uint8)
			nois_reduce = cv2.morphologyEx(gray_vid, cv2.MORPH_OPEN, kernel)
			edged_frame = cv2.Canny(nois_reduce, 150, 200, 5)

			_, threshold = cv2.threshold(edged_frame, 150, 200, 0)
			im2, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			
			for cnt in contours:
				approx = cv2.approxPolyDP(cnt, 0.07*cv2.arcLength(cnt, True), True)
				M = cv2.moments(cnt)
				
				if M["m00"] != 0:
					cX = int(M["m10"] / M["m00"])
					cY = int(M["m01"] / M["m00"])
					if len(approx) == 3:
						cv2.circle(nois_reduce, (cX, cY), 5, (255), -1)
				else:
					cX, cY = 0, 0
			
			#denoised = cv2.GaussianBlur(edged_frame,(5,5),0)
			#Testing finding triangles:
			#triangles = find_triangles(edged_frame)
			
			cv2.imshow('Original',frame)
			cv2.imshow('Contours and edges',nois_reduce)
			
			k = cv2.waitKey(5)
		
		
		
	def get_location(name):
		#read in current contours 
		#get contours for robot
		robot = name
		#return row and column of robot
	
	def move_robot(name, ip, row, col):
                if(not_using_opencv):
                    
                    return
		is_connected = connect_robot(name, ip)
		if is_connected:
			r1_row, r1_column =  get_location(name)
		#get contour and centroid for dest
		#calculate angle and distance for robot move
                	
		send_message(name, ip, angle, distance)
	
	def send_message(name, ip, angle, distance):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                server_address = (ip, 65432)
                sock.connect(server_address)

                message = "{0},{1}".format(angle, distance)
                sock.sendall(message.encode('ascii'))

                data = sock.recv(3)
                sock.close()
		
	def connect_robot(name, ip):
		#connect
		#return true if connection works
		
		
