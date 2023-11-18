import cv2
import time

# 카메라 초기화
cap = cv2.VideoCapture(0) # 0은 첫 번째 카메라를 의미

# 캡처 간격 설정 (초 단위)
interval = 2
count = 50

try:
    while True:
        # 현재 시간으로 파일명 생성
        filename = time.strftime(f"23_11_17_1_{count}") + '.jpg'

        # 이미지 캡처
        ret, frame = cap.read()
        if ret:
            # 이미지 저장
            cv2.imwrite(filename, frame)
            print(f'Image saved as {filename}')

            # 캡처된 이미지 표시
            cv2.imshow('Captured_Image', frame)

            # 1초 동안 이미지 표시 후 닫기
            cv2.waitKey(1000)  # 1000ms = 1초
            cv2.destroyAllWindows()

        # 캡처 간격 대기
        count += 1
        time.sleep(interval)

except KeyboardInterrupt:
    print("캡쳐 중단")

finally:
    # 카메라 자원 해제
    cap.release()
