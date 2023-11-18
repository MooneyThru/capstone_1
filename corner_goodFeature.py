import cv2
import numpy as np

# 이미지를 로드하고 그레이스케일로 변환
image = cv2.imread('giraffe.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 외곽선 검출
contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 외곽선 간 최소 거리 계산
min_distance = float('inf')
closest_points = None

for i in range(len(contours)):
    for j in range(i + 1, len(contours)):
        for point1 in contours[i]:
            for point2 in contours[j]:
                distance = np.linalg.norm(point1 - point2)
                if distance < min_distance:
                    min_distance = distance
                    closest_points = (point1, point2)

# 결과 출력
print(f"최소 거리: {min_distance}")
print(f"가장 가까운 점들의 좌표: {closest_points[0]}, {closest_points[1]}")
