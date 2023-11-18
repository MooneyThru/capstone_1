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
                        if distance > 25:
                            robot.set_motor_speed(60, 60)
                        elif distance > 20 and distance < 25:
                            robot.set_motor_speed(30, 30)
                        else:
                            robot.set_motor_speed(0, 0)
                            break
                # 모터 정지
                break  # 원하는 객체를 찾았으므로 while 루프를 빠져나옴
            else:
                # 물체를 찾지 못했으면 정지
                robot.set_motor_speed(0, 0)


        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

# 아두이노와 시리얼 통신 설정

# port = '/dev/ttyACM0' # for Linux
port = 'COM7'         # for Windows
arduino = serial.Serial(port, 9600)  # 'COM포트'는 아두이노가 연결된 포트로 수정
time.sleep(2)  # 시리얼 통신 시작 후 잠시 대기
robot = RobotController(port)

# 링크 길이 정의
link1_length = 12.0
link3_length = 12.0
link4_length = 10.0

while True:
    try:
        cart_items = retrieve_cart_items('cart_items.txt')
        if cart_items:
            print("Items in the cart as a list:")
            for i in range(len(cart_items)):
                if cart_items[i] == 'elephant':
                    cart_items[i] = 'elephant_doll'
                elif cart_items[i] == 'monkey':
                    cart_items[i] = 'monkey_doll'

            for item in cart_items:

                search_for_object(robot, item)
                move_to_target(item)


            #마지막 카트 에 아이템 지우기

        else:
            print("No items in the cart.")

    except KeyboardInterrupt:
        break
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")