import cv2
import numpy as np
import imutils

def change_threshold(value):
    print(value)

def detection(p):
    period = cv2.arcLength(p,True)
    approx = cv2.approxPolyDP( p, 0.04 * period, True )
    if len(approx) == 4:
        (x,y,w,h) = cv2.boundingRect(approx)
        return "square"
    else:
        return "circle"

# 이미지 stacking
def StackVideo(scale,array):
    rows = len(array)
    cols = len(array[0])
    rowsAvailable = isinstance(array[0],list)
    width = array[0][0].shape[1]
    height = array[0][0].shape[0]
    
    if rowsAvailable:
        for x in range(0,rows):
            for y in range(0, cols):
                if array[x][y].shape[:2] == array[0][0].shape[:2]:
                    array[x][y] = cv2.resize(array[x][y],(0,0),None,scale,scale)
                else:
                    array[x][y] = cv2.resize(array[x][y], (array[0][0].shape [1], array[0][0].shape [0]), None, scale, scale)
                if len(array[x][y].shape) == 2: array[x][y] = cv2.cvtColor(array[x][y], cv2.COLOR_GRAY2BGR)
            imgBlank = np.zeros((height,width,3),np.uint8)
            hor = [imgBlank] * rows
            hor_con = [imgBlank] * rows
            for x in range(0,rows):
                hor[x] = np.hstack(array[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if array[x].shape[:2] == array[0].shape[:2]:
                    array[x] = cv2.resize(array[x],(0,0),None,scale,scale)
                else:
                    array[x] = cv2.resize(array[x], (array[0].shape[1], array[0].shape[0]),None,scale,scale)
                if len(array[x].shape) == 2: array[x] = cv2.cvtColor(array[x],cv2.COLOR_GRAY2BGR)
            hor = np.hstack(array)
            ver = hor
        return ver
        
ratio = 4.285714285714286 # 카메라 사용 전 설정할 것.

threshold = 60
Canny_threshold1 = 0 #105
Canny_threshold2 = 0 #175 적절함

cam = cv2.VideoCapture(0)
cv2.namedWindow('params')
cv2.resizeWindow('params',800,500)
cv2.createTrackbar('threshold', 'params', threshold, 255, change_threshold)
cv2.createTrackbar('Canny_threshold1','params',Canny_threshold1,255,change_threshold)
cv2.createTrackbar('Canny_threshold2','params',Canny_threshold2,360,change_threshold)

#stacking = StackVideo(0.8,([frame,blurred,thresh]))

while cv2.waitKey(1) < 0 :
    threshold = cv2.getTrackbarPos('threshold','params')
    Canny_threshold1 = cv2.getTrackbarPos('Canny_threshold1','params')
    Canny_threshold2 = cv2.getTrackbarPos('Canny_threshold2','params')

    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
    canny = cv2.Canny(thresh,Canny_threshold1,Canny_threshold2)

    #필터링 영상에 canny 알고리즘을 적용하고자 함.
    #but 기존의 필터링 된 영상에 canny 적용이 어려움. 

#    cnts = imutils.grab_contours(cnts)
#    cnts,hir = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
#    for c in cnts:
#        M = cv2.moments(c)
#        if M['m00'] != 0.0:
#            cX = int(M['m10']/M['m00'])
#            cY = int(M['m01']/M['m00'])

#        c = c.astype("float")
#        c *= ratio
#        c = c.astype("int")

#        shape = detection(c)
#        cv2.drawContours(canny, [c], -1, (0, 255,0), 2)
#        cv2.putText(canny, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#        cv2.imshow("target",canny)

    cv2.imshow("target", canny)

cam.release()
cv2.destroyAllWindows()