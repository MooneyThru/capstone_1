import json

# 파일에서 데이터 불러오기
with open('detected_objects.json', 'r') as f:
    detected_objects = json.load(f)

# 불러온 데이터 사용
for obj in detected_objects:
    print(obj)
