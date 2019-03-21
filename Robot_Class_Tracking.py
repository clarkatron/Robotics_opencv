import cv2
import numpy as np
import argparse
import imutils
import socket

not_using_opencv = True

class Robot_Track(object):

    def __init__(self, camera_index):
        self.cap = cv2.VideoCapture(camera_index)
        self.board_layout = None
        robots = {'p1_l':[50,70,100], 'p1_u':[100,255,255], 
					'p2_l':[0,150,100], 'p2_u':[25,200,255],
					't1_l':[],'t1_u':[]}
		

    def current_board(self):
        #get image data for current game board
        for i in range (0, 9):
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
            
    def get_location(self, name):
        #read in current contours 
        robot = name
        #get the HSV values for the robot based on name.
        if robot == 'p1':
			hsv_l = robot['p1_l']
			hsv_u = robot['p1_u']
		else if robot == 'p2'
			hsv_l = robot['p2_l']
			hsv_u = robot['p2_u']
		else
			hsv_l = robot['t_l']
			hsv_u = robot['t_u']
		#get location of the blob of this color and then do the 
		#distance equation. 
        #return row and column of robot

    def move_robot(self, name, ip, row, col):
        if(not_using_opencv):
            good = 0
            while good == 0:
                print("please give directions for the robot " + name + "to get to location (" + str(row) + "," + str(col) +")")
                distance = float(input("Distance:  "))
                if name == "t":
                    distance = int(distance)
                angle = int(input("Angle:  "))
                self.send_message(name, ip, angle, distance)
                good = int(input("is he in the right spot? (1/0)  "))
            return
        is_connected = connect_robot(name, ip)
        if is_connected:
            r1_row, r1_column =  get_location(name)
        #get contour and centroid for dest
        #calculate angle and distance for robot move
                    
        send_message(name, ip, angle, distance)

    def send_message(self, name, ip, angle, distance):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (ip, 65432)
        sock.connect(server_address)

        message = "{0},{1}".format(angle, distance)
        sock.sendall(message.encode('ascii'))

        data = sock.recv(3)
        sock.close()
	
	
