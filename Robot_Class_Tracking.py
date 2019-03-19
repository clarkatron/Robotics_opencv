import cv2
import numpy as np
import argparse
import imutils


Class Robot_Track:
	cap = cv2.VideoCapture(1)
	
	def current_board():
		#get image data for current game board
		
		
		
		
	def get_location(name):
		#read in current contours 
		#get contours for robot
		robot = name
		#return row and column of robot
		
	def move_robot(name, ip, row, col):
		is_connected = connect_robot(name, ip)
		if is_connected:
			r1_row, r1_column =  get_location(name)
		#get contour and centroid for dest
		#calculate angle and distance for robot move
		
		send_message(name, ip, angle, distance)
	
	def send_message(name, ip, angle, distance):
		#message should take the format of (degrees,distance)
		
	def connect_robot(name, ip):
		#connect
		#return true if connection works
		
		
