import serial
import time
import numpy as np
import robot_arm
import json

# port = '/dev/ttyACM0' # for Linux
port = 'COM3'         # for Windows
robo = serial.Serial(port, 9600)  # 'COM포트'는 아두이노가 연결된 포트로 수정
time.sleep(2)  # 시리얼 통신 시작 후 잠시 대기

print("hello")

def get_first_word_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline()  # 첫 번째 줄 읽기
            first_word = first_line.split()[0]  # 첫 번째 단어 추출
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

# 파일에서 첫 번째 단어 가져오기
file_path = 'cart_items.txt'
first_word = get_first_word_from_file(file_path)

def set_motor_speed(right_speed, left_speed):
    command = f"M1{left_speed}\nM2{right_speed}\n"
    robo.write(command.encode())

def set_servo_angle(servo_number, angle):
    command = f"S{servo_number}{angle}\n"
    robo.write(command.encode())

def retrieve_cart_items(file_path):
    try:
        with open(file_path, 'r') as f:
            items = f.read().split('\n')
            items = [item for item in items if item]
            return items
    except FileNotFoundError:
        print("Cart items file not found.")
        return []

def search_for_object(item):
    while True:
        try:
            object_found = False
            # 파일에서 데이터 불러오기
            with open('detected_objects.json', 'r') as f:
                detected_object = json.load(f)  # 딕셔너리 로드

            # 탐지된 객체가 원하는 객체인지 확인
            if detected_object['class_name'] == item:
                print("Object detected!")
                x_coordinate = detected_object['center_x']  # 객체의 x 좌표
                if 260 <= x_coordinate <= 400:
                    object_found = True
                    set_motor_speed(0, 0)
                    break  # 원하는 객체를 찾고 좌표 범위 내에 있으면 루프를 빠져나옴
                # else:
                #     set_motor_speed(-20, 20)
            else:
                # 물체를 찾지 못했으면 계속 돌기
                set_motor_speed(-20, 20)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unexpected error: {e}")




def inverse_kinematics(x_target, y_target, z_target):
    # 목표점까지의 거리 계산
    d = np.sqrt(x_target ** 2 + y_target ** 2 + z_target ** 2)
    d_prime = np.sqrt((y_target - 10) ** 2 + z_target ** 2)

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
    theta1_deg = np.degrees(theta1)
    theta2_deg = np.degrees(theta2)
    theta3_deg = np.degrees(theta3)

    theta4_deg = 90 - theta2_deg - theta3_deg

    return theta1_deg, theta2_deg, theta3_deg, theta4_deg

def move_to_target(item):
    try:
        with open('detected_objects.json', 'r') as f:
            detected_object = json.load(f)  # 딕셔너리 로드

        # 탐지된 객체가 원하는 객체인지 확인
        if detected_object['class_name'] == item:
            while True:
                distance = detected_object['distance_y']  # 객체의 y 거리

                if distance >= 25:
                    set_motor_speed(60, 60)
                elif 20 <= distance < 25:
                    set_motor_speed(30, 30)
                elif 17 <= distance < 20:
                    set_motor_speed(20, 20)
                else:
                    set_motor_speed(0, 0)
                    break  # 원하는 객체를 찾고 거리 조건에 맞으면 루프를 빠져나옴

        else:
            # 물체를 찾지 못했으면 정지
            set_motor_speed(0, 0)

    except KeyboardInterrupt:
        pass  # 중단 시 아무것도 하지 않음
    except Exception as e:
        print(f"Unexpected error: {e}")

def align_with_object(detected_object):

    # if detected_object == 'giraffe':
    #     item = 'giraffe_head'
    # elif detected_object == 'elephant_doll':
    #     item = 'elephant_head'
    # else:
    #     pass

    while True:
        try:
            object_found = False
            # 파일에서 데이터 불러오기
            with open('detected_objects.json', 'r') as f:
                detected_object = json.load(f)  # 딕셔너리 로드

            if detected_object['class_name'] == item:
                while True:
                        x_coordinate = detected_object['center_x']  # 객체의 x 좌표
                        if 280 <= x_coordinate <= 360:
                            object_found = True
                            set_motor_speed(0, 0)
                            break  # 원하는 객체를 찾고 좌표 범위 내에 있으면 루프를 빠져나옴
                # 모터 정지
                break  # 원하는 객체를 찾았으므로 while 루프를 빠져나옴
            else:
                # 물체를 찾지 못했으면 계속 돌기
                set_motor_speed(-10, 10)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


def grip_coordinate(items):
    # 객체 이름 매핑
    if items == 'giraffe':
        item = 'giraffe_head'
    elif items == 'elephant_doll':
        item = 'elephant_head'
    else:
        item = items  # 기본값으로 items 사용

    try:
        with open('detected_objects.json', 'r') as f:
            detected_object = json.load(f)  # 딕셔너리 로드

        # 탐지된 객체가 원하는 객체인지 확인
        if detected_object['class_name'] == item:
            y_target = detected_object['y_target']
            z_target = detected_object['z_target']
            return y_target, z_target
        else:
            print("Desired item not found in detected objects.")
            return None, None
    except Exception as e:
        print(f"Error reading from JSON: {e}")
        return None, None

def pick_up_object(theta2_deg, theta3_deg, theta4_deg):
    # 서보 모터 2, 3, 4의 각도를 설정
    set_servo_angle(4, theta2_deg)
    set_servo_angle(3, theta3_deg)
    set_servo_angle(2, theta4_deg)
    set_motor_speed(-10,-10)
    time.sleep(1)
    set_motor_speed(10, 10)
    time.sleep(1)
    set_servo_angle(1, 30)
    time.sleep(1)
    # 잡은거 확인 하는

    set_servo_angle(4, 180)
    time.sleep(1)
    set_servo_angle(3, 0)
    time.sleep(1)
    set_servo_angle(2, 100)

def place_object(robot, theta2_deg, theta3_deg, theta4_deg):
    robot.set_servo_angle(4, theta2_deg)
    robot.set_servo_angle(3, theta3_deg)
    robot.set_servo_angle(2, theta4_deg)
    robot.set_motor_speed(-10, -10)
    time.sleep(1)
    robot.set_motor_speed(10, 10)
    time.sleep(1)
    robot.set_servo_angle(1, 80)
    time.sleep(1)
    # 잡은거 확인 하는

    # 로봇팔 원위치
    robot.set_servo_angle(4, 180)
    time.sleep(1)
    robot.set_servo_angle(3, 0)
    time.sleep(1)
    robot.set_servo_angle(2, 100)
    time.sleep(1)


# 아두이노와 시리얼 통신 설정
# 링크 길이 정의
link1_length = 12.0
link3_length = 12.0
link4_length = 10.0


while True:
    try:
        if first_word:
            #print("First word in the file:", first_word)
            cart_item = first_word
            print(f"you have chosen : {cart_item}")
            time.sleep(3)

        if cart_item == 'elephant':
            item = 'elephant_doll'
        elif cart_item == 'monkey':
            item = 'monkey_doll'
        else:
            item = cart_item

        search_for_object(item)
        move_to_target(item)
        # # 물체 정중앙 위치시키기
        align_with_object(item)

        # 좌푯값 가져와서 잡기
        x_target = 0
        y_target, z_target = grip_coordinate(item)
        theta2_deg, theta3_deg, theta4_deg = robot_arm.inverse_kinematics(x_target, y_target, z_target)
        pick_up_object(theta2_deg, theta3_deg, theta4_deg)

        item = 'target_item'

        # 물체의 좌표를 가져와서 로봇 암을 해당 위치로 이동
        search_for_object(item)
        move_to_target(item)
        # 좌푯값 가져와서 내려 놓기
        align_with_object(item)
        x_target, y_target, z_target = grip_coordinate(item)
        theta2_deg, theta3_deg, theta4_deg = robot_arm.inverse_kinematics(x_target, y_target, z_target)

        # 설정된 위치에 물체를 내려놓기
        place_object(theta2_deg, theta3_deg, theta4_deg)

        #마지막 카트 에 아이템 지우기
        with open('cart_items.txt', 'r') as file:
            lines = file.readlines()

        # 'item'을 제외한 나머지 줄들을 유지
        lines = [line for line in lines if line.strip() != item]
        if lines:
            lines[0] = lines[0].strip()

        # 파일 다시 쓰기
        with open('cart_items.txt', 'w') as file:
            file.writelines(lines)

    except KeyboardInterrupt:
        break
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")