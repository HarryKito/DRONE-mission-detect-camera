import cv2
import numpy as np

#트렉 바 생성
cv2.createTrackbar("threshold", "HSV", 0, 255, ctr)
cv2.setTrackbarPos("threshold", "HSV",255)

# 트렉 바 현재 값 출력
def ctr(val):
    print(val)

# array [H,S,V] [ Hue(색상), Saturation(채도), Value(명도) ]
#red
red_lower = np.array([0,0,165],np.uint8)
red_upper = np.array([0,0,255],np.uint8)
#green
green_lower = np.array([0,255,0],np.uint8)
green_lower = np.array([0,165,0],np.uint8)
#blue
lower_blue = np.array([110,50,50],np.uint8)
upper_blue = np.array([130,255,255],np.uint8)

#영상 수집 구성
cam = cv2.VideoCapture(0)
aim = cv2.imread('../media/aim.png')

#전체화면 생각중

while cv2.waitKey(1) < 0 :
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    red_target = cv2.inRange(hsv,red_lower,red_upper)

#   cv2.circle(frame, point,radius,colour,lineWidth) # 야 시발 이거로 타겟팅 안 됨?
#    peri = cv2.arcLength(target, True)
#    approx = cv2.approxPolyDP(target, 0.04 * peri, True)
#    cv2.imshow("cam",frame)
    cv2.imshow("hsv", hsv)
    cv2.imshow("target", red_target)

    thresh = cv2.getTrackbarPos("threshold", "Trackbar Windows")

cv2.destroyAllWindows()