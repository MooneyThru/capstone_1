import cv2
from yolov5 import YOLOv5
import json

# YOLOv5 모델 초기화
model_path = 'yolov5s.pt'  # 모델 파일 경로
detector = YOLOv5(model_path)

# 카메라 초기화
cap = cv2.VideoCapture(0)

detected_objects = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 객체 탐지
    results = detector.predict(frame)

    # 탐지된 객체 정보 추출
    for result in results.pred[0]:
        x1, y1, x2, y2, conf, class_id = result
        class_name = results.names[int(class_id)]
        detected_objects.append({
            "class_name": class_name,
            "confidence": float(conf),
            "bbox": [float(x1), float(y1), float(x2), float(y2)]
        })

    # 탐지 결과를 화면에 표시
    cv2.imshow('YOLOv5 Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 파일로 저장 (예: JSON)
with open('detected_objects.json', 'w') as f:
    json.dump(detected_objects, f, indent=4)

cap.release()
cv2.destroyAllWindows()
