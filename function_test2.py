import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while(1):
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	gray = cv2.GaussianBlur(gray,(5,5),0)
	gray = cv2.medianBlur(gray, 5)
	
	rows = gray.shape[0]
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows/8,
								param1=100, param2=20, minRadius=10, maxRadius=40)
	
	if circles is not None:
		circles = np.uint16(np.around(circles))
		for i in circles[0, :]:
			center = (i[0], i[1])
			# circle center
			cv2.circle(frame, center, 1, (0, 100, 100), 3)
			# circle outline
			radius = i[2]
			cv2.circle(frame, center, radius, (255, 0, 255), 3)
	print(circles)
	cv2.imshow("detected circles", frame)
	k = cv2.waitKey(5)
	if k==27:
		break
	
cap.release()
cv2.destroyAllWindows()
				
	

