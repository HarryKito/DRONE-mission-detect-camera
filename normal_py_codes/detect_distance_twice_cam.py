import cv2
import numpy as np

# 스테레오 카메라 초기화
cap_left = cv2.VideoCapture(0)
cap_right = cv2.VideoCapture(1)

if not cap_left.isOpened() or not cap_right.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 카메라 설정
cap_left.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap_left.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap_right.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap_right.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 스테레오 카메라 설정
f = 1000.0  # 초점거리
B = 0.1     # 카메라 간 거리
Q = np.array([[1, 0, 0, -320],
              [0, 1, 0, -240],
              [0, 0, 0, f],
              [0, 0, -1.0/B, 0]])

while True:
    # 카메라 영상 읽기
    ret_left, img_left = cap_left.read()
    ret_right, img_right = cap_right.read()
    
    if not ret_left or not ret_right:
        print("영상을 읽을 수 없습니다.")
        break
    
    # 스테레오 매칭
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=9)
    img_disparity = stereo.compute(img_left, img_right)
    
    # 거리 계산
    img_depth = cv2.convertScaleAbs(img_disparity, alpha=1/16.0)
    img_distance = -f*B/img_depth
    
    # 거리 출력
    print("거리: {} m".format(img_distance[240, 320]))
    
    # 화면에 영상 출력
    cv2.imshow("left", img_left)
    cv2.imshow("right", img_right)
    cv2.imshow("depth", img_distance)
    
    # 키 입력 대기
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료
cap_left.release()
cap_right.release()
cv2.destroyAllWindows()
