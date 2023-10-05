import cv2
import numpy as np

# 트렉 바 값 출력
def ctr(val):
    print(val)

#비디오
cap = cv2.VideoCapture('../media/fail.mp4')

# 폭격지점
aim = cv2.imread('../media/aim.png',cv2.IMREAD_COLOR)

cv2.imshow('wa',aim)

while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()