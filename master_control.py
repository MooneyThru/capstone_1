import serial
import time
import numpy as np
import robot_arm
import json

class RobotController:
    def __init__(self, port, baud_rate=9600):
        self.serial = serial.Serial(port, baud_rate)
        time.sleep(2)  # Arduino가 재시동하는 동안 기다립니다.

    def set_motor_speed(self, right_speed, left_speed):
        command = f"M1{left_speed}\nM2{right_speed}\n"
        self.serial.write(command.encode())

    def set_servo_angle(self, servo_number, angle):
        command = f"S{servo_number}{angle}\n"
        self.serial.write(command.encode())

    def close(self):
        self.serial.close()


def retrieve_cart_items(file_path):
    try:
        with open(file_path, 'r') as f:
            items = f.read().split('\n')
            items = [item for item in items if item]
            return items
    except FileNotFoundError:
        print("Cart items file not found.")
        return []


def search_for_object(robot, item):
    while True:
        try:
            object_found = False
            # 파일에서 데이터 불러오기
            with open('detected_objects.json', 'r') as f:
                detected_objects = json.load(f)

            # 탐지된 객체 중 원하는 객체가 있는지 확인
            object_found = any(obj['class_name'] == item for obj in detected_objects)

            if object_found:
                print("Object detected!")

                for obj in detected_objects:
                    if obj['class_name'] == item:
                        x_coordinate = obj['x_coordinate']  # 객체의 x 좌표
                        if 4 <= x_coordinate <= 6:
                            object_found = True
                            robot.set_motor_speed(0, 0)
                            break  # 원하는 객체를 찾고 좌표 범위 내에 있으면 루프를 빠져나옴
                # 모터 정지
                break  # 원하는 객체를 찾았으므로 while 루프를 빠져나옴
            else:
                # 물체를 찾지 못했으면 계속 돌기
                robot.set_motor_speed(-20, 20)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


def move_to_target(item):
    # 로봇을 특정 거리만큼 이동시키는 코드
    while True:
        try:
            object_found = False
            # 파일에서 데이터 불러오기
            with open('detected_objects.json', 'r') as f:
                detected_objects = json.load(f)

            # 탐지된 객체 중 원하는 객체가 있는지 확인
            object_found = any(obj['class_name'] == item for obj in detected_objects)

            if object_found:
                print("Object detected!")

                for obj in detected_objects:
                    if obj['class_name'] == item:
                        distance = obj['distance']  # 객체의 x 좌표
                        if distance >= 25:
                            robot.set_motor_speed(60, 60)
                        elif distance >= 20 and distance < 25:
                            robot.set_motor_speed(30, 30)
                        elif distance >= 17 and distance < 20:
                            robot.set_motor_speed(20, 20)
                        else:
                            robot.set_motor_speed(0, 0)
                            break
                # 모터 정지
                break  # 원하는 객체를 찾았으므로 while 루프를 빠져나옴
            else:
                # 물체를 찾는 알고리즘 추가 필요
                # 물체를 찾지 못했면 정지
                robot.set_motor_speed(0, 0)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

def align_with_object(detected_object):

    if detected_object == 'giraffe':
        item = 'giraffe_head'
    elif detected_object == 'elephant_doll':
        item = 'elephant_head'
    else:
        pass

    while True:
        try:
            object_found = False
            # 파일에서 데이터 불러오기
            with open('detected_objects.json', 'r') as f:
                detected_objects = json.load(f)

            # 탐지된 객체 중 원하는 객체가 있는지 확인
            object_found = any(obj['class_name'] == item for obj in detected_objects)

            if object_found:
                for obj in detected_objects:
                    if obj['class_name'] == item:
                        x_coordinate = obj['x_coordinate']  # 객체의 x 좌표
                        if 4 <= x_coordinate <= 6:
                            object_found = True
                            robot.set_motor_speed(0, 0)
                            break  # 원하는 객체를 찾고 좌표 범위 내에 있으면 루프를 빠져나옴
                # 모터 정지
                break  # 원하는 객체를 찾았으므로 while 루프를 빠져나옴
            else:
                # 물체를 찾지 못했으면 계속 돌기
                robot.set_motor_speed(-10, 10)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
def grip_coordinate(detected_object):
    if detected_object == 'giraffe':
        item = 'giraffe_head'
    elif detected_object == 'elephant_doll':
        item = 'elephant_head'
    else:
        pass

    with open('detected_objects.json', 'r') as f:
        detected_objects = json.load(f)

    # 탐지된 객체 중 원하는 객체가 있는지 확인
    object_found = any(obj['class_name'] == item for obj in detected_objects)
    if object_found:
        for obj in detected_objects:
            if obj['class_name'] == item:
                x_target = obj['x_coordinate']  # 객체의 x 좌표
                y_target = obj['y_coordinate']
                z_target = obj['z_coordinate']

    return x_target, y_target, z_target

def pick_up_object(theta2_deg, theta3_deg, theta4_deg):
    # 서보 모터 2, 3, 4의 각도를 설정
    robot.set_servo_angle(4, theta2_deg)
    robot.set_servo_angle(3, theta3_deg)
    robot.set_servo_angle(2, theta4_deg)
    robot.set_motor_speed(-10,-10)
    time.sleep(1)
    robot.set_motor_speed(10, 10)
    time.sleep(1)
    robot.set_servo_angle(1, 30)
    time.sleep(1)
    # 잡은거 확인 하는

    robot.set_servo_angle(4, 180)
    time.sleep(1)
    robot.set_servo_angle(3, 0)
    time.sleep(1)
    robot.set_servo_angle(2, 100)

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

# port = '/dev/ttyACM0' # for Linux
port = 'COM7'         # for Windows
arduino = serial.Serial(port, 9600)  # 'COM포트'는 아두이노가 연결된 포트로 수정
time.sleep(2)  # 시리얼 통신 시작 후 잠시 대기
robot = RobotController(port)

while True:
    try:
        cart_items = retrieve_cart_items('cart_items.txt')
        if cart_items:
            print("Items in the cart as a list:")
            if cart_items[0] == 'elephant':
                cart_items[0] = 'elephant_doll'
            elif cart_items[0] == 'monkey':
                cart_items[0] = 'monkey_doll'
            item = cart_items[0]

            search_for_object(robot, item)
            move_to_target(item)
            # 물체 정중앙 위치시키기
            align_with_object(item)

            # 좌푯값 가져와서 잡기
            x_target, y_target, z_target = grip_coordinate(item)
            theta2_deg, theta3_deg, theta4_deg = robot_arm.inverse_kinematics(x_target, y_target, z_target)
            pick_up_object(robot, theta2_deg, theta3_deg, theta4_deg)

            item = 'target_item'

            # 물체의 좌표를 가져와서 로봇 암을 해당 위치로 이동
            search_for_object(robot, item)
            move_to_target(item)
            # 좌푯값 가져와서 내려 놓기
            align_with_object(item)
            x_target, y_target, z_target = grip_coordinate(item)
            theta2_deg, theta3_deg, theta4_deg = robot_arm.inverse_kinematics(x_target, y_target, z_target)

            # 설정된 위치에 물체를 내려놓기
            place_object(robot, theta2_deg, theta3_deg, theta4_deg)

            #마지막 카트 에 아이템 지우기
            cart_items.pop(0)

        else:
            print("No items in the cart.")
            time.sleep(15)

    except KeyboardInterrupt:
        break
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")