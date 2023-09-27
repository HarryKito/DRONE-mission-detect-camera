# DRONE-mission-detect-camera
드론 임무에 사용될 detection 알고리즘 &lt;&lt;PYTHON>>

# 드론
임무 : 낙하점 수류탄 투하 및 타겟 식별
<img width="1222" alt="Screenshot 2023-09-27 at 15 06 59" src="https://github.com/HarryKito/DRONE-mission-detect-camera/assets/71598954/cba8e152-d441-42b9-ae78-c6b804d39071">

## 본 프로젝트의 목적
### 사격자(조종자)에게 타겟 식별과 낙하에 도움을 줄 수 있는 수류탄 낙하용 HUD의 개발.
> 각 칼라값을 개별적으로 검출 [검은색 / 파란색 / 빨간색 / 녹색] 순서로 검출,
> 검출 된 칼라가 사각상자? 혹은 원형인가를 판단하여 목표타겟 좌표습득 (카메라 영상 기준)
> 컬러 (박스 혹은 원형) 검출은 색상 필터링 후 Canny 알고리즘을 적용하는 것으로 고려하고 있음.
> 특정 좌표값 이용하여 근사수치일 경우 자동낙하, 하지만 자동낙하가 불가능할경우 조종자가 사격하기 쉽게
> HUD 창에 낙하점과 목표 타깃과의 상대거리를 동시에 표현

현재 계획중인 예상 낙하 지점 표지
![aim](https://github.com/HarryKito/DRONE-mission-detect-camera/assets/71598954/4f3fef57-3ddc-4f3c-b5fe-2a2de2a40a0d)
