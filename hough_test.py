import cv2
import numpy as np
import math

img = cv2.imread('test4.jpg')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,150,200,apertureSize = 3)

fast = cv2.FastFeatureDetector_create()
kp = fast.detect(edges, None)

img2 = cv2.drawKeypoints(edges, kp, outImage=np.array([]), color=(255,0,0))

lsd = cv2.createLineSegmentDetector(0)

lines = lsd.detect(edges)[0]

drawn_img = lsd.drawSegments(edges, lines)

alines = cv2.HoughLines(edges,1,np.pi/180,50, None,0,0)
for rho,theta in alines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

img = cv2.resize(img, (960,540))
drawn_img = cv2.resize(drawn_img, (960,540))
edges = cv2.resize(edges, (960,540))

cv2.imshow('cv2lines.jpg', drawn_img)
cv2.imshow('mask.jpg', edges)
cv2.imshow('houghlines.jpg',img2)
#cv2.imshow('edges', edges)

cv2.waitKey(0)
