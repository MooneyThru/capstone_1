import serial
import time
import numpy as np
import json

# port = '/dev/ttyACM0' # for Linux
port = 'COM7'         # for Windows
robo = serial.Serial(port, 9600)
time.sleep(2)

# 전역 변수 선언
item = None
theta1_deg = 0
theta2_deg = 0
theta3_deg = 0
theta4_deg = 0
def get_first_word_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline()
            first_word = first_line.split()[0]
            return first_word
    except FileNotFoundError:
        print("File not found.")
        return None
    except IndexError:
        print("No word found in the first line.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def set_motor_speed(left_speed, right_speed):
    robo.write(f"M2{right_speed}\n".encode())
    robo.write(f"M1{left_speed}\n".encode())
def set_servo_angle(servo_number, angle):
    command = f"S{servo_number}{angle}\n"
    robo.write(command.encode())
def get_last_object(item):
    try:
        with open('detected_objects.json', 'r') as f:
            detected_objects = json.load(f)
        # item과 일치하는 class_name을 가진 객체만 필터링
        matching_objects = [obj for obj in detected_objects if obj['class_name'] == item]
        return matching_objects[-1] if matching_objects else None
    except Exception as e:
        print(f"Error reading from JSON: {e}")
        return None
def search_for_object(item, algorithm_number):
    while True:
        try:
            # item과 일치하는 class_name을 가진 객체만 필터링
            detected_object = get_last_object(item)
            if detected_object:
                # 마지막 객체 가져오기
                x_coordinate = detected_object['center_x']  # 객체의 x 좌표
                print(f"object detected search_for_object : {x_coordinate} / 460")
                set_motor_speed(0, 0)
                if 320 <= x_coordinate <= 410:
                    set_motor_speed(0, 0)
                    print("Object found and within range.")
                    print("---------------break---------------")
                    break  # 원하는 객체를 찾고 좌표 범위 내에 있으면 루프를 빠져나옴
                elif x_coordinate < 320:
                    if algorithm_number % 2 == 1:
                        set_motor_speed(-2, 2)
                    else:
                        set_motor_speed(-3, 3)
                    time.sleep(1)
                    set_motor_speed(0, 0)
                    time.sleep(1)
                    print("Object found but not within range. Adjusting position...")

                elif 410 < x_coordinate:
                    if algorithm_number % 2 == 1:
                        set_motor_speed(2, -2)
                    else:
                        set_motor_speed(3, -3)
                    time.sleep(1)
                    set_motor_speed(0, 0)
                    time.sleep(1)
                    print("Object found but not within range. Adjusting position...")

            else:
                print("searching item : ", item)
                if algorithm_number % 2 == 1:
                    set_motor_speed(-3, 3)
                else:
                    set_motor_speed(3, -3)
                time.sleep(1)
                set_motor_speed(0, 0)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
def move_to_target(item):
    print("move_to_target")
    while True:
        try:
            detected_object = get_last_object(item)
            class_name = detected_object.get('class_name', None)  # 기본값 None으로 설정

            if class_name in ['giraffe_head', 'dinosaur']:
                distance = detected_object['distance_y']  # 객체의 y 거리
                print("distance_y :", distance)

                if distance >= 35:
                    set_motor_speed(15, 15)
                    print("speed 7, 7")
                elif 28 <= distance < 35:
                    set_motor_speed(6, 6)
                    print("speed 6, 6")
                    time.sleep(1)
                elif 20 <= distance < 28:
                    set_motor_speed(0, 0)
                    time.sleep(1)
                    print("----------   speed 0, 0   ---------")
                    break
                elif distance < 32:
                    set_motor_speed(-5, -5)
                    time.sleep(3)
                    set_motor_speed(0, 0)
                    time.sleep(1)
                    print("backward")
            elif class_name in ['box']:
                distance = detected_object['distance_y']  # 객체의 y 거리
                print("distance_y :", distance)

                if distance >= 37:
                    set_motor_speed(13, 13)
                    print("box speed 7, 7")

                elif 33 <= distance < 37:
                    set_motor_speed(6, 6)
                    print("box speed 6, 6")
                    time.sleep(1)

                elif 28 <= distance < 33:
                    set_motor_speed(0, 0)
                    time.sleep(1)
                    print("box --------------------   speed 0, 0   --------------------")
                    break

                elif distance < 28:
                    set_motor_speed(-5, -5)
                    time.sleep(3)
                    set_motor_speed(0, 0)
                    time.sleep(1)
                    print("backward")
            else:
                search_for_object(item,1)
                print("Object not found.")

            time.sleep(1)
        except KeyboardInterrupt:
            pass
        except KeyError as e:
            print(f"Key not found in detected_object: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
def align_with_object(item):
    while True:
        print("align_with_object")
        try:
            detected_object = get_last_object(item)  # 루프 내에서 객체 정보 갱신
            class_name = detected_object.get('class_name', None)
            print(f"aligning item!! {detected_object['class_name']}")
            if class_name in ['dinosaur'] :
                x_coordinate = detected_object['center_x']
                print("align_with_object: ", x_coordinate)
                if 240 <= x_coordinate <= 290:
                    set_motor_speed(0, 0)
                    time.sleep(1)
                    print("Object found and within range.")
                    break
                elif x_coordinate < 240:
                    set_motor_speed(-3, 3)
                    time.sleep(1)
                    set_motor_speed(0, 0)
                    print("Object found but not within range. Adjusting position...")
                    return True
                elif 290 < x_coordinate:
                    set_motor_speed(3, -3)
                    time.sleep(1)
                    set_motor_speed(0, 0)
                    print("Object found but not within range. Adjusting position...")
                    return True
            elif class_name in ['giraffe_head']:
                x_coordinate = detected_object['center_x']
                print("align_with_object: ", x_coordinate)
                if 270 <= x_coordinate <= 320:
                    set_motor_speed(0, 0)
                    time.sleep(1)
                    print("Object found and within range.")
                    break
                elif x_coordinate < 270:
                    set_motor_speed(-3, 3)
                    time.sleep(1)
                    set_motor_speed(0, 0)
                    print("Object found but not within range. Adjusting position...")
                    return True
                elif 320 < x_coordinate:
                    set_motor_speed(3, -3)
                    time.sleep(1)
                    set_motor_speed(0, 0)
                    print("Object found but not within range. Adjusting position...")
                    return True
            elif class_name in ['box']:
                x_coordinate = detected_object['center_x']
                if 190 <= x_coordinate <= 240:
                    set_motor_speed(0, 0)
                    print("Object found and within range.")
                    print("---------------break---------------")
                    break  # 원하는 객체를 찾고 좌표 범위 내에 있으면 루프를 빠져나옴
                elif x_coordinate < 190:
                    set_motor_speed(-3, 3)
                    time.sleep(1)
                    set_motor_speed(0, 0)
                    time.sleep(2)
                    print("Object found but not within range. Adjusting position...")
                    return True
                elif 240 < x_coordinate:
                    set_motor_speed(3, -3)
                    time.sleep(1)
                    set_motor_speed(0, 0)
                    time.sleep(2)
                    print("Object found but not within range. Adjusting position...")
                    return True
            else:
                print("Object not found. Searching for object.")
                move_to_target(item)  # 객체를 찾지 못했을 때 탐색

        except KeyboardInterrupt:
            print("Interrupted by user.")
        except Exception as e:
            print(f"Unexpected error: {e}")
def inverse_kinematics(x_target, y_target, z_target):
    # 목표점까지의 거리 계산
    d = np.sqrt(x_target ** 2 + y_target ** 2 + z_target ** 2)
    d_prime = np.sqrt((y_target - 10) ** 2 + z_target ** 2)
    print(d_prime)
    time.sleep(1)
    # 가능한 위치인지 체크
    if d_prime > np.sqrt( link1_length ** 2 + link3_length ** 2 ):
        raise ValueError("Target is unreachable")

    # 어깨 관절 각도 계산 (평면에 대한 회전)
    theta1 = np.arctan2(y_target, x_target)

    # Inverse Kinematics 공식을 사용하여 theta2와 theta3를 계산합니다.
    cos_theta3 = (d_prime ** 2 - link1_length ** 2 - link3_length ** 2) / (2 * link1_length * link3_length)
    # 여기서 cos_theta3의 값이 [-1, 1] 범위 내에 있는지 확인합니다.
    if not -1 <= cos_theta3 <= 1:
        raise ValueError("cos_theta3 out of range, invalid target position")

    # cos_theta3 값에 따라 theta3 계산
    theta3 = np.arccos(cos_theta3)

    # theta2 계산
    sin_theta3 = np.sqrt(1 - (cos_theta3 ** 2))
    k1 = link1_length + (link3_length * cos_theta3)
    k2 = link3_length * sin_theta3

    theta2 = np.arctan2((y_target - 10), z_target) - np.arctan2(k2, k1)

    # 각도를 도(degree)로 변환
    theta1_deg = round(np.degrees(theta1),2)
    theta2_deg = round(np.degrees(theta2),2)
    theta3_deg = round(np.degrees(theta3),2)

    if (theta3_deg + theta2_deg) >= 90:
        theta4_deg = theta2_deg + theta3_deg - 90
    else:
        theta4_deg = 90 - theta2_deg - theta3_deg

    theta4_deg = 90 + theta4_deg
    theta2_deg = 90 - theta2_deg
    return theta1_deg, theta2_deg, theta3_deg, theta4_deg
def pick_up_object(item, theta2_deg, theta3_deg, theta4_deg):
    try:
        detected_object = get_last_object(item)  # 루프 내에서 객체 정보 갱신
        class_name = detected_object.get('class_name', None)
        print(f"aligning item!! {detected_object['class_name']}")
        print("pick_up_object")
        if class_name in ['dinosaur']:
            set_servo_angle(4, 120)
            time.sleep(2)
            set_motor_speed(-10, -10)
            time.sleep(3)
            set_motor_speed(0, 0)
            time.sleep(1)
            # 서보 모터 2, 3, 4의 각도를 설정
            set_servo_angle(1, theta2_deg)
            time.sleep(1)
            set_servo_angle(2, theta3_deg)
            time.sleep(1)
            set_servo_angle(3, theta4_deg)
            time.sleep(1)
            set_motor_speed(11, 10)
            time.sleep(5)
            set_motor_speed(0, 0)
            time.sleep(1)
            set_servo_angle(4, 30)
            time.sleep(3)
            # 잡은거 확인 하는
            set_servo_angle(1, 90)
            time.sleep(1)
            set_servo_angle(2, 30)
            time.sleep(1)
            set_servo_angle(3, 50)
            time.sleep(1)
        else:
            set_servo_angle(4, 120)
            time.sleep(2)
            set_motor_speed(-10, -10)
            time.sleep(3)
            set_motor_speed(0, 0)
            time.sleep(1)
            # 서보 모터 2, 3, 4의 각도를 설정
            set_servo_angle(1, theta2_deg)
            time.sleep(1)
            set_servo_angle(2, theta3_deg)
            time.sleep(1)
            set_servo_angle(3, theta4_deg)
            time.sleep(1)
            set_motor_speed(10, 10)
            time.sleep(3)
            set_motor_speed(0, 0)
            time.sleep(1)
            set_servo_angle(4, 30)
            time.sleep(3)
            # 잡은거 확인 하는
            set_servo_angle(1, 90)
            time.sleep(1)
            set_servo_angle(2, 30)
            time.sleep(1)
            set_servo_angle(3, 50)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
def place_object():
    print("place_object")
    set_servo_angle(4, 30)
    time.sleep(1)
    set_motor_speed(10, 10)  # 5cm delay(2) 10cm delay(3)
    time.sleep(3.5)
    set_motor_speed(0,0)
    time.sleep(1)
    set_servo_angle(1, 60)
    time.sleep(2)
    set_servo_angle(2, 30)
    time.sleep(2)
    set_servo_angle(3, 70)
    time.sleep(1)
    set_servo_angle(4, 120)
    time.sleep(1)
    # 로봇팔 원위치
    set_servo_angle(1, 90)
    time.sleep(1)
    set_servo_angle(2, 0)
    time.sleep(1)
    set_servo_angle(3, 90)
    time.sleep(1)

# 링크 길이 정의
link1_length = 12.0
link3_length = 12.0
link4_length = 10.0
file_path = 'cart_items.txt'
cart_item = None  # 초기화 추가

def main():
    while True:
        try:
            first_word = get_first_word_from_file(file_path)
            if first_word:
                cart_item = first_word
                print(f"you have chosen : {cart_item}")
                time.sleep(1)

                if cart_item == 'giraffe':
                    rev_remove_item = cart_item
                    count = 1
                    item = 'giraffe_head'
                    x_target = 0
                    y_target = 25
                    z_target = 7
                elif cart_item == 'dinosaur':
                    count = 2
                    rev_remove_item = cart_item
                    item = 'dinosaur'
                    x_target = 0
                    y_target = 24
                    z_target = 8
                    # 스위치 문으로 변환


                if count % 2 == 0:  # Even count
                    search_for_object(item, 1)
                else:  # Odd count
                    search_for_object(item, 2)

                move_to_target(item)
                # 물체 정중앙 위치시키기
                align_with_object(item)

                # 좌푯값 가져와서 잡기
                theta1_deg, theta2_deg, theta3_deg, theta4_deg = inverse_kinematics(x_target, y_target, z_target)
                print( "angle : ", theta2_deg, ", ", theta3_deg, ", ", theta4_deg)
                time.sleep(1)
                pick_up_object(item,theta2_deg, theta3_deg, theta4_deg)
                set_motor_speed(0,0)

                item = 'box'
                if item == 'box':
                    box_height = 12
                    y_target = 20
                    z_target = box_height

                set_motor_speed(-20,-20)
                time.sleep(3)
                set_motor_speed((0,0))
                time.sleep(1)
                print(item)
                # # 물체의 좌표를 가져와서 로봇 암을 해당 위치로 이동
                if count % 2 == 0:  # Even count
                    search_for_object(item, 1)
                else:  # Odd count
                    search_for_object(item, 2)

                move_to_target(item)
                # 좌푯값 가져와서 내려 놓기
                align_with_object(item)
                set_motor_speed(10, 10)
                time.sleep(2)
                set_motor_speed(0, 0)
                # 설정된 위치에 물체를 내려놓기
                place_object()

                set_motor_speed(-10, -10)
                time.sleep(3)
                set_motor_speed((0, 0))
                time.sleep(1)

                # 마지막 카트에 아이템 지우기
                item_to_remove = rev_remove_item
                count += 1

                with open('cart_items.txt', 'r') as file:
                    lines = file.readlines()

                # 'item_to_remove'를 제외한 나머지 줄들을 유지
                lines = [line for line in lines if line.strip() != item_to_remove]

                with open('cart_items.txt', 'w') as file:
                    file.writelines(lines)
                print("DONE!")
                time.sleep(2)
            else:
                set_motor_speed(0, 0)
                time.sleep(2)

        except KeyboardInterrupt:
            break
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()