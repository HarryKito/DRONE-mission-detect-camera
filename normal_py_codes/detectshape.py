import cv2
import numpy as np

class mode: # 열거형 안되나..
    cam_modes = ["cam","detection","square aim","aim to specific","circle aim"] # C 키로 동작하도록
    flight_modes = ["manual flight","drop bomb","find target"] # F 키로 동작하도록

    current_cam = 0
    current_flight = 0

    shape_text_color = (255,0,255)
    kernel = np.ones((5,5))
    clearness = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

    aim = cv2.imread('../media/aim.png')
    aim_L = (150,50)
    aim_R = (0,0)

    brightness = 1
    contrast = 1

    threshold           = 20
    Canny_threshold1    = 101 #105
    Canny_threshold2    = 57 #175 적절함
    area_scale          = 4000

    def __init__(self) -> None:
        print("modes class activate")

    def change_cam(self) -> None:
        self.current_cam = self.current_cam + 1 if len(self.cam_modes) - 1 > self.current_cam else  0
        print(" cam mode changed :: ",self.cam_modes[self.current_cam])

    def change_flight(self) -> None:
        self.current_flight = self.current_flight + 1 if len(self.flight_modes) - 1 > self.current_flight else  0
        print(" flight mode changed :: ",self.flight_modes[self.current_flight])

# 카메라 출력 제어부
    def cam_detection(self,frame):
        if self.cam_modes[self.current_cam] == "cam":
            pass
            #frame = cv2.filter2D(frame, -1, self.clearness)

        elif self.cam_modes[self.current_cam] == "detection":
            blurred = cv2.GaussianBlur(frame, (5, 5), 0)
            gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
            canny = cv2.Canny(gray,self.Canny_threshold1,self.Canny_threshold2)
            dilate = cv2.dilate(canny,self.kernel,iterations=1)
            cnts,_ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(frame,cnts,-1,(0,255,0),7)

        # 사각형 검출
        elif self.cam_modes[self.current_cam] == "square aim":
            blurred = cv2.GaussianBlur(frame, (5, 5), 0)
            gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
            canny = cv2.Canny(gray,self.Canny_threshold1,self.Canny_threshold2)
            dilate = cv2.dilate(canny,self.kernel,iterations=1)
            cnts,hir = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for cnt in cnts:
                area = cv2.contourArea(cnt)
                if area > Mode.area_scale and area < 8000:
                    period = cv2.arcLength(cnt,True)
                    approx = cv2.approxPolyDP(cnt, 0.04 * period, True)
                    if len(approx) == 4:
                        x,y,w,h = cv2.boundingRect(approx)
                        cv2.drawContours(frame,cnt,-1,(0,255,0),7)
                        cv2.rectangle(frame,(x,y),(x+w,y+h),Mode.shape_text_color,5)
                        cv2.putText(frame,"points:"+str(len(approx)),(x+w+20,y+20),cv2.FONT_HERSHEY_COMPLEX,.7,Mode.shape_text_color,2)
                        cv2.putText(frame,"area:"+str(int(area)),(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,.7,(255,0,0),2)
                        cv2.putText(frame,"target:"+str(x)+","+str(y),(x+w+20,y+70),cv2.FONT_HERSHEY_COMPLEX,.7,Mode.shape_text_color,2)

        elif self.cam_modes[self.current_cam] == "aim to specific":
            frame = cv2.filter2D(frame, -1, self.clearness)
            yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
            frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB)

        
        elif self.cam_modes[self.current_cam] == "circle aim":
            blur = cv2.GaussianBlur(frame, (5, 5), 0)
            gray = cv2.cvtColor(blur,cv2.COLOR_RGB2GRAY)
#            circles = cv2.HoughCircles(gray,circles,1,20, param1=50,param2=30,minRadius=0,maxRadius=0)
#            circles = np.uint16(np.around(circles))
#            print(circles)
#            for i in circles[0]:
#                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 3)


        else:
            print("mode error!")
            pass

    def change_threshold(self,value) -> None:
        print(value)

    def parameter_display(self) -> None:
        cv2.namedWindow('params')
        cv2.createTrackbar('threshold', 'params',self.threshold, 255, self.change_threshold)
        cv2.createTrackbar('Canny_threshold1','params',self.Canny_threshold1,255,self.change_threshold)
        cv2.createTrackbar('Canny_threshold2','params',self.Canny_threshold2,360,self.change_threshold)
        cv2.createTrackbar('area scale','params',self.area_scale,8000,self.change_threshold)

    def get_param(self) -> None:
        self.threshold = cv2.getTrackbarPos('threshold','params')
        self.Canny_threshold1 = cv2.getTrackbarPos('Canny_threshold1','params')
        self.Canny_threshold2 = cv2.getTrackbarPos('Canny_threshold2','params')
        self.area_scale = cv2.getTrackbarPos('area scale','params')

    def draw_text(self,img, text, font=cv2.FONT_HERSHEY_PLAIN, pos=(0, 0), font_scale=3,
          font_thickness=2, text_color=(0, 255, 0), text_color_bg=(0, 0, 0) ):
        x, y = pos
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
        cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

#    def draw_overlay(self,frame):
#        if self.cam_modes[self.current_cam] == "square aim" or "circle aim":
#        frame = cv2.addWeighted(frame,0.4,aim,0.1,0)
# Mode class 끝

if __name__ == "__main__":

    server = 0#"rtsp://192.168.144.25:8554/main.264"
    Mode = mode()
    cam = cv2.VideoCapture(server)

    Mode.parameter_display()

# 영상 수신 시작
    while True:
        key = cv2.waitKeyEx(1)
        if key == 27:
            print("exit")
            break
        elif key == ord('c'):
            Mode.change_cam()
        elif key == ord('f'):
            Mode.change_flight()    
        elif key== ord(']'): # 방향키 방향 전환 0x260000==up
            Mode.brightness = Mode.brightness + 1
        elif key==ord('['): # 방향키 방향 전환 0x280000==down
            Mode.brightness = Mode.brightness - 1
        elif key==ord('.'): # 방향키 방향 전환 0x270000==right
            Mode.contrast = Mode.contrast + 0.01
        elif key==ord(','): # 방향키 방향 전환 0x250000==left
            Mode.contrast = Mode.contrast - 0.01

        # 트랙 바 정보수집
        Mode.get_param()

        #카메라 데이터 수집
        _, frame = cam.read()
  
        #영상처리
        Mode.cam_detection(frame)

        cv2.line(img=frame, pt1=(0, 120), pt2=(800, 120), color=(255, 255, 255), thickness=5,lineType=8,shift=0)
        Mode.draw_text(frame, "brightness : "+str(Mode.brightness)+" contrast : "+str(Mode.contrast), font_scale=1, pos=(0, 0), text_color_bg=(0, 0,  0))
        cv2.imshow("target", frame)

    cam.release()
    cv2.destroyAllWindows()