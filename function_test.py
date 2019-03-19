import cv2
import numpy as np
import argparse
import imutils

img = cv2.imread('test3.jpg', 1)

#gray_vid = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
gray_vid = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
edged_frame = cv2.Canny(gray_vid, 150, 200, 5)
lower_red = np.array([103,86,50])
upper_red = np.array([145,133,100])
mask = cv2.inRange(img, lower_red, upper_red)
res = cv2.bitwise_and(edged_frame, edged_frame, mask = mask)

mask1 = cv2.resize(mask, (960,540))
res1 = cv2.resize(res, (960,540))
edges = cv2.resize(edged_frame, (960,540))

cv2.imshow('mask', mask1)
cv2.imshow('res', res1)
cv2.imshow('edges', edges)

cv2.waitKey(0)
