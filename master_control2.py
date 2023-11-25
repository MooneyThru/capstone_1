import serial
import time
import numpy as np
# import robot_arm
import json
import threading

# port = '/dev/ttyACM0' # for Linux
port = 'COM3'         # for Windows
robo = serial.Serial(port, 9600)  # 'COM포트'는 아두이노가 연결된 포트로 수정
time.sleep(2)  # 시리얼 통신 시작 후 잠시 대기
# 파일에서 첫 번째 단어 가져오기

# 전역 변수 선언
item = None
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

def set_motor_speed(right_speed, left_speed):
    robo.write(f"M1{right_speed}\n".encode())
    robo.write(f"M2{left_speed}\n".encode())

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
def search_for_object(item):
    while True:
        try:
            object_found = False

            # item과 일치하는 class_name을 가진 객체만 필터링
            detected_object = get_last_object(item)

            if detected_object:
                # 마지막 객체 가져오기
                print("object detected")
                x_coordinate = detected_object['center_x']  # 객체의 x 좌표
                print(x_coordinate)
                if 260 <= x_coordinate <= 400:
                    object_found = True
                    set_motor_speed(0, 0)
                    print("Object found and within range.")
                    break  # 원하는 객체를 찾고 좌표 범위 내에 있으면 루프를 빠져나옴
                else:
                    set_motor_speed(-20, 20)
                    print("Object found but not within range. Adjusting position...")
            else:
                print("No object found with class_name:", item)
                # 물체를 찾지 못했으면 계속 돌기
                set_motor_speed(-20, 20)
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
            if detected_object:
                distance = detected_object['distance_y']  # 객체의 y 거리
                print(distance)
                if distance >= 25:
                    set_motor_speed(30, 30)
                    print("30, 30")
                elif 20 <= distance < 25:
                    set_motor_speed(20, 20)
                    print("20, 20")
                elif 17 <= distance < 20:
                    set_motor_speed(0, 0)
                    print("0, 0")
                    break
                else:
                    set_motor_speed(0, 0)
                    print("pause")
            else:
                print("Object not found.")
                search_for_object(item)

            time.sleep(1)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Unexpected error: {e}")

def align_with_object(item):
    while True:
        print("align_with_object")
        try:
            detected_object = get_last_object(item)  # 루프 내에서 객체 정보 갱신
            if detected_object:
                print("align_with_object")
                x_coordinate = detected_object['center_x']  # 객체의 x 좌표
                print(x_coordinate)
                if 280 <= x_coordinate <= 360:
                    set_motor_speed(0, 0)
                    print("Object aligned.")
                    break
                elif x_coordinate > 360:
                    set_motor_speed(20, -20)
                    print("Adjusting position to the left.")
                else:
                    set_motor_speed(-20, 20)
                    print("Adjusting position to the right.")
            else:
                print("Object not found. Searching for object.")
                search_for_object(item)  # 객체를 찾지 못했을 때 탐색

            time.sleep(1)
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
    theta1_deg = np.degrees(theta1)
    theta2_deg = np.degrees(theta2)
    theta3_deg = np.degrees(theta3)

    theta4_deg = 90 - theta2_deg - theta3_deg

    return theta1_deg, theta2_deg, theta3_deg, theta4_deg



def grip_coordinate(item):
    try:
        print("grip_coordinate!!")
        detected_object = get_last_object(item)
        if detected_object:
            y_target = detected_object['distance_y']
            z_target = detected_object['z_target']
            return y_target, z_target
        else:
            print("Desired item not found in detected objects.")
            return None, None
    except Exception as e:
        print(f"Error reading from JSON: {e}")
        return None, None


def pick_up_object(theta2_deg, theta3_deg, theta4_deg):

    print("pick_up_object")
    # 서보 모터 2, 3, 4의 각도를 설정
    set_servo_angle(4, theta2_deg)
    time.sleep(1)
    set_servo_angle(3, theta3_deg)
    time.sleep(1)
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
    print("place_object")
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
file_path = 'cart_items.txt'
cart_item = None  # 초기화 추가

print("0")

def mainthread(file_path):
    global item
    while True:
        try:
            first_word = get_first_word_from_file(file_path)
            if first_word:
                #print("First word in the file:", first_word)
                cart_item = first_word
                print(f"you have chosen : {cart_item}")
                time.sleep(1)

            if cart_item == 'elephant':
                item = 'elephant_doll'
            elif cart_item == 'monkey':
                item = 'monkey_doll'
            else:
                item = cart_item
            print("1")

            time.sleep(1)

            search_for_object(item)
            time.sleep(1)
            print("2")
            move_to_target(item)
            time.sleep(1)
            # 물체 정중앙 위치시키기
            align_with_object(item)
            time.sleep(1)
            # 좌푯값 가져와서 잡기
            x_target = 0
            y_target, z_target = grip_coordinate(item)

            print(y_target, " and ", z_target)
            time.sleep(1)
            theta1_deg, theta2_deg, theta3_deg, theta4_deg = inverse_kinematics(x_target, y_target, z_target)
            print(theta1_deg, ", ", theta2_deg, ", ", theta3_deg, ", ", theta4_deg)
            time.sleep(1)
            pick_up_object(theta2_deg, theta3_deg, theta4_deg)
            #
            # item = 'target_item'
            #
            # # 물체의 좌표를 가져와서 로봇 암을 해당 위치로 이동
            # search_for_object(item)
            # move_to_target(item)
            # # 좌푯값 가져와서 내려 놓기
            # align_with_object(item)
            # y_target, z_target = grip_coordinate(item)
            # theta2_deg, theta3_deg, theta4_deg = inverse_kinematics(x_target, y_target, z_target)
            #
            # # 설정된 위치에 물체를 내려놓기
            # place_object(theta2_deg, theta3_deg, theta4_deg)

            #마지막 카트 에 아이템 지우기
            # 마지막 카트에 아이템 지우기
            # with open('cart_items.txt', 'r+') as file:
            #     lines = file.readlines()
            #     file.seek(0)  # 파일 포인터를 시작 지점으로 이동
            #     file.truncate()  # 파일 내용을 현재 위치에서 잘라냄
            #
            #     # 'item'을 제외한 나머지 줄들을 유지
            #     lines = [line for line in lines if line.strip() != item]
            #
            #     # 파일 다시 쓰기
            #     file.writelines(lines)


        except KeyboardInterrupt:
            break
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def camera5():
    global item
    angle = 90
    while True:
        try:
            detected_object = get_last_object(item)  # 루프 내에서 객체 정보 갱신
            if detected_object:
                up_y = detected_object['y1_up']  # 객체의 x 좌표
                down_y = detected_object['y2_down']
                print(up_y, " and ", down_y)
                if up_y >= 450:
                    angle += 3
                    set_servo_angle(5, angle)
                    print("")
                    break
                elif down_y <= 10:
                    angle -= 3
                    set_servo_angle(5, angle)
                    print("Adjusting position to the left.")
            else:
                angle = 90
                set_servo_angle(5, angle)

        except KeyboardInterrupt:
            print("Interrupted by user.")
        except Exception as e:
            print(f"Unexpected error: {e}")


main_thread_process = threading.Thread(target=mainthread, args=(file_path,))
main_thread_process.start()

camera5_process = threading.Thread(target=camera5)
camera5_process.start()

# 스레드가 완료될 때까지 기다립니다.
main_thread_process.join()
camera5_process.join()