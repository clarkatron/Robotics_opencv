import cv2
import numpy as np
import math
import time

def main():
    
    windowName = "Nice window b*rho"
    cv2.namedWindow(windowName)
    frame = cv2.imread('test4.jpg')
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grey, 50, 100, apertureSize=3, L2gradient=True)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 250)
    #ref = cv2.line(frame,(0,240),(640,240),(255,0,0),2)
	
	if lines is not None:
		for rho, theta in lines[0]:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			pts1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
			pts2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
			cv2.line(frame, pts1, pts2, (0,255,0), 2)
			#cv2.circle(frame, (x0,y0), 10, (0,0,255), -1)
			
			Hslope = y0/x0
			angle = math.atan((Hslope - 0)/(1 + Hslope*0))
			Hangle = -angle*(180/np.pi)
			print(Hangle+90)
	
	#print(time.time() - start_time)
	cv2.imshow(windowName, frame)
	cv2.imwrite('test.png', frame)

	if cv2.waitKey(1) == 27:
		break

cv2.destroyAllWindows()
cap.release()
    
if __name__ == "__main__":
    main()
    
