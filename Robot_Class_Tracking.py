import cv2
import numpy as np
import argparse
import imutils
import socket

not_using_opencv = False
no_robots = True
p1_l = 1
p1_u = 2
p2_l = 3
p2_u = 4
t1_l = 5
t1_u = 6

class Robot_Track(object):
    def __init__(self, camera_index):
        self.cap = cv2.VideoCapture(camera_index)
        self.board_layout = {
                (0,0) : (353, 67),
                (1,0) : (279, 205),
                (1,1) : (358, 169),
                (1,2) : (440, 195),
                (2,0) : (223, 339),
                (2,1) : (292, 312),
                (2,2) : (369, 337),
                (2,3) : (442, 299),
                (2,4) : (512, 330),
                (3,0) : (172, 449),
                (3,1) : (241, 422),
                (3,2) : (305, 444),
                (3,3) : (375, 423),
                (3,4) : (441, 439),
                (3,5) : (504, 409),
                (3,6) : (575, 433)
                }

        self.robots = { p1_l : np.array([50,70,100]),
                        p1_u : np.array([100,255,255]), 
                        p2_l : np.array([0,150,100]),
                        p2_u : np.array([25,200,255]),
                        t1_l : np.array([0, 37, 179]),
                        t1_u : np.array([20, 78, 255])
                        }
        
    def static_board_coords(self, row, column):
        #pull in current coords
        return board_layout[(row, column)]
            
    def get_location(self, name):
        #read in current contours 
        robot = name
    #get the HSV values for the robot based on name.
        if robot == 'p1':
            hsv_l = self.robots[p1_l]
            hsv_u = self.robots[p1_u]
            
        elif robot == 'p2':
            hsv_l = self.robots[p2_l]
            hsv_u = self.robots[p2_u]
        else:
            hsv_l = self.robots[t1_l]
            hsv_u = self.robots[t1_u]
            
        x, y = self.get_blob(hsv_l, hsv_u)
        return x, y
        
    def get_blob(self, hsv_low, hsv_upper):
        circles = []
        count = 0
        while (count < 10):
            ret, frame = self.cap.read()
            #gray_vid = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
            #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv_vid = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            kernel = np.ones((5,5), np.uint8)

            hsv_vid = cv2.morphologyEx(hsv_vid, cv2.MORPH_OPEN, kernel)
            #edged_frame = cv2.Canny(gray_vid, 150, 200, 5)
            lower_red = hsv_low
            upper_red = hsv_upper
            mask = cv2.inRange(hsv_vid, lower_red, upper_red)
            mask = cv2.erode(mask, kernel)
            mask = cv2.dilate(mask, kernel)
            #res = cv2.bitwise_and(edged_frame, edged_frame, mask = mask)
            gray = cv2.GaussianBlur(mask,(5,5),0)
            gray = cv2.medianBlur(gray, 5)

            rows = gray.shape[0]
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows/8,param1=100, param2=20, minRadius=10, maxRadius=40)
            count = count + 1
        if circles is not None:    
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                x = i[0]
                y = i[1]
                if x:
                    return x, y

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
                #get contour and centroid for dest
        r1_row, r1_col =  self.get_location(name)
        dest_row, dest_col = self.static_board_coords(row, col)
        
                #calculate angle and distance for robot move
        angle  = degrees(atan2((dest_col - r1_col), (dest_row - r1_row)))
        distance = sqrt((dest_row - r1_row)**2 + (dest_col - r1_col)**2)
        # send the message
        self.send_message(name, ip, angle, distance)

    def send_message(self, name, ip, angle, distance):
        if(no_robots):
            print("sending robot: " + str(name) + " dist: " + str(distance) + " angle: " + str(angle))
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (ip, 65432)
        sock.connect(server_address)

        message = "{0},{1}".format(angle, distance)
        sock.sendall(message.encode('ascii'))

        data = sock.recv(3)
        sock.close()
        
    def current_board(self):
        #get image data for current game board
        #this function may be obsolete if other options work
        for i in range (0, 9):
            ret, frame = self.cap.read()
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
    
    
